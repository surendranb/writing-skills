/**
 * Telemetry relay for writing-skills MCP (SUR-88 pattern, SUR-267 Phase 2).
 * /e ingests events: validate, cap, forward to PostHog with CF edge props.
 * Spec: $ip = CF-Connecting-IP, cf_asn / cf_as_organization / cf_colo /
 * cf_verified_bot / cf_bot_score / cf_edge_country; no $geoip_* props.
 * POSTHOG_API_KEY lives in a Worker secret, never in this repo.
 */

const GATEWAY_VERSION = "1";

const KNOWN_EVENTS = new Set([
  "mcp_started", "tool_executed", "server_first_install", "resource_read",
  "package_download", "tools_listed", "trouble", "session_end",
]);

const MAX_PROPS_BYTES = 65536;

// Per-instance caps: distinct_id 600 events/hr, IP 3600/hr.
// ponytail: in-memory per-isolate windows; per-isolate only, upgrade to
// Durable Object counters if multi-isolate abuse shows up.
const WINDOW_MS = 3600_000;
const CAP_BY_DISTINCT_ID = 600;
const CAP_BY_IP = 3600;
const buckets = new Map();

function capped(key, cap) {
  const now = Date.now();
  let hits = buckets.get(key);
  if (!hits) {
    hits = [];
    buckets.set(key, hits);
  }
  hits = hits.filter((t) => now - t < WINDOW_MS);
  if (hits.length >= cap) {
    buckets.set(key, hits);
    return true;
  }
  hits.push(now);
  buckets.set(key, hits);
  return false;
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    if (request.method === "GET" && (url.pathname === "/" || url.pathname === "/health")) {
      return new Response("ok", { headers: { "content-type": "text/plain" } });
    }

    if (request.method !== "POST" || url.pathname.toLowerCase() !== "/e") {
      return Response.redirect(env.DOCS_URL, 302);
    }

    const userAgent = request.headers.get("user-agent") || "";
    const clientIp = request.headers.get("cf-connecting-ip") || "";
    const dnt = request.headers.get("dnt") === "1" || request.headers.get("sec-gpc") === "1";
    const internal = request.headers.get("x-writing-skills-internal") === "1";

    if (dnt) {
      return json({ recorded: false, reason: "dnt" });
    }

    // Default-library UAs are rejected unless the caller marks itself internal.
    if (/python-requests|python-urllib|go-http-client|node-fetch|axios\/|curl\/|wget\//.test(userAgent.toLowerCase()) && !internal) {
      return json({ recorded: false, reason: "rejected_ua" }, 403);
    }

    if (capped(`ip:${clientIp}`, CAP_BY_IP)) {
      return json({ recorded: false, reason: "rate_limited" }, 429);
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return json({ recorded: false, reason: "invalid_json" }, 400);
    }

    const eventName = typeof body.event === "string" ? body.event : "";
    if (!/^[a-z_][a-z0-9_]{0,63}$/.test(eventName)) {
      return json({ recorded: false, reason: "invalid_event_name" }, 400);
    }
    if (!KNOWN_EVENTS.has(eventName)) {
      return json({ recorded: false, reason: "unregistered_event" }, 400);
    }

    const distinctId = String(body.distinct_id || `anon_${crypto.randomUUID()}`).slice(0, 200);
    if (capped(`id:${distinctId}`, CAP_BY_DISTINCT_ID)) {
      return json({ recorded: false, reason: "rate_limited" }, 429);
    }

    const cf = request.cf || {};
    let props = (body.properties && typeof body.properties === "object") ? body.properties : {};
    const propsSize = JSON.stringify(props).length;
    if (propsSize > MAX_PROPS_BYTES) {
      props = { payload_truncated: true, original_size_bytes: propsSize };
    }

    props.$ip = clientIp;
    props.$geoip_disable = false;
    props.cf_asn = cf.asn || 0;
    props.cf_as_organization = cf.asOrganization || "unknown";
    props.cf_colo = cf.colo || "unknown";
    props.cf_verified_bot = Boolean(cf.verified_bot);
    props.cf_bot_score = typeof cf.botManagement?.score === "number" ? cf.botManagement.score : null;
    props.cf_edge_country = cf.country || "unknown";
    props.via_gateway = true;
    props.gateway_version = GATEWAY_VERSION;
    props.traffic_class = internal ? "internal" : "external";
    if (!body.distinct_id) props.missing_distinct_id = true;
    if (cf.asOrganization === "Anthropic, PBC") props.managed_agent = "claude_managed";

    ctx.waitUntil(sendPostHogEvent(env, {
      event: eventName,
      distinct_id: distinctId,
      properties: props,
    }));
    return json({ recorded: true });
  },
};

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "content-type": "application/json" },
  });
}

async function sendPostHogEvent(env, payload) {
  try {
    await fetch(`${env.POSTHOG_HOST}/capture/`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        api_key: env.POSTHOG_API_KEY,
        event: payload.event,
        distinct_id: payload.distinct_id,
        properties: payload.properties,
        timestamp: new Date().toISOString(),
      }),
    });
  } catch (err) {
    // Fail silently — telemetry never blocks the caller.
  }
}