---
name: google-dev-docs
description: Use when writing API documentation, READMEs, tutorials, reference guides, error messages, or any technical content for developers using the Google developer documentation style guide.
compatibility: Requires standard Markdown parser and agent context
---

# Google Developer Documentation Style

Write precise, task-oriented technical documentation with second-person address and active voice.

## The core rule

**Task-oriented headings, present tense, second person ("you"), active voice.**

Workflow: `state user goal in title` → `prerequisites first` → `numbered steps with concrete code examples` → `verification step`.

## Mechanics

1. **Second person.** Address the developer directly as "you"; avoid "we", "us", or third-person generalities.
2. **Present tense.** Describe current system behavior in present tense ("Returns a 200 OK status", not "Will return").
3. **Task-oriented headings.** Start headings with gerunds or action verbs ("Configuring authentication", not "Authentication overview").
4. **Active voice.** "The server processes the request" rather than "The request is processed by the server".
5. **Code blocks with context.** Every code snippet must include necessary imports, setup, and expected output.
6. **Pronoun clarity.** Ensure "this", "that", and "it" clearly point to a preceding noun.
7. **Consistent terminology.** Use identical terms across guides, API references, and UI labels.
8. **Concise error messages.** Explain what went wrong and how to fix it immediately.

## Verify

- Headings use gerunds or action verbs describing tasks
- Sentences consistently use second person ("you")
- Code snippets are complete, syntactically valid, and tested
- Active voice used throughout instructions
- Present tense used for API descriptions

## Do not

- Use future tense for deterministic software behavior ("The method will return...")
- Leave code snippets without imports or setup context
- Use vague filler phrases ("Simply run...", "Just configure...")
- Mix second person and first person within the same tutorial

## References

For exact mechanical rules (numbers, percentages, ordinals, ranges, abbreviations, units), read `references/REFERENCE.md` when a draft contains any of these — load on demand, not upfront.

## Example transformations

**Before:** "In order to initialize our SDK, users are required to first invoke the setup method, after which time you will be able to make API requests successfully."

**After:** "To initialize the SDK, call `setup()`. Once initialized, you can make API requests."

**Before:** "Simply add the configuration dictionary to your project and you're good to go!"

**After:** "Add the configuration dictionary to your project configuration file."
