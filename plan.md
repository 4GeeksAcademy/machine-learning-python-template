# Plan — Sentiment Analysis on Customer Reviews (WeLoveReviews)

Small steps to learn by doing. Finish each step's **Check** before you move on, and tick the boxes (`[x]`) as you go.

**The question in one sentence:** the client has a 4.5 / 5 star average. Does the *text* of its 500 reviews read as positive as that number suggests? If not, why not?

**What this project is NOT:** you do not train or fine-tune a model. You *integrate* an existing Hugging Face model, check its output against reality, and explain where it goes wrong.

---

## Before Step 1: understand the project

Do these before you write any code. Write your answers in a notebook or a scratch file, in your own words.

- [x] **Step A — Retell the story.** Read "Your challenge" on the assignment page. Answer:
  - Who is the client? *(WeLoveReviews, a company that analyses reviews for businesses)*
  - Who is *their* client? *(a café, Harbor House Café, with a 4.5-star average)*
  - What does the account manager want, in one sentence? *(how many of the 500 reviews read positive / neutral / negative, and whether that matches 4.5 stars)*
  - *Check:* you can explain the project to a friend in 30 seconds.

- [x] **Step B — Understand why a model is needed at all.** The star rating already exists, so why read the text? Because a person can give 5 stars and still complain in the text. The project measures what people *wrote*, not what they *clicked*.
  - *Check:* you can give one example of a review where the text and the stars disagree.

- [x] **Step C — Understand the model's job and its weakness.** Read "Model note" on the assignment page and the model card linked below.
  - Input: one review's text. Output: a guess of 1–5 stars plus a confidence score.
  - Weakness: it learned from **product** reviews ("battery died", "wrong size"). Your reviews are about **service** ("waited 20 minutes", "friendly staff"). It will misread some of them.
  - The project *expects* the model to make mistakes. Finding and explaining them is the assignment, not a failure.
  - *Check:* you can explain what a "false negative" means here (see the Glossary).

- [x] **Step D — Map the deliverables.** Look at the "Expected file layout" table below and answer: which file tells the *story*, and which one *does the work*?
  - `src/explore.ipynb` is the report: a reader follows it from question → data → model → results → conclusions.
  - `src/app.py` is the production script: it runs the model on all reviews and saves a CSV. No analysis.
  - `data/processed/reviews_with_sentiment.csv` is the output that `app.py` writes.
  - *Check:* you can draw the "Data flow" diagram from memory.

- [x] **Step E — Read the grading list.** Read "What We Will Evaluate" on the assignment page and the "Rules you will be graded on" below. For each rule, write *why* it exists:
  - Load the model once → loading takes seconds and lots of memory, and doing it 500 times is wasteful.
  - Pin the model name and package versions → results stay reproducible for whoever runs it next.
  - Don't commit weights → they are hundreds of MB and Hugging Face already hosts them.
  - Check by hand → models are confidently wrong sometimes, and you have to prove you looked.

- [x] **Step F — Skim the reference solution once.** Open the solution link below. Don't copy it. Notice its shape: the notebook sections, the `app.py` functions, the false-negative patterns table. Then close it and work from this plan.

- [x] **Step G — Check your knowledge.** Go through the "Knowledge you need" table below. For any row you can't do yet, spend 15–30 minutes on it before Step 1.

### Knowledge you need

| Topic | What you should be able to do | Where you use it |
| --- | --- | --- |
| **Python basics** | functions, `if`/`else`, list comprehensions, `str.split()`, `int()` | `stars_to_sentiment`, parsing `"4 stars"` |
| **Virtual environments & pip** | create a venv, `pip install`, `pip freeze`, pin with `==` | Steps 2–3 |
| **Jupyter notebooks** | code vs markdown cells, run all, restart kernel | the whole `explore.ipynb` |
| **pandas** | `read_csv`, `.shape`, `.info()`, `.isna()`, `.value_counts()`, `.mean()`, boolean filtering `df[(a) & (b)]`, `pd.crosstab`, `to_csv` | EDA, breakdown, false negatives |
| **matplotlib / seaborn** | bar chart, heatmap | breakdown and crosstab plots |
| **What a pretrained model is** | know the difference between *training* (learning weights) and *inference* (using them) | you only do inference |
| **Hugging Face `transformers`** | `pipeline("text-classification", model=...)`, read the output `{'label', 'score'}` | Steps 4, 15–16 |
| **Tokens & truncation** | know that BERT reads at most 512 tokens and longer text is cut off | `truncation=True` |
| **Classification evaluation (light)** | what agreement, false positive and false negative mean, and how to read a confusion matrix (crosstab) | Steps 18–20 |
| **Domain shift** | know why a model trained on one kind of text performs worse on another | Steps 13, 20, 22 |
| **Writing for non-technical readers** | plain-language summary with numbers and a recommendation | Step 22 |
| **Scripts vs notebooks** | `if __name__ == "__main__":`, relative paths, running from the repo root | `src/app.py` |
| **Git & GitHub** | `add`, `commit`, `push`, `.gitignore` | Steps 5, 28 |

