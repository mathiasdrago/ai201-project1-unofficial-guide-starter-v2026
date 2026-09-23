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

---

# Unit 2

## Run Log — Before

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. At least 4 of 5 sampled chunks read as a complete thought | 4 of 5 |  |  |  |  |
| 5. For at least 4 of 5 test questions, the answer includes the expected phrase and a source | 4 of 5 |  |  |  |  |

## Verdicts

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

## The Improvement

**What I changed:**

**Why I picked it:**

### Run Log — After

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. At least 4 of 5 sampled chunks read as a complete thought | 4 of 5 |  |  |  |  |
| 5. For at least 4 of 5 test questions, the answer includes the expected phrase and a source | 4 of 5 |  |  |  |  |

**Did it help?**

## What's Still Broken

## What I'd Do Differently

