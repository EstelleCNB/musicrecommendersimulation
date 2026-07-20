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

The UserProfile holds a user's taste in four fields: their favorite genre, their favorite mood, a target energy level (from 0.0 for calm to 1.0 for intense), and a likes_acoustic flag. One thing to note is that likes_acoustic is stored but the scorer never actually reads it, so it doesn't affect the results at the moment.

How does your Recommender compute a score for each song
For each song, the scorer adds up points across three things. If the song's genre matches the user's favorite genre, it adds 2.0 points, and if the mood matches, it adds 1.5. For energy, it measures how close the song's energy is to the user's target using 1 - abs(gap), then multiplies that by a weight of 3.0. So the closer the energy, the more points it earns. All three parts are added together into one final score, and the code also builds a short list of reasons explaining which features matched.

How do you choose which songs to recommend
I score every song in the catalog, then sort them from highest score to lowest and keep the top few. By default it returns the top 5. Each recommendation comes back with its score and a plain-language explanation of why it was picked, so the user can see what the song matched on.

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

====


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
====================================================================================================== test session starts ======================================================================================================
platform darwin -- Python 3.13.7, pytest-9.1.1, pluggy-1.6.0 -- /opt/anaconda3/envs/opencv-env/bin/python
cachedir: .pytest_cache
rootdir: /Users/caitlynbennett/ai_engineering1101/musicrecommendersimulation/musicrecommendersimulation
collected 2 items                                                                                                                                                                                                               

tests/test_recommender.py::test_recommend_returns_songs_sorted_by_score PASSED                                                                                                                                            [ 50%]
tests/test_recommender.py::test_explain_recommendation_returns_non_empty_string PASSED                                                                                                                                    [100%]

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:



============================================================
(opencv-env) caitlynbennett@Estelles-MacBook-Pro musicrecommendersimulation % python src/main.py
Loaded songs: 18

============================================================
           TOP RECOMMENDATIONS — High-Energy Pop            
============================================================

1. Sunrise City — Neon Echo
   Score: 8.02
   Reasons:
     • genre match: pop (+1.0)
     • mood match: happy (+1.5)
     • energy close to your target (+5.5)

2. Gym Hero — Max Pulse
   Score: 6.82
   Reasons:
     • genre match: pop (+1.0)
     • energy close to your target (+5.8)

3. Rooftop Lights — Indigo Parade
   Score: 6.66
   Reasons:
     • mood match: happy (+1.5)
     • energy close to your target (+5.2)

4. Storm Runner — Voltline
   Score: 5.94
   Reasons:
     • energy close to your target (+5.9)

5. Neon Overdrive — Pulsewave
   Score: 5.70
   Reasons:
     • energy close to your target (+5.7)
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

Working on this project made me learn the math behind recommenders. Each song is broken down into numbers and labels, like genre, mood, and energy, and the system scores how well each one lines up with what the user says they want. The prediction isn't magic. It's just adding up points based on weights I chose, like genre being worth 2 points and energy being worth 3, and then sorting the songs from highest to lowest. What surprised me most is how much those small choices matter. Changing one weight or ignoring one feature completely changes what gets recommended, even though the data itself never changed. So a lot of the "intelligence" is really just decisions the designer made about what counts as important.

I also learned that bias and unfairness can sneak in really easily, usually without anyone meaning for it to happen. In my system, the dataset was uneven, since some genres had several songs and others had only one, so users with popular tastes got lots of good options while niche listeners barely had any real choices. The scoring can be unfair too. Because energy is weighted so heavily, it can outweigh a perfect genre match, and preferences like likes_acoustic get ignored entirely(which that is my fault), so certain users are basically invisible to the system. This made me understand that fairness in these systems depends just as much on the data you feed in and the weights you pick as it does on the code itself.



