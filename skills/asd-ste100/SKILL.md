---
name: asd-ste100
description: Use when writing technical procedures, instructions, warnings, maintenance manuals, or any text where every reader including non-native English speakers must understand exactly one meaning.
compatibility: Requires standard Markdown parser and agent context
---

# ASD-STE100 Simplified Technical English

Control vocabulary and syntax to eliminate ambiguity in technical documentation.

## The core rule

**One word, one meaning. Imperative voice for instructions. Maximum 20 words per sentence.**

Workflow: `choose approved STE vocabulary` → `write imperative command` → `restrict sentence length to 20 words max` → `verify zero ambiguity`.

## Mechanics

1. **Approved vocabulary.** Use only words from the ASD-STE100 dictionary or approved technical nouns.
2. **Imperative commands.** Start steps with an action verb ("Remove the bolt", not "You should remove the bolt").
3. **Word count limits.** Maximum 20 words for procedural sentences; maximum 25 words for descriptive sentences.
4. **No noun clusters.** Maximum of 3 nouns in a sequence (e.g. use "valve control switch" instead of "engine fuel system valve control switch").
5. **Present tense.** Describe current states in present tense; avoid future tense ("The light is on" not "The light will turn on").
6. **No gerunds in titles.** Use simple nouns or infinitives for headings.
7. **Explicit conditions.** Place conditional clauses at the beginning of the sentence ("If the pressure is low, replace the filter").
8. **Approved modifiers.** Avoid vague adjectives like "extreme", "rapid", or "normal" unless quantified.

## Verify

- Sentences do not exceed 20 words for procedures
- Every instruction starts with an active imperative verb
- No noun clusters exceeding 3 words
- All technical terms conform to standard dictionary definitions
- Zero ambiguous pronouns (replace "it" or "they" with specific nouns)

## Do not

- Use words with multiple meanings (e.g., use "fast" or "secure", avoid "fixed")
- Write conditional clauses after the main action
- Use contractions or colloquialisms
- Use passive voice in maintenance steps

## References

For the enforceable limits (sentence/paragraph/noun-cluster caps), safety-text structure (WARNING/CAUTION/NOTE), and punctuation rules, read `references/REFERENCE.md` when a draft is borderline or needs verification — load on demand, not upfront.

## Example transformations

**Before:** "It is recommended that technicians should carefully inspect the aforementioned component assembly for any potential signs of wear prior to system operation."

**After:** "Inspect the component assembly for wear before you operate the system."

**Before:** "When the pressure drops too low, you might want to consider resetting the main system valve."

**After:** "If the pressure is low, reset the main valve."
