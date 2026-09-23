# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
Campus life posts are short and factual, so a retrieval system should be able to surface the exact document that answers the question most of the time. I set the target at 4 of 5 because one question is anchored in a more specific detail that may be harder to match than the others.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
This corpus is built around student advice and administrative facts, so source attribution is part of the promise of the app. I chose 5 of 5 because every answer should be traceable to a file, and a single missing source would make the result feel ungrounded even if the summary is otherwise correct.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

**Why this target:**
The cutoff has to separate in-corpus questions from clearly unrelated ones without being so strict that it blocks real answers. I picked 4 of 5 because the app is allowed to miss one out-of-scope question, but it should not keep hallucinating answers to questions the corpus cannot answer.

---

## 4. Sampled chunks read as complete thoughts

At least 4 of 5 sampled chunks read as a complete thought, with no sentence cut
in half at either end.

**Why this target:**
I chose this because the short campus-life posts rely on one idea per paragraph, and a chunk that cuts through the middle of a sentence is much less useful. A 4-of-5 standard is realistic for a corpus with a few edge cases, while still making sure the chunker is not producing fragments most of the time.

---

## 5. Answers include the expected phrase and a source

For at least 4 of 5 test questions, the answer includes the expected keyword or
phrase and names the source file it came from.

**Why this target:**
The app is supposed to answer real questions from the corpus, not just say something vaguely relevant. I wanted a criterion that checks both content and grounding: the answer has to mention the fact in the same terms the question is asking for, and it has to point back to a document so a reader can verify it.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
