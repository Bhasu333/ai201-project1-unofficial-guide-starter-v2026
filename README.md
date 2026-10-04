# The Unofficial Guide

Bhaswath Datla — campus_life corpus

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.

---

# Unit 1

## What This Does

I picked the `campus_life` corpus, which contains 88 short student posts about college life, dorms, dining, course workloads, and administrative rules. This system is a retrieval-augmented question answering tool that lets students ask plain questions about campus survival tips, like housing lottery quirks or laundry costs. When a question is asked, it retrieves the most relevant post chunks, checks whether they are actually relevant via a distance cutoff gate, and generates a grounded response citing the exact source file.

## Chunking Strategy

**Chunk size:** 800
**Overlap:** 120

When looking at the documents in `corpora/campus_life/documents`, almost every file is an individual post between 178 and 549 characters, with an average length of about 317 characters. With the starter's default 800 character window, every post was already smaller than 800 characters so it didn't split anything (88 documents produced exactly 88 chunks). 

However, rather than blindly cutting text by character offsets if longer posts are added later, I updated `split_documents` so that each post stays as one complete chunk if it's under 800 characters, and splits on double newlines (`\n\n`) for paragraphs if it exceeds that size. This keeps every student thought intact without cutting sentences in half or creating 2-character trailing fragments.

## Sample Chunks

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_biol_160.txt#0` — produced by: `chunker.py::split_documents`

```
BIOL 160 Cell Biology

I lived here my sophomore year. Format is lecture three times a week with a weekly lab. Assessment: four unit tests and a cumulative final. Not curved.

Expect 9 to 11 hours a week, the heaviest first-year course by reputation.

The one piece of advice: the unit tests come fast, roughly every three weeks; falling behind once is very hard to recover from.
```

**Chunk 3** — source: `course_hist_118_workload.txt#0` — produced by: `chunker.py::split_documents`

```
Workload for HIST 118 Modern World History

People keep asking so: a lot of reading, about 120 pages a week, but no problem sets. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.
```

**Chunk 4** — source: `dining_pellew_dining_hall_followup.txt#0` — produced by: `chunker.py::split_documents`

```
Re: Pellew Dining Hall

Adding to what people have said about Pellew Dining Hall. The wait figure of 12 to 18 minutes at peak matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely.

Also worth saying: the furthest hall from anywhere, next to the athletics centre. Nobody tells you this at orientation.
```

**Chunk 5** — source: `housing_innisfree_hall.txt#0` — produced by: `chunker.py::split_documents`

```
Innisfree Hall — what it's actually like

Transferred in last year, so take this with a grain of salt. Built 1991, renovated 2022. Rooms are doubles arranged as pairs sharing one bathroom between two rooms.

The good: the shared-bathroom-between-two-rooms arrangement is the best compromise on campus.

The bad: no air conditioning, which matters for the first three weeks of September.

Laundry costs $1.75 wash, $1.75 dry, app-based. On noise: moderate; the building is L-shaped and the short wing is much quieter.
```

## Sample Answer

**Question:** Is the housing lottery actually random?

**Answer:**

```
The housing lottery is not completely random. While rising sophomores receive a randomly drawn number, juniors and seniors are prioritized by their accumulated credit hours first and only use random selection to break ties (admin_housing_lottery.txt).
```

**My relevance cutoff:** 0.60

I ran my five test questions and the five out-of-scope questions using `app.py retrieve` to check the cosine distance of the closest match for each. The in-corpus questions all had closest distances ranging between 0.198 and 0.423. The out-of-scope questions had best distances ranging from 0.825 to 0.934. There is a huge gap between 0.423 and 0.825, so 0.60 sits right in the middle, giving plenty of buffer to accept valid variations of in-corpus questions while easily refusing completely unrelated questions.

