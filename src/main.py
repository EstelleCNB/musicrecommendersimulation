"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


# Distinct taste profiles to simulate different kinds of listeners.
# Each maps to the keys score_song expects: favorite_genre, favorite_mood,
# target_energy (0.0 calm -> 1.0 intense), and likes_acoustic.
USER_PROFILES = {
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.9,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "focused",
        "target_energy": 0.4,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.95,
        "likes_acoustic": False,
    },

    "Conflicting: hype-sad": {
        "favorite_genre": "rock",
        "favorite_mood": "sad",
        "target_energy": 0.9,
        "likes_acoustic": False,
    },
    "Out-of-range energy": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 2.0,
        "likes_acoustic": False,
    },
    "Unmatchable genre": {
        "favorite_genre": "polka",
        "favorite_mood": "",
        "target_energy": 0.5,
        "likes_acoustic": False,
    },

}


def print_recommendations(profile_name: str, recommendations) -> None:
    width = 60
    print()
    print("=" * width)
    print(f"TOP RECOMMENDATIONS — {profile_name}".center(width))
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


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for profile_name, user_prefs in USER_PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(profile_name, recommendations)


if __name__ == "__main__":
    main()