You do **not** need: neural network math, training loops, fine-tuning, GPUs, or a database.

---

## Reference (keep this open)

### Sources
- Assignment: 4Geeks page "Sentiment Analysis on Customer Reviews — WeLoveReviews" (22 tasks)
- Reference solution: https://github.com/4GeeksAcademy/ai-engineering-syllabus/blob/main/content/projects/existing-model-sentiment-analysis-reviews/.learn/solution/README.md
- Model card: https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment
- Optional model: https://huggingface.co/tabularisai/multilingual-sentiment-analysis
- `transformers` pipeline docs: https://huggingface.co/docs/transformers/main_classes/pipelines

### Expected file layout
| File | Purpose |
| --- | --- |
| `requirements.txt` | Pinned dependencies (template + `transformers` + `torch`) |
| `data/raw/reviews.csv` | Input: 500 reviews (`review_id`, `rating`, `review_text`) |
| `src/explore.ipynb` | The story: an executed notebook **with outputs** |
| `src/app.py` | Production inference script |
| `data/processed/reviews_with_sentiment.csv` | Enriched output |
| `PROMPT.md` | Provided EDA prompt |

### Data flow
```
data/raw/reviews.csv ──► src/explore.ipynb  (story: EDA, results, false negatives, conclusions)
          │                     │ migrate the clean inference logic
          └────────────────────► src/app.py ◄── Hugging Face cache (~/.cache/huggingface)
                                    │
                                    ▼
                 data/processed/reviews_with_sentiment.csv
```

### Model facts
- Pinned model: `MODEL_NAME = "nlptown/bert-base-multilingual-uncased-sentiment"`
- Output: labels `"1 star"` … `"5 stars"` plus a `score` (confidence)
- Trained on **product** reviews (Amazon-style). Your data is **service** reviews (a café). This mismatch is the main thing the project teaches.

### Star → band mapping
| Model prediction | Sentiment band |
| --- | --- |
| 1–2 stars | NEGATIVE |
| 3 stars | NEUTRAL |
| 4–5 stars | POSITIVE |

### Rules you will be graded on
1. Load the model with `pipeline()` or `from_pretrained()`. Never commit weights to the repo.
2. Load the model **once**, before the loop. Never inside the per-review loop.
3. Pin the model name as a constant, not "latest".
4. Every one of the 500 reviews gets a prediction.
5. The notebook carries the story. `app.py` only runs production inference.
6. No separate client report. The notebook is the report.

---

## Steps

Steps 6–23 go in **`src/explore.ipynb`**, in order, with short markdown between code cells. Imagine your account manager reading it top to bottom.

- [x] **Step 1 — Look at the raw data by eye.** Open `data/raw/reviews.csv` and read 10 reviews.
  - *Learn:* before any code, get a feel for the data. Do the 5-star reviews ever mention complaints?
  - *Check:* you can name the 3 columns and guess roughly what share of ratings are 5s.
  - *Done:* found reviews **17** (★4, "polite but a bit slow… Five stars") and **22** (★5, "waited 25 minutes just to get water"). Reuse them in Steps 19 and 21.

- [x] **Step 2 — Create a virtual environment.** *(commands are for Git Bash)*
  ```bash
  py -V:Astral/CPython3.12.14 -m venv /c/venvs/wlr
  source /c/venvs/wlr/Scripts/activate
  python -m pip install --upgrade pip
  pip install -r requirements.txt
  ```
  - *Why outside the repo:* a `.venv` inside this folder fails with `WinError 206: filename too long`. The repo path is ~185 chars and Windows limits paths to 260.
  - *Why 3.12:* `torch` may have no build for Python 3.14 yet. `py -0` lists installed Pythons. The 3.12 one was installed by uv, so its tag is `Astral/CPython3.12.14`.
  - *Check:* `python -c "import pandas; print(pandas.__version__)"` works (3.1.0).

