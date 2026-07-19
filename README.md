# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.
My version of recommendations will be based off of penalizing the distance from preference. It rewards closeness in either direction, so if a song is too energetic, or too mellow, then it will get penalized. This will be effi

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

The system scores every song against a user's taste profile, then ranks them.
It has two distinct rules:

- **Scoring rule** (`score_song`) — measures how well *one* song matches the user.
- **Ranking rule** (`recommend_songs`) — sorts all scored songs and returns the top *k*.

### Scoring Formula

- **Categorical features:** exact match earns the feature's full weight, else 0.
- **Numerical features:** closeness = `1 - abs(song_value - target_value)`,
  scaled by the feature's weight. A perfect match scores 1.0, opposite values 0.0.
- **Total score:** the weighted sum across all features. Optionally divided by the
  sum of weights to produce a 0–100% match.

### Pipeline

1. `load_songs` — read the CSV, casting numeric columns to floats.
2. `score_song` — compute a weighted match score + reasons for one song.
3. `recommend_songs` — score all songs, sort by score, return the top *k*
   with explanations.

### Known Biases

- **Exact-match bias** — only identical genre/mood labels score; near-cousins like
  "indie pop" vs "pop" get no credit.
- **Feature-weight bias** — the designer's default weights impose one taste on all users.
- **Ignored features** — `tempo_bpm` is never scored, a silent blind spot.
- **Filter bubble** — rewarding closeness to stated taste means no discovery or diversity.
- **Small/uneven catalog** — genres with more songs are more likely to appear in results.
- **Cold start** — scores rely on a stated profile, never on actual listening history.

You can include a simple diagram or bullet list if helpful.

==========Sample Recommendation Output=======
                    TOP RECOMMENDATIONS                     
============================================================

1. Focus Flow — LoRoom
   Score: 6.50
   Reasons:
     • genre match: lofi (+2.0)
     • mood match: focused (+1.5)
     • energy close to your target (+3.0)

2. Midnight Coding — LoRoom
   Score: 4.94
   Reasons:
     • genre match: lofi (+2.0)
     • energy close to your target (+2.9)

3. Library Rain — Paper Lanterns
   Score: 4.85
   Reasons:
     • genre match: lofi (+2.0)
     • energy close to your target (+2.8)

4. Coffee Shop Stories — Slow Stereo
   Score: 2.91
   Reasons:
     • energy close to your target (+2.9)

5. Paper Boats — Wren & Willow
   Score: 2.79
   Reasons:
     • energy close to your target (+2.8)

============================================================
---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



