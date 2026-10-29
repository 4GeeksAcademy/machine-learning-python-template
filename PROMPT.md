# EDA prompt — WeLoveReviews reviews

Copy everything below this line into your coding agent (Cursor, Copilot, Claude Code, etc.).

---

You are helping an AI engineer explore a customer-reviews dataset before any modeling work.

Context:

- Client: WeLoveReviews / Harbor House Café style service reviews
- Boilerplate: 4GeeksAcademy machine-learning-python-template
- File: `data/raw/reviews.csv` (columns: `review_id`, `rating`, `review_text`)
- Business question (for context only — do not solve the full project): whether written sentiment aligns with a ~4.5 / 5 star average

Your job in the project notebook `src/explore.ipynb`:

1. Explore the dataset (shape, dtypes, missing values, rating distribution, text length stats, a small sample of review texts).
2. Surface the most important insights that would later justify an action plan (keep the insight list short and actionable).
3. Propose cleaning actions only if needed; if none are needed, say why.

Rules:

- Write short markdown between code cells that explains the transition to the next step (tutorial tone, minimal text).
- Do not run sentiment models.
- Do not write or modify `src/app.py`.
- Do not produce a client markdown report.
- Do not claim the full project is done — stop after exploration, insights, and cleaning proposal.
- Keep work in `src/explore.ipynb`.
