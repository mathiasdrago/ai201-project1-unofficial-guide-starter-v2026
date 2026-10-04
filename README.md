# The Unofficial Guide

This repository builds an answer system for the campus_life corpus. It loads student-written advice and administrative notes, retrieves the closest chunks to a user question, and answers only from those source documents.

---

# Unit 1

## What This Does

I used the campus_life corpus, which is made up of short student posts about housing, registration, dining, and course advice. The app ingests those documents, embeds each chunk, retrieves the closest matches for a question, and then answers using only the retrieved passages plus the source file names. It is designed for practical questions like when to book an adviser appointment or how the housing lottery actually works.

## Chunking Strategy

**Chunk size:** 500 characters
**Overlap:** 120 characters

I chose this chunk size for the campus_life corpus because the documents are mostly short posts with one or two paragraphs of useful advice. A 500-character window is long enough to keep an entire thought together but short enough that the answer is not buried inside a long block of unrelated detail. I kept 120 characters of overlap so adjacent chunks still preserve continuity when a paragraph is split across boundaries. The real test was reading the raw documents and noticing that most useful facts sit in a single paragraph, so cutting at a strict 800-character fixed length would have created noisy chunks or left entire posts unbroken.

## Sample Chunks

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_biol_160_exams.txt#0` — produced by: `chunker.py::split_documents`

```
BIOL 160 Cell Biology — assessment

Four unit tests and a cumulative final. Not curved.

The unit tests come fast, roughly every three weeks; falling behind once is very hard to recover from.
```

**Chunk 3** — source: `course_math_220_exams.txt#0` — produced by: `chunker.py::split_documents`

```
MATH 220 Linear Algebra — assessment

Two midterms and a cumulative final. Curved to a b- median.

The problem sets are the course; the lectures make sense afterwards rather than during.
```

**Chunk 4** — source: `dining_the_ridgeway_cafe.txt#0` — produced by: `chunker.py::split_documents`

```
The Ridgeway Café

Second-year here. Wait times: 10 to 15 minutes at 12:30, none after 2:00. The thing worth going for is the only place on campus with real espresso. The thing to know is that seating is tight; about 40 seats for a building of 900.

Hours are 7:00am to 4:00pm weekdays only. Costs declining balance only, no meal swipes.
```

**Chunk 5** — source: `housing_morrow_house.txt#0` — produced by: `chunker.py::split_documents`

```
Morrow House — what it's actually like

Just finished a year in this building. Built 1954, partially renovated 2008. Rooms are singles and doubles, hall bathrooms.

The good: cheapest housing tier by about $900 a year, and the singles are real singles.

The bad: known damp problem on the ground floor; two rooms were taken offline in 2024.

Laundry costs $1.50 wash, $1.25 dry, coin or card. On noise: loud until about 1am on weekends, no enforced quiet hours.
```

## Sample Answer

**Question:** How do students say the housing lottery works for juniors and seniors?

**Answer:** According to `admin_housing_lottery.txt`, juniors and seniors in the housing lottery are ordered by accumulated credit hours first, with ties broken randomly.

```
According to *admin_housing_lottery.txt*, juniors and seniors in the housing lottery are ordered by accumulated credit hours first, with ties broken randomly.
```

**My relevance cutoff:** 0.6

The in-corpus distances were all well below the cutoff: 0.219, 0.355, 0.393, 0.422, and 0.377. The out-of-scope questions were much further away: 0.825, 0.934, 0.886, 0.844, and 0.896. That gap made 0.6 a clean middle ground: it rejects unrelated questions without discarding the real answers.

| Question | In corpus? | Best distance |
|---|---|---|
| How do students say the housing lottery works for juniors and seniors? | Yes | 0.2186 |
| What do students say about the final exam in CS 210 and how is it different from the textbook? | Yes | 0.3552 |
| When should students book an adviser appointment before registration opens? | Yes | 0.3933 |
| Why do students recommend doing the labs in CS 210 even though they are only 10 percent of the grade? | Yes | 0.4219 |
| What is the main timing advice for the housing lottery and when does selection run? | Yes | 0.3767 |
| What is the capital of Mongolia? | No | 0.8246 |
| How do I change the oil in a diesel engine? | No | 0.9340 |
| Who won the 1994 World Cup? | No | 0.8859 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.8442 |
| How do I write a for loop in Rust? | No | 0.8960 |

## How I Used AI

**1.** I asked an AI tool to help me design a chunking strategy for short campus-life posts. It suggested a paragraph-oriented approach, but it did not account for a proper overlap rule. I changed the implementation to split on paragraph breaks, fall back to sentence-based splitting for extra-long sections, and keep each chunk readable as a standalone thought.

**2.** I asked an AI tool where to set the relevance cutoff after I computed the distances. It suggested a generic number without tying it to the corpus, so I used the actual in-corpus and out-of-scope distance groups to place the threshold in the gap between them. That produced a cutoff of 0.6, which is specific to this corpus and test set rather than a random default.

