# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
!TUNE IN!
---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

The recommender takes a user's taste profile and a catalog of songs, scores every song, and returns the top 5 as a ranked list. Each song gets points for matching the user's favorite genre and mood, plus points for how close its energy is to the user's target energy (recommender.py:81-105). It also comes with a short explanation for each pick, listing which features matched and how many points they added, so the results aren't just a black box. The output is printed to the terminal in a simple ranked format.

What assumptions does it make about the user
It assumes the user can describe their taste with one favorite genre, one favorite mood, and a single target energy level between 0 and 1.

Is this for real users or classroom exploration
This is built for classroom exploration, not real users. It runs from the terminal line using a few hardcoded example profiles and a small 22-song CSV, which is meant for testing and learning rather than serving actual people. And there is no UI, no login, no real music library, and no way for a user to enter their own preferences on the fly. 

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  
Features it does not consider

The model only looks at genre, mood, and energy. It ignores everything else the songs actually carry, like how positive a song feels (valence), its tempo, how danceable it is, and how acoustic it is. I found that it ignores the user's own "likes acoustic" preference, which is collected but never used. So if I have two very different songs, they can look the same to the model as long as they share a genre, mood, and energy level.

Genres or moods that are underrepresented

The catalog is small (18 songs) and lopsided. Lofi shows up three times, but most genres appear only once. Because the model needs an exact genre match to give credit, if the user likes one of those genres that only appears one, then never get a second true match, and their lists get padded with unrelated songs. Moods have the same gap: some moods barely appear, and "sad" isn't in the data at all, so a user wanting sad music gets nothing that fits.

Cases where the system overfits to one preference

The model favors energy very heavily. Matching a user's energy level is worth more than matching their mood, so once a genuinely good matches run out, energy alone decides the rest of the list. In testing, this produced some odd results: a happy pop song was recommended to someone who asked for intense rock, and a "high-energy but sad" request returned five upbeat songs that matched the sad mood on none of them. The list always fills up to five, even when only one or two songs truly fit.

Ways the scoring might unintentionally favor some users

Users whose taste lines up with the well-stocked genres (like lofi or pop) get coherent, satisfying lists. Users who like rare genres, unusual moods, or very high/very low energy get weaker results — sometimes filler, sometimes even negative scores. There's also a subtle ordering bias: when two songs tie, the one listed earlier in the file always wins, so the same songs tend to surface again and again.



---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
There are now 22 songs in the catalog, each with an id, title, artist, genre, mood, and five numeric features (energy, tempo, valence, danceability, and acousticness).
- What genres or moods are represented  
The catalog still spans a wide range of genres such as  pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip hop, classical, reggae, edm, country, r&b, metal, and folk. After the additions, the counts are a bit more balanced: lofi has 4 songs, pop has 3, and rock and r&b now have 2 each, while the rest still have just one. Moods are similar, with chill, happy, and intense at 3 each, relaxed, focused, and romantic at 2 each, and a bunch of others like moody, confident, melancholy, aggressive, and peaceful appearing only once.
- Did you add or remove data  
Yes, I added to it so there is now 22 songs. wirth various categories. 
- Are there parts of musical taste missing in the dataset  
Yes, some gaps are still there. The genre coverage is broad but a lot of genres still only have one song, so niche tastes (like metal or classical) barely have choices. 
---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
It gives reasonable results for high energy pop profiles, so if someone wanted an upbeat pop son, then the system would provide a good match for that.
- Any patterns you think your scoring captures correctly  
The scoring captures exact matches based on mood and genre very well, and because genre carries the highest weight a request for a specific genre would consistently show that genre first. Since energy is handled in the sense of proximity rather than a match, songs that come close to the target still have high value given. 
- Cases where the recommendations matched your intuition  
This case of chill lofi reccomendations matched my intitiion. Bit I would say typically when I run the recommendations, the #1 song almost alwyas matches with what I would've picked. But I do feel like the genre weighting matches with expectations, and the energy is a strong weight that leads the recommendation. 
===========================================================
              TOP RECOMMENDATIONS — Chill Lofi              
============================================================

1. Focus Flow — LoRoom
   Score: 8.50
   Reasons:
     • genre match: lofi (+1.0)
     • mood match: focused (+1.5)
     • energy close to your target (+6.0)

2. Midnight Coding — LoRoom
   Score: 6.88
   Reasons:
     • genre match: lofi (+1.0)
     • energy close to your target (+5.9)

3. Library Rain — Paper Lanterns
   Score: 6.70
   Reasons:
     • genre match: lofi (+1.0)
     • energy close to your target (+5.7)

4. Coffee Shop Stories — Slow Stereo
   Score: 5.82
   Reasons:
     • energy close to your target (+5.8)

