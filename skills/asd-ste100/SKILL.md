---
name: asd-ste100
description: Write controlled, unambiguous technical prose per ASD-STE100 Simplified Technical English — the aerospace standard for maintenance manuals and technical documentation. Use when the user writes technical procedures, instructions, warnings, manuals, or any text where every reader (including non-native English speakers) must understand exactly one meaning.
---

# ASD-STE100 (Simplified Technical English)

One sentence, one instruction, one meaning. The standard for safety-critical documentation.

## The core rule

**Every sentence has exactly one interpretation — because every sentence has one instruction, one approved word, and no synonyms.** STE-100 trades elegance for certainty: writers cannot choose between "start", "begin", "activate", "commence" — they use the approved word and only the approved word.

Workflow: `state the objective` → `write instructions as short imperative sentences` → `use only approved vocabulary, one meaning per word` → `separate warnings from actions` → `run the verification checklist`.

## Mechanics

1. **One instruction per sentence.** "Open the valve. Wait 30 seconds. Close the valve." Never chain ("open the valve, then after waiting, close it").
2. **Sentences ≤ 20 words** (procedures); ≤ 25 for descriptions.
3. **Imperative mood for procedures.** "Remove the cover." — direct commands only.
4. **One meaning per word, always.** Approved technical terms mean one thing; never use a synonym in the same document. Pick "remove" and never "detach/unfasten/take off" for the same object.
5. **Active voice, present tense.** "The pump moves the fluid" not "the fluid is moved by the pump".
6. **No verbs derived from nouns** (make a decision → decide; perform an inspection → inspect).
7. **Articles always required.** "The valve", "an adapter" — never bare "valve" where grammar allows dropping the article.
8. **Warnings are exact and separate.** "WARNING: HIGH PRESSURE. Do not open the valve while the system is pressurized." Structure: warning keyword, hazard, consequence, instruction.
9. **Numbers and units written exactly.** "6 mm", "100 °C" — spelled-out numbers only for 1–9 where the approved dictionary says so.
10. **No idioms, no metaphor, no humor.** "It's the heart of the system" is banned. The reader may not share the culture.

## Verify

- Every sentence ≤ 20 words and contains exactly one instruction
- Every sentence in active voice (no "was/were + past participle")
- No synonyms for the same object/action anywhere in the document
- No noun-verb constructions ("perform a test" → "test")
- No idioms or metaphors (search for "like", "as if", figurative phrases)
- Warnings follow the keyword-hazard-consequence-instruction shape

## Do not

- Chain instructions with "then/after/while" — split them
- Use unapproved vocabulary for any safety-critical step
- Assume a shared cultural or technical background with the reader

## Example transformations

**Before:** "Prior to commencing the disassembly process, ensure that the pressure has been completely relieved from the system, as failure to do so may result in the sudden and dangerous release of pressurized fluid which could cause serious injury or even death."

**After:** "WARNING: HIGH PRESSURE. The fluid in the system is under pressure. If you open the system while it is pressurized, the fluid can spray out and cause injury. 1. Turn the system OFF. 2. Wait until the pressure gauge shows zero. 3. Open the drain valve."

**Before:** "When you've finished, it's good practice to give the unit a quick check for any loose connections and make sure everything is nice and snug."

**After:** "Check all connections. Tighten any loose connection. Make sure each connection is secure."