| Question | In corpus? | Best distance |
|---|---|---|
| Is the housing lottery actually random? | Yes | 0.248 |
| How many pages can I print with my printing quota? | Yes | 0.423 |
| What are the library hours during reading week? | Yes | 0.404 |
| What are the lunch wait times at Kestrel Commons? | Yes | 0.198 |
| How much does laundry cost in Old Brewhouse? | Yes | 0.216 |
| What is the capital of Mongolia? | No | 0.825 |
| How do I change the oil in a diesel engine? | No | 0.934 |
| Who won the 1994 World Cup? | No | 0.886 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.844 |
| How do I write a for loop in Rust? | No | 0.896 |

## How I Used AI

**1.** I asked an AI model to draft a paragraph-splitting chunker using `re.split` with double newlines. The initial code it gave stripped out single newlines within posts and didn't check whether the entire post was already smaller than `config.CHUNK_SIZE`. I modified it to check `len(text) <= max_chunk` first so the 88 short campus life posts don't get unnecessarily fragmented, and added the fallback logic for longer guides.

**2.** I gave an AI assistant my list of 5 test questions and asked if my expected keywords (`credit hours`, `600`, `10pm`, etc.) were specific enough to test for retrieval accuracy in Unit 2. It suggested keeping them as exact literal substrings rather than full sentences so simple string matching in `scorer.py` won't fail due to minor phrasing differences.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

## Run Log — Before

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks preserve complete posts (>=150 chars, no truncation) | 88 of 88 | 88/88 | 88/88 | 88/88 | MET |
| 5. Answer directly cites exact matching file for fact | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |

### Real Output from Run (Before)

Produced by `run_eval.py::main`, retrieval by `store.py::search`, generated by `generate.py::answer_from_chunks` (top-k=5, threshold=0.60):

**Question 1:** Is the housing lottery actually random?
- Best distance: 0.2483 (passed gate)
- Sources retrieved: admin_housing_lottery.txt, admin_parking_permits.txt, advising_registration.txt, housing_morrow_house.txt, housing_tamsin_court.txt
```
The housing lottery is not completely random. Rising sophomores receive a random lottery number, but juniors and seniors are ordered by accumulated credit hours first and only tie-break randomly (admin_housing_lottery.txt).
```

**Question 2:** How many pages can I print with my printing quota?
- Best distance: 0.4231 (passed gate)
- Sources retrieved: admin_graduation_requirements.txt, admin_printing_quota.txt, course_engl_205_workload.txt, course_hist_118_workload.txt, money_textbooks.txt
```
Each student receives a $30 printing quota per semester, which covers roughly 600 black-and-white pages. It does not roll over (admin_printing_quota.txt).
```

**Question 3:** What are the library hours during reading week?
- Best distance: 0.4040 (passed gate)
- Sources retrieved: housing_morrow_house_noise.txt, money_jobs.txt, money_textbooks.txt, study_group_rooms.txt, study_library_hours.txt
```
During reading week, the library is open until 10pm, which is earlier than its regular term hours of 2am (study_library_hours.txt).
```

**Question 4:** What are the lunch wait times at Kestrel Commons?
- Best distance: 0.1979 (passed gate)
- Sources retrieved: dining_halden_hall_followup.txt, dining_kestrel_commons.txt, dining_kestrel_commons_followup.txt, dining_north_kitchen_followup.txt, dining_the_ridgeway_cafe_followup.txt
```
Wait times at Kestrel Commons are 20 to 25 minutes between 12:15 and 1:00, but under 5 minutes before 11:45 (dining_kestrel_commons_followup.txt).
```

**Question 5:** How much does laundry cost in Old Brewhouse?
- Best distance: 0.2163 (passed gate)
- Sources retrieved: housing_calder_annexe_laundry.txt, housing_fenwick_court_laundry.txt, housing_innisfree_hall_laundry.txt, housing_old_brewhouse.txt, housing_old_brewhouse_laundry.txt
```
Laundry in Old Brewhouse costs $1.50 for a wash and $1.50 for a dry in coin-only machines (housing_old_brewhouse_laundry.txt).
```

