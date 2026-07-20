# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

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

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