5. Paper Boats — Wren & Willow
   Score: 5.58
   Reasons:
     • energy close to your target (+5.6)

==============================================

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  
Features it does not consider

The model only looks at genre, mood, and energy. It ignores everything else the songs actually carry, like how positive a song feels (valence), its tempo, how danceable it is, and how acoustic it is. I found that it ignores the user's own "likes acoustic" preference, which is collected but never used. So if I have two very different songs, they can look the same to the model as long as they share a genre, mood, and energy level.

Genres or moods that are underrepresented

The catalog is small (18 songs) and lopsided. Lofi shows up three times, but most genres appear only once. Because the model needs an exact genre match to give credit, if the user likes one of those genres that only appears one, then never get a second true match, and their lists get padded with unrelated songs. Moods have the same gap: some moods barely appear, and "sad" isn't in the data at all, so a user wanting sad music gets nothing that fits.

Cases where the system overfits to one preference

The model favors energy very heavily. Matching a user's energy level is worth more than matching their mood, so once a genuinely good matches run out, energy alone decides the rest of the list. In testing, this produced some odd results: a happy pop song was recommended to someone who asked for intense rock, and a "high-energy but sad" request returned five upbeat songs that matched the sad mood on none of them. The list always fills up to five, even when only one or two songs truly fit.

Ways the scoring might unintentionally favor some users

Users whose taste lines up with the well-stocked genres (like lofi or pop) get coherent, satisfying lists. Users who like rare genres, unusual moods, or very high/very low energy get weaker results — sometimes filler, sometimes even negative scores. There's also a subtle ordering bias: when two songs tie, the one listed earlier in the file always wins, so the same songs tend to surface again and again.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  
Which user profiles you tested
I tested two kinds of profiles. First, some "normal" ones where the genre, mood, and energy all made sense together and ran them through the CLI to see if the top songs looked right. Then I made some adversarial test  to try and break it: a "hype-sad" profile (high energy but sad), an energy value that was way too high (2.0), a genre that doesn't exist (polka), a genre with the wrong capitalization ("Pop" vs "pop"), a profile missing its energy value, and one that only changed likes_acoustic. The goal was to check both the easy cases and the out of the norm ones.

What you looked for in the recommendations
Mostly I checked that the songs came out sorted by score correctly and that the good profiles put the right genre and mood at the top. In the adversarial tests I also checked the exact scores, so if the math ever changes, a test will fail and tell me instead of the results quietly being wrong. I also made sure the explanations showed up when a song actually matched, and were empty when nothing matched, since the CLI prints "(no strong matches)" in that case.

What surprised you
I was surprised that when energy is weighted so high (3.0) that a good energy match can beat a full genre match, which I didn't mean to happen. 

Any simple tests or comparisons you ran
I kept the tests small so it was easy to tell what the right answer should be usually just two songs where I already knew which one should win. 
I also did some direct comparisons to test one thing at a time, like scoring the same song with likes_acoustic on and off to prove it makes no difference, and comparing a genre-only match against an energy-only match to show energy wins. I checked ties too, and confirmed that a profile missing its energy value throws an error instead of silently breaking. All of these run with pytest so I can re-check them anytime.



---

## 8. Future Work  

Ideas for how you would improve the model next.  

Better ways to explain recommendations
Right now the explanations just list which features matched and how many points they added. It'd be nicer for the user to see why a song ranked where it did compared to the others, like "this was your #1 because it matched on all three things." 

Improving diversity among the top results
Because the top 5 is just the 5 highest scores, you can end up with a bunch of very similar songs. Something that I would change fix would be to make sure the top results include some variety, like not showing five songs from the same genre or artist. I could also add a little randomness so you don't get the exact same list every single time. Fixing the uneven dataset would help too, since some genres only have one song and others have several.

Handling more complex user tastes
It would be nice to let users list a few genres or moods they like, maybe with weights so their favorite counts more. It could also handle "conflicting" tastes better becuase right now something like "high energy but sad" gets full points on both without noticing they don't really go together.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
The biggest thing I learned is that a recommender is really just a scoring formula, and how to create a fair scoring algorithm, though I don't think I did the best for this one. For example, deciding that energy is worth 3 points and genre is only worth 2 completely changes what shows up at the top, and I didn't realize energy would end up outweighing a full genre match until I tested it. 

- Something unexpected or interesting you discovered
I think something unexpected was having an enitre preference like_acoustic being collected but not used, I didn't realize that until the test and until I asked my AI agent what some discrepancies were with my model, I was not thinking that I left out an entire preference.
- How this changed the way you think about music recommendation apps  
Now when apps like Spotify recommend me something, I think about the fact that there's a scoring system behind it making trade-offs I can't see. I also get why my recommendations sometimes feel repetitive or off, the system is may be leaning too hard on one feature. 
