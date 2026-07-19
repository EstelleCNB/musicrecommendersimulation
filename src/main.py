"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Taste profile
    user_prefs = {
        "favorite_genre": "lofi",        # favorite genre
        "favorite_mood": "focused",      # desired mood
        "target_energy": 0.4,          # target energy (0.0 calm -> 1.0 intense)
        "likes_acoustic": True, # leans toward acoustic textures
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    width = 60
    print()
    print("=" * width)
    print("TOP RECOMMENDATIONS".center(width))
    print("=" * width)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print()
        print(f"{rank}. {song['title']} — {song['artist']}")
        print(f"   Score: {score:.2f}")

        reasons = [r for r in explanation.split("; ") if r]
        if reasons:
            print("   Reasons:")
            for reason in reasons:
                print(f"     • {reason}")
        else:
            print("   Reasons: (no strong matches)")

    print()
    print("=" * width)


if __name__ == "__main__":
    main()
