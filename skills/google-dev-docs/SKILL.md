---
name: google-dev-docs
description: Write developer documentation to the Google developer documentation style guide — active voice, second person, present tense, task-oriented headings. Use when the user writes API docs, READMEs, tutorials, reference guides, error messages, or any technical content for developers.
---

# Google Developer Docs

Write for the developer with a question and a deadline. Clarity over cleverness, always.

## The core rule

**Answer the reader's question in the fewest steps, in active voice, addressed to "you", in present tense.** Developer docs are read at the moment of need: an error on screen, a deadline, a broken build. Every paragraph must justify itself against that reader.

Workflow: `name the task in the heading (verb-first)` → `state what the reader will accomplish` → `give the steps in order, one action each` → `show a real example` → `note the failure modes`.

## Mechanics

1. **Active voice always.** "The API returns a list" not "a list is returned by the API".
2. **Address the reader as "you".** "Install the SDK" not "one installs the SDK" and never "we".
3. **Present tense.** "The server listens on port 8080" not "will listen".
4. **Task-oriented, verb-first headings.** "Authenticate a user" not "Authentication"; "Configure the proxy" not "Proxy configuration".
5. **One action per step, numbered.** Steps are imperative, complete, and checkable.
6. **Examples are real and copyable.** Include actual code/output the reader can run; never pseudo-examples for the happy path only — show the common error too.
7. **Explain the "why" once, briefly.** One sentence of rationale per non-obvious decision; then move on.
8. **Consistent terminology.** Pick one term per concept ("request", never "call/invoke/query" interchangeably). Include a definitions list where terms collide.
9. **Plain language layer.** Even technical prose obeys plain-language rules: short sentences, no marketing, no "effortlessly/simply/seamlessly".
10. **Error messages are docs too.** Say what failed, why, and how to fix: "Error: port 8080 is in use. Stop the process using it, or set PORT to a free port."

## Verify

- Every heading starts with a verb (or a noun that is the reader's search term)
- No passive voice (search "was/were/are + past participle")
- No "we" referring to your org; no marketing adjectives (simple, easy, powerful, robust)
- Every step is imperative, numbered, and results in something checkable
- Present tense throughout (search "will ", "would ")
- At least one runnable example per tutorial section

## Do not

- Write "getting started" without stating prerequisites up front
- Hide errors — document what breaks and why
- Use the reader's learning time for product marketing

## Example transformations

**Before:** "In order to make use of the API, it is necessary that an API key be obtained. This can be done by navigating to the dashboard, where the key will be displayed once a project has been created. The key should then be included in the Authorization header of every request that will be made."

**After:** "1. Create a project in the dashboard. 2. Copy your API key. 3. Send it with every request: Authorization: Bearer YOUR_KEY. All requests must include this header; without it, the API returns 401."

**Before:** "The system is designed to facilitate seamless integration of third-party services through a robust and flexible webhook architecture."

**After:** "Webhooks notify you when an event happens (for example, a payment succeeds). Add your webhook URL to the dashboard, and we'll POST the event payload to it within 2 seconds."