**3.** In Unit 2, I used an AI tool to review my verdicts and check whether my interpretation of the results was reasonable. I asked it to argue the opposite of my MET/MISSED decisions to ensure I wasn't being too generous in my self-assessment. This helped confirm that my targets were set appropriately.

---

# Unit 2

## Run Log — Before

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. At least 4 of 5 sampled chunks read as a complete thought | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. For at least 4 of 5 test questions, the answer includes the expected phrase and a source | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

### Real output for each criterion

**Criterion 1 output** — produced by `run_eval.py::main` with retrieval from `store.py::search`:

Question 2 across all three runs:
```
Run 1: The documents do not mention student opinions about the final exam in CS 210, so I do not have enough information to answer that part of the question. However, the documents state that the exams are drawn from lecture material rather than the textbook (course_cs_210.txt and course_cs_210_exams.txt).

Run 2: The documents do not contain any statements from students specifically about what they say regarding the final exam in CS 210, but they do state that the exams are drawn from lecture material rather than the textbook.

Files used: course_cs_210.txt and course_cs_210_exams.txt

Run 3: Based on the documents, the final exam in CS 210 is not curved, whereas the midterms are (course_cs_210.txt and course_cs_210_exams.txt). Additionally, the exams are drawn from the lecture material rather than the textbook (course_cs_210.txt and course_cs_210_exams_txt).

Files used: course_cs_210.txt and course_cs_210_exams.txt
```

**Criterion 2 output** — produced by `generate.py::answer_from_chunks`:

All 5 questions across all 3 runs include source citations. Example from question 3:
```
Students should book their adviser appointment two weeks before registration opens.

Source: advising_registration.txt
```

**Criterion 3 output** — produced by `run_eval.py::check_out_of_scope`:

```
Out-of-scope questions (the gate should refuse these):
  refused  (best distance 0.825)  What is the capital of Mongolia?
  refused  (best distance 0.934)  How do I change the oil in a diesel engine?
  refused  (best distance 0.886)  Who won the 1994 World Cup?
  refused  (best distance 0.844)  What is the recommended dosage of ibuprofen for a headache?
  refused  (best distance 0.896)  How do I write a for loop in Rust?
  -> gate refused 5 of 5
```

**Criterion 4 output** — produced by `chunker.py::split_documents`:

Sample chunks from the index:
```
Chunk 1 — housing_tamsin_court_noise.txt#0
Noise levels in Tamsin Court

Asked about this a lot so writing it down. Quiet, structurally — concrete floors between units.

If you're someone who needs quiet to work, the library is open until 2am during term and that's what most people in this building end up doing.

Chunk 2 — admin_wifi_and_accounts.txt#0
On the wifi and accounts

Your student account gives you campus wifi, printing, and a cloud drive with unlimited storage that most people never discover. The account stays active for six months after you graduate, and the cloud drive is purged at that point without a second warning.
```

**Criterion 5 output** — produced by `generate.py::answer_from_chunks`:

All answers include expected phrases. Example from question 4:
```
Students recommend doing the labs because the exams reuse the lab problems.

Source: course_cs_210_exams.txt (also mentioned in course_cs_210.txt)
```

## Verdicts

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer | MET | All three runs scored 4/5. Question 2 asks for student opinions about the final exam, which aren't in the corpus — the chunks only contain information about the textbook difference. The other 4 questions had answers in the retrieved chunks. Since the target was 4 of 5 and this held consistently across all runs, this is MET. |
| 2 | Every answer names a source | MET | All 5 questions named a source in all 3 runs (5/5 each). The target was 5 of 5, and the system delivered it consistently. |
| 3 | Gate stops out-of-corpus questions | MET | The gate refused all 5 out-of-scope questions (5/5), exceeding the target of 4 of 5. This was deterministic and identical across all runs. |
| 4 | At least 4 of 5 sampled chunks read as a complete thought | MET | I sampled 5 chunks from the index and all 5 read as complete thoughts with no sentences cut in half. The target was 4 of 5, so this is MET. |
| 5 | For at least 4 of 5 test questions, the answer includes the expected phrase and a source | MET | All 5 questions included their expected phrases ("credit hours", "lecture material", "two weeks out", "lab problems", "second week of March") and named sources in all 3 runs (5/5 each). The target was 4 of 5, so this is MET. |

## Diagnoses

No criteria were missed in the baseline run.

**Assessment of target difficulty:**

The system cleared every criterion on the first try, which suggests the targets were set conservatively rather than aggressively. Looking at each criterion:

- **Criterion 1 (retrieval):** Target was 4 of 5, achieved 4 of 5. The miss on question 2 is a legitimate limitation — the question asks for "what students say" about the final exam, but the corpus only contains factual information about the exam structure, not student opinions. This is a corpus limitation, not a system failure. A stricter target of 5 of 5 would have been unreasonable given the question design.

- **Criterion 2 (source attribution):** Target was 5 of 5, achieved 5 of 5. This was appropriately strict — every answer should be traceable.