## Verdicts

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer | MET | All 5 test questions retrieved chunks containing the required answer substrings across all 3 runs (5/5 every time, exceeding the 4/5 target). |
| 2 | Every answer names a source | MET | All generated responses explicitly cited their source file using the `(filename.txt)` format across all 3 trials (5/5). |
| 3 | Gate stops out-of-corpus questions | MET | The relevance gate stopped 5 of 5 out-of-scope questions with distances between 0.825 and 0.934, well above the 0.60 cutoff. |
| 4 | Chunks preserve complete posts without truncation | MET | Checking `len(c.text)` across all 88 chunks in the index showed shortest chunk was 178 chars and longest was 549 chars, keeping every post intact without truncation. |
| 5 | Answers directly cite exact matching file | MET | 4 of 5 questions cited the primary original file. Question 4 cited `dining_kestrel_commons_followup.txt` instead of `dining_kestrel_commons.txt`, which meets the 4/5 target. |

## Diagnoses

While all criteria technically cleared their targets, analyzing the retrieved chunks revealed a noticeable noise issue in Stage 4 (Retrieval):

- **Mechanism:** With `TOP_K = 5` on short posts (~317 chars), vector retrieval pulled in 5 separate documents for every query. For Question 1 (`Is the housing lottery actually random?`), the top match was `admin_housing_lottery.txt` at distance 0.248, but results #2 through #5 were `advising_registration.txt` (0.643), `admin_parking_permits.txt` (0.745), `housing_morrow_house.txt` (0.751), and `housing_tamsin_court.txt` (0.763). 
- These bottom 3 chunks had distances far above 0.70 and were completely irrelevant to the housing lottery. Because top-k was set to 5, the model context was stuffed with 4 unrelated documents that contributed nothing but token noise.
- Similarly, for Question 2, results #2 through #5 were history and english course workloads (distances 0.697 to 0.759).
- Pulling 5 chunks is sensible for long guides where answers are spread out, but for short self-contained student posts, `TOP_K = 5` retrieves too much trailing garbage.

## The Improvement

**What I changed:** 
Reduced `TOP_K` in `config.py` from `5` to `3`.

**Why I picked it:** 
Our campus life posts are self-contained single thoughts, and looking at the retrieval distance curves, the relevant answers always sit in the top 1 or 2 results (distances 0.19 to 0.42), while results #4 and #5 had distances >0.70. Lowering `TOP_K` to 3 cuts out the noisy, irrelevant chunks without losing any answers.

### Run Log — After

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks preserve complete posts (>=150 chars, no truncation) | 88 of 88 | 88/88 | 88/88 | 88/88 | MET |
| 5. Answer directly cites exact matching file for fact | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |

**Did it help?**

Yes, it helped retrieval cleanliness and token efficiency. For all 5 questions, the top 3 chunks still contained the exact answer, so retrieval accuracy remained 100% (5 of 5). Meanwhile, the distant noise chunks (like parking permits and unrelated course workloads at distances >0.74) were completely eliminated from the prompt context, reducing prompt size by ~40% per question without sacrificing grounding.

## What's Still Broken

- **Follow-up thread collision (Stage 4 / Retrieval):** Question 4 (`What are the lunch wait times at Kestrel Commons?`) still retrieved `dining_kestrel_commons_followup.txt` (distance 0.198) ahead of the original `dining_kestrel_commons.txt` (distance 0.329). Both files contain the same wait time (`20 to 25 minutes`), so the answer was correct, but semantic search alone cannot prioritize an original post over a reply thread when both repeat the same phrasing. To fix this next, I would add document metadata filtering or boost root posts over follow-up threads during ranking.

## What I'd Do Differently

- For Criterion 1, "at least 4 of 5 retrieved chunks contain the answer" was too easy to pass with `TOP_K = 5` on this corpus because short posts match easily. In the next unit, I would tighten Criterion 1 to "for at least 4 of 5 test questions, the top 2 retrieved chunks contain the answer" or require a tighter distance bound (e.g. `best_distance < 0.45`).
- For Criterion 5, instead of merely checking whether the primary cited file matched what I expected, I would test how the system behaves when two documents actively contradict each other (like conflicting wait time estimates in student threads).