- [x] **Step 3 — Install the model libraries and pin them.**
  ```bash
  pip install transformers torch
  pip freeze
  ```
  Replace every line in `requirements.txt` with its exact `pip freeze` version, plus `torch` and `transformers`.
  - *Assignment requirement:* "Dependencies are pinned in `requirements.txt`."
  - *Learn:* why pin? So someone who clones the repo in a year gets the same behaviour you did.
  - *Check:* every line in `requirements.txt` uses `==` (done: `torch==2.15.0`, `transformers==5.22.1`).

- [ ] **Step 4 — Smoke-test the model in a Python shell.** *(Skipped. It's a plan suggestion, not an assignment requirement; the model downloads at Step 15 instead. The interactive `python` prompt freezes in Git Bash, so use a heredoc `python - <<'EOF' … EOF` or `winpty python` if you try it.)*
  ```python
  from transformers import pipeline
  clf = pipeline("text-classification", model="nlptown/bert-base-multilingual-uncased-sentiment")
  clf("The coffee was great but we waited 25 minutes.")
  ```
  - *Learn:* the first run downloads the weights to `~/.cache/huggingface`. Later runs reuse them. That cache is outside your repo, which is why you never commit weights.
  - *Check:* you see something like `[{'label': '3 stars', 'score': 0.4...}]`. Try 3–4 sentences of your own. Which ones does it get "wrong"?

- [x] **Step 5 — Make sure `.gitignore` keeps junk out.** Add `.venv/` and `.ipynb_checkpoints/` if they are missing.
  - Committed as `2622cea` together with the pinned `requirements.txt`.

- [x] **Step 5b — Connect the notebook to the venv.**
  - Install the VS Code **Jupyter** extension (by Microsoft): `code --install-extension ms-toolsai.jupyter`. Without it, *Select Kernel* shows nothing.
  - In the venv: `pip install ipykernel` (pinned in `requirements.txt` as `ipykernel==7.4.0`).
  - VS Code doesn't scan `C:\venvs` by default, so `wlr` was missing from the list. Fix: add `"python.venvPath": "C:\\venvs"` to the VS Code **user** settings (not the repo's `.vscode/settings.json`, which is committed).
  - Reload VS Code (Ctrl+Shift+P → *Developer: Reload Window*), open `src/explore.ipynb` → *Select Kernel* → *Python Environments* → `wlr`.
  - *Pitfall:* typing a path into the *Select Kernel* search box and pressing Enter runs "Create Python Environment". The box only filters the list.
  - *Check:* a cell with `import pandas; pandas.__version__` shows `'3.1.0'` ✔.

- [x] **Step 6 — Title + Objectives markdown cell** at the very top of the notebook:
  - the business question (written sentiment vs the 4.5-star average)
  - what you will deliver (a sentiment breakdown, a comparison with the rating, false-negative analysis, a manual check, conclusions)
  - the constraint: an existing model, no training
  - *Check:* someone who never saw the assignment understands the goal from this cell alone.

- [x] **Step 7 — Run `PROMPT.md`.** Paste everything below its `---` line into your coding agent. It should fill the EDA section only.

- [x] **Step 8 — Read and understand every EDA cell.** For each one, write down what question it answers:
  - shape, dtypes, missing values
  - rating distribution (`df["rating"].value_counts()`) and **mean rating**
  - text length stats (characters/words). Very long reviews matter because BERT truncates at 512 tokens.
  - a few sample texts per rating

- [x] **Step 9 — Check the mean rating yourself:** `df["rating"].mean()`. Is it ≈ 4.5?

- [x] **Step 10 — Write the insights cell** (3–5 bullets). Example: *"Most ratings are 5, but several 5-star reviews mention waits or staff attitude, so the model may read those as negative."*

- [x] **Step 11 — Cleaning decision cell.** Say what you clean (strip whitespace, drop empty or duplicate texts) or why nothing is needed.
  - *Check:* you still have 500 rows. If you dropped any, explain why.