- **Criterion 3 (gate):** Target was 4 of 5, achieved 5 of 5. The 0.6 cutoff separates in-corpus distances (0.2-0.4) from out-of-scope distances (0.8-0.9) cleanly, so this was correctly calibrated.

- **Criterion 4 (chunking):** Target was 4 of 5, achieved 5 of 5. The paragraph-based chunking strategy works well for this corpus of short posts. A more aggressive test would have sampled more chunks or looked for edge cases like very long paragraphs.

- **Criterion 5 (answer quality):** Target was 4 of 5, achieved 5 of 5. The system consistently included the expected phrases. A tighter criterion would have checked for accuracy of the full answer, not just presence of a keyword.

**Criterion I would tighten:**

If I were to write this again, I would tighten **Criterion 5** to check not just for the presence of an expected phrase, but for the accuracy of the complete answer. The current criterion only requires that the answer mentions "credit hours" or "lab problems" — it doesn't verify that the surrounding context is correct. A revised version would be: "For at least 4 of 5 test questions, the answer is factually complete and accurate according to the source documents." This would have made the test more meaningful but also harder to pass.

## The Improvement

**What I changed:**

I implemented hybrid search in `store.py` by adding a `search_hybrid` function that combines semantic search (cosine similarity from embeddings) with BM25 keyword search. The function ranks chunks using a weighted combination: 70% semantic similarity and 30% BM25 score. I also updated `run_eval.py` to accept a `--hybrid` flag that uses this new retrieval method.

**Why I picked it:**

Although all criteria were met in the baseline, the Milestone 4 instructions suggest hybrid search as a primary improvement option for questions containing names, numbers, or exact terms. My test questions include specific terms like "credit hours," "lecture material," "two weeks," "lab problems," and "second week of March." Hybrid search is designed to help surface chunks containing these exact keywords, which semantic search might miss if the meaning is spread across the corpus rather than concentrated in one document.

### Run Log — After

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. At least 4 of 5 sampled chunks read as a complete thought | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. For at least 4 of 5 test questions, the answer includes the expected phrase and a source | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

**Did it help?**

No measurable improvement. All five criteria show identical results before and after the change: Criterion 1 still scores 4/5 (question 2 misses because the corpus lacks student opinions), and criteria 2-5 still meet their targets. The semantic distances are identical across all questions, and the retrieved sources are nearly the same with only minor variations in the 4th and 5th results.

This outcome makes sense: the baseline semantic search was already well-matched to this corpus of short, factual posts. The BM25 component didn't change the ranking because the embeddings already captured the relevant meaning. Hybrid search would likely show more benefit on a corpus with longer documents, more technical terminology, or questions about exact phrases that don't have strong semantic matches.

## What's Still Broken

All criteria are met after the improvement, so nothing is strictly "broken." However, there are still areas where the system could be improved:

**Criterion 1 (retrieval):** Question 2 consistently misses because it asks for "what students say" about the final exam, but the corpus only contains factual information about exam structure, not student opinions. This is a corpus limitation, not a system failure. To fix this, I would either:
- Rewrite the question to ask about the factual information that exists in the corpus (e.g., "How is the final exam in CS 210 different from the textbook?")
- Add student-written documents that actually contain opinions and experiences

**Criterion 5 (answer quality):** While all answers include the expected phrases, the current criterion only checks for keyword presence, not full accuracy. A tighter criterion would verify that the complete answer is factually correct. For example, question 2's answer correctly states that exams are drawn from lecture material, but it doesn't actually address "what students say" because that information doesn't exist in the corpus.

**Why I stopped here:**

I stopped after implementing hybrid search because the assignment requires only one improvement, and I completed it with proper measurement (before/after runs). The hybrid search didn't improve results, but that's a valid finding — not every optimization helps on every corpus. The most impactful next step would be to tighten Criterion 5 to check for complete answer accuracy rather than just keyword presence, which would be a more meaningful test of the system's actual performance.

## What I'd Do Differently

Knowing what I know now, I would rewrite **Criterion 5** to be more stringent. The current criterion is:

> "For at least 4 of 5 test questions, the answer includes the expected keyword or phrase and names the source file it came from."

This only checks for the presence of a keyword (e.g., "credit hours" or "lab problems"), not whether the full answer is accurate. A system could mention the keyword while getting the surrounding context wrong and still pass this criterion.

I would rewrite it as:

> "For at least 4 of 5 test questions, the answer is factually complete and accurate according to the source documents, and names the source file it came from."

This would require manually verifying each answer against the source documents, not just checking for a keyword. It would be harder to pass but would be a more meaningful test of whether the system actually works. The original Criterion 5 was too easy — passing it doesn't guarantee the answers are correct, only that they mention the right terms.

I would also reconsider **Criterion 1**. The target of 4 of 5 is reasonable, but the miss on question 2 is a question design issue rather than a system issue. If I were to write this again, I would ensure all five questions are answerable from the corpus before setting the criterion, or I would explicitly note which questions are known to be partially unanswerable and adjust the target accordingly.

