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
The campus_life corpus documents are short posts (~317 chars average) where key facts like numbers or specific rules are usually stated in just one sentence. 4 of 5 gives some room for error because phrasing differences between the question and the post might cause semantic retrieval to rank a general document above the exact specific one.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
Every document in the campus_life corpus is passed into the prompt with its filename header `[from ...]`, and the system instruction explicitly demands citing the file. Since top-k provides at least one retrieved document when the gate passes, every generated answer should cite at least one source document.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

**Why this target:**
The distances for unrelated out-of-scope questions sit between 0.82 and 0.94, while relevant questions match at distances below 0.43. Setting the cutoff in that gap (around 0.55-0.60) should cleanly reject all 5, but I set the target to 4 of 5 in case one random general question happens to share accidental keyword overlap with a course syllabus.

---

## 4. Chunks preserve complete posts without truncation

Across all indexed chunks in campus_life, 100% of chunks (88 of 88) have a character length greater than or equal to 150 characters, and no post is broken across a chunk boundary.

**Why this target:**
When inspecting the campus_life documents, every file is an individual self-contained student tip between 178 and 549 characters. If chunks are set to fixed arbitrary windows like 800 or 200 without checking boundaries, sentences get cut in half or documents get chopped into tiny fragments. In this corpus, keeping each post intact as a single chunk guarantees every chunk holds a complete thought.

---

## 5. Answers directly cite the exact matching file for specific facts

For at least 4 of my 5 test questions, the primary source cited in the answer matches the exact document where the factual answer originated.

**Why this target:**
In a vector search with top-k=5, multiple loosely related documents (like follow-up threads or general dorm tips) get retrieved alongside the correct file. It is not enough for an answer to just invent or cite any random retrieved document; it needs to specifically attribute the fact to the real file that contained it. 4 of 5 is realistic because follow-up posts in campus_life sometimes touch on similar keywords.



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