- [x] **Step 12 — Markdown cell "Action plan":** load the model → predict stars for all 500 → map to bands → compare with ratings → hunt for false negatives → check by hand → conclude.

- [x] **Step 13 — Markdown cell "Why this model":** `nlptown` is fixed by the client brief. It outputs 1–5 stars. Note the domain-mismatch risk up front (product vs service reviews). Paste the star → band table.

- [x] **Step 14 — Code cell: pin the model and the mapping.**
  ```python
  MODEL_NAME = "nlptown/bert-base-multilingual-uncased-sentiment"

  def stars_to_sentiment(label: str) -> str:
      star = int(str(label).split()[0])   # "4 stars" -> 4
      if star <= 2:
          return "NEGATIVE"
      if star == 3:
          return "NEUTRAL"
      return "POSITIVE"
  ```
  - *Check:* `stars_to_sentiment("1 star")` gives `NEGATIVE` and `stars_to_sentiment("5 stars")` gives `POSITIVE`.

- [x] **Step 15 — Load the model ONCE in its own cell.**
  ```python
  from transformers import pipeline
  classifier = pipeline("text-classification", model=MODEL_NAME)
  ```

- [x] **Step 16 — Run inference on all 500 reviews in a separate cell.** Add 3 columns: `predicted_stars`, `predicted_sentiment`, `confidence`.
  ```python
  results = classifier(df["review_text"].tolist(), truncation=True, batch_size=16)
  df["predicted_stars"] = [int(r["label"].split()[0]) for r in results]
  df["predicted_sentiment"] = [stars_to_sentiment(r["label"]) for r in results]
  df["confidence"] = [round(r["score"], 4) for r in results]
  ```
  - *Learn:* passing a list lets the pipeline batch the reviews, which is faster than a Python loop and still uses the one loaded model. `truncation=True` protects against texts longer than 512 tokens.
  - *Check:* `df["predicted_stars"].isna().sum() == 0` and `len(df) == 500`.

- [x] **Step 17 — Sentiment breakdown.**
  ```python
  df["predicted_sentiment"].value_counts(normalize=True).mul(100).round(1)
  ```
  Plot it as a bar chart.

- [x] **Step 18 — Compare with the 4.5-star average.**
  - human mean rating vs model mean `predicted_stars`
  - map the *human* ratings to bands with the same rule, then put human % and model % side by side
  - a crosstab: `pd.crosstab(df["rating"], df["predicted_stars"])`, plotted as a heatmap
  - *Learn:* the crosstab diagonal shows agreement. The cells for rating 4–5 vs predicted 1–2 are your false negatives.
  - Markdown: in plain words, where is the gap?

- [x] **Step 19 — Find the false negatives.**
  ```python
  false_negatives = df[(df["rating"] >= 4) & (df["predicted_stars"] <= 2)]
  ```
  - count them and show them as a % of all reviews
  - list them with `review_id`, `rating`, `predicted_stars`, text, and a one-line reason for each

- [x] **Step 20 — Group the false negatives into patterns.** The solution's patterns are below; check which ones appear in *your* data.

  | Pattern | Example | Why the model fails |
  | --- | --- | --- |
  | Mixed sentiment | "staff seemed annoyed… food made up for it" | Product models weight complaint phrases heavily |
  | Service complaint inside a positive review | "waited 25 minutes for water, but food was great" | Wait-time language reads as negative |
  | Backhanded compliment | "polite but a bit slow, overall solid" | Qualifiers like "slow" or "average" dominate |
  | Domain vocabulary | "server", "brunch", "ambiance" | The training data was about product attributes |

  Markdown: write your **hypothesis** of why a product-review model misreads service-review text.

- [x] **Step 21 — Manual sample (15–20 reviews).** Pick a mix: some false negatives, some agreements, some 3-star ratings. Read each one yourself and fill in a table:

  | review_id | rating | text (truncated) | predicted_stars | manual_sentiment | match? | notes |
  | --- | --- | --- | --- | --- | --- | --- |

  Build it as a DataFrame with a `manual_sentiment` / `notes` list that you type by hand, then display it.
  - *Learn:* this is your evidence that you did not trust the model blindly.
  - *Check:* at least 15 rows, and each mismatch has a note.

- [x] **Step 22 — Conclusions markdown**, written for the account manager (no jargon):
  - X % positive / Y % neutral / Z % negative according to the model
  - does that line up with 4.5 stars? Where does the gap come from: real dissatisfaction, or the model misreading service language?
  - a recommendation, e.g. "the model under-counts positivity; don't put the raw negative % in front of the client without manual review" or "consider a better-fitting model" (see Step 31)

- [x] **Step 23 — Restart & Run All.** The notebook must run top to bottom with saved outputs.
  - *Check:* no error cells, and every chart and table is visible on GitHub.

- [x] **Step 24 — Remove the template's DB code from `src/app.py`.** The template's `from utils import db_connect` needs a `DATABASE_URL`, and this project has no database.

- [x] **Step 25 — Write the functions in `src/app.py`.** Move the logic over from the notebook. This file does inference only, with no analysis.

  | Function / constant | Role |
  | --- | --- |
  | `MODEL_NAME` | Pinned model id |
  | `stars_to_sentiment(label)` | `"N stars"` → band |
  | `load_reviews(path="data/raw/reviews.csv")` | Read the CSV |
  | `run_inference(df, classifier)` | Add `predicted_stars`, `predicted_sentiment`, `confidence` |
  | `write_output(df, path="data/processed/reviews_with_sentiment.csv")` | Save the CSV |
  | `main()` | Load the model once → infer all → write → print the breakdown |

  Finish with `if __name__ == "__main__": main()`.
  - *Learn:* paths are relative to the repo root, so run the script from the root.

- [x] **Step 26 — Run it:** `python src/app.py`
  - *Check:* `data/processed/reviews_with_sentiment.csv` exists with 500 rows and columns
    `review_id,rating,review_text,predicted_stars,predicted_sentiment,confidence`, and the terminal prints counts and percentages.
  - *Check:* the numbers match your notebook.

  Expected output looks roughly like this (the solution's indicative numbers; yours may differ):
  ```
  Total reviews analyzed: 500
  Mean star rating: 4.48 / 5
  Sentiment breakdown (from nlptown model):
    POSITIVE: 378 (75.6%)
    NEUTRAL:   62 (12.4%)
    NEGATIVE:  60 (12.0%)
  ```

- [x] **Step 27 — Final checklist** (mirrors "What We Will Evaluate"):
  - [x] `src/explore.ipynb` has executed outputs and the full arc: objectives → EDA → cleaning → plan/model → results → conclusions
  - [x] short transitional markdown between code blocks
  - [x] model loaded via `pipeline()` / `from_pretrained()`, with no weights in the repo
  - [x] `MODEL_NAME` pinned
  - [x] model loaded once and reused
  - [x] all 500 reviews have stars + a band
  - [x] breakdown % calculated and explicitly compared with 4.5 stars
  - [x] false negatives documented, with a hypothesis
  - [x] 15–20 manually reviewed examples
  - [x] `src/app.py` runs and writes `data/processed/reviews_with_sentiment.csv`
  - [x] dependencies pinned in `requirements.txt`

- [ ] **Step 28 — Commit and push** the notebook, `app.py`, the processed CSV, `requirements.txt` and `data/raw/reviews.csv`. Submit the repo link.

- [ ] **Step 29 — (Optional) Run a second model.** Run `tabularisai/multilingual-sentiment-analysis` on the same 500 reviews. It outputs Very Negative … Very Positive directly. Collapse those into 3 bands for a fair comparison.

- [ ] **Step 30 — (Optional) Compare the two models.** Put the false-negative counts side by side. Which reviews fail under **both** models? Those probably need a human regardless.

- [ ] **Step 31 — (Optional) Write a recommendation.** Add an addendum at the end of `src/explore.ipynb`: should WeLoveReviews switch models for this client, and why?

---

## Glossary
- **Pretrained model:** a model someone else already trained. You only run it (this is called inference).
- **Pipeline:** the `transformers` helper that bundles tokenizer + model + post-processing into one call.
- **Tokenizer / truncation:** text is split into tokens, and BERT reads at most 512 of them. Longer text gets cut off.
- **Domain mismatch:** the model learned on one kind of text (product reviews) and is used on another (service reviews), so accuracy drops.
- **False negative (in this project):** the human says positive (rating 4–5), but the model says negative (1–2 stars).
- **Confidence (`score`):** the model's probability for its chosen label. A high score does not mean the label is correct.
