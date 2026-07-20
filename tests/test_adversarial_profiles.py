"""
Adversarial / edge-case tests for the functional scorer in src/recommender.py
(score_song and recommend_songs).

These tests PIN CURRENT BEHAVIOR. Several of them document behavior that is
arguably a bug (negative scores, case-sensitivity, a dead preference field).
The point is that if any of these behaviors change later, a test turns red and
tells you — so nothing shifts silently. Where a test documents a questionable
behavior, the comment says so.
"""

from src.recommender import score_song, recommend_songs


def make_song(**overrides):
    """A valid song dict with sensible defaults; override only what a test cares about."""
    song = {
        "id": 1,
        "title": "Test Song",
        "artist": "Test Artist",
        "genre": "pop",
        "mood": "happy",
        "energy": 0.5,
        "tempo_bpm": 120.0,
        "valence": 0.5,
        "danceability": 0.5,
        "acousticness": 0.5,
    }
    song.update(overrides)
    return song


# ---------------------------------------------------------------------------
# 1. Conflicting preferences are NOT penalized (features scored independently)
# ---------------------------------------------------------------------------
def test_conflicting_mood_and_energy_are_scored_independently():
    # User wants high energy (0.9) AND a "sad" mood — semantically in tension.
    prefs = {"favorite_genre": "rock", "favorite_mood": "sad", "target_energy": 0.9}
    # A loud, high-energy song that merely carries the tag mood="sad".
    song = make_song(genre="rock", mood="sad", energy=0.9)

    score, reasons = score_song(prefs, song)

    # It gets FULL credit on all three axes even though "loud + sad" is odd.
    # genre 2.0 + mood 1.5 + energy 3.0*(1-0) = 6.5. No coherence check exists.
    assert score == 6.5
    assert any("mood match" in r for r in reasons)
    assert any("energy" in r for r in reasons)


# ---------------------------------------------------------------------------
# 2. Out-of-range target_energy produces NEGATIVE scores (no clamping)
# ---------------------------------------------------------------------------
def test_out_of_range_energy_can_drive_score_negative():
    # target_energy=2.0 is outside the intended 0..1 range. Nothing validates it.
    prefs = {"favorite_genre": "zzz", "favorite_mood": "zzz", "target_energy": 2.0}
    song = make_song(genre="pop", mood="happy", energy=0.5)

    score, _ = score_song(prefs, song)

    # closeness = 1 - abs(0.5 - 2.0) = -0.5  ->  energy points = 3.0 * -0.5 = -1.5
    # With no genre/mood match, the total is negative. QUESTIONABLE: scores
    # should probably be floored at 0.
    assert score == -1.5


# ---------------------------------------------------------------------------
# 3. Energy alone can outrank a categorical match (weighting imbalance)
# ---------------------------------------------------------------------------
def test_energy_match_outranks_genre_only_match():
    # target_energy=1.0 so the genre song's energy=0.0 is MAXIMALLY far
    # (gap 1.0 -> closeness 0 -> 0 energy points).
    prefs = {"favorite_genre": "pop", "favorite_mood": "happy", "target_energy": 1.0}
    genre_only = make_song(id=1, genre="pop", mood="zzz", energy=0.0)   # +2.0 genre only
    energy_only = make_song(id=2, genre="zzz", mood="zzz", energy=1.0)  # +3.0 energy only

    ranked = recommend_songs(prefs, [genre_only, energy_only], k=2)

    # energy_only (3.0) beats genre_only (2.0): one numeric axis outweighs a
    # full genre match, because energy's weight (3.0) > genre's (2.0).
    assert ranked[0][0]["id"] == 2
    assert ranked[1][0]["id"] == 1


# ---------------------------------------------------------------------------
# 4. Categorical matching is CASE-SENSITIVE (a common real-world trap)
# ---------------------------------------------------------------------------
def test_genre_match_is_case_sensitive():
    prefs = {"favorite_genre": "Pop", "favorite_mood": "happy", "target_energy": 0.5}
    song = make_song(genre="pop", mood="happy", energy=0.5)  # data is lowercase

    score, reasons = score_song(prefs, song)

    # "Pop" != "pop" -> genre earns NOTHING. Only mood (1.5) + energy (3.0) count.
    assert score == 4.5
    assert not any("genre match" in r for r in reasons)


# ---------------------------------------------------------------------------
# 5. No matches + distant energy -> empty reasons list
# ---------------------------------------------------------------------------
def test_no_matches_yields_empty_reasons():
    prefs = {"favorite_genre": "polka", "favorite_mood": "", "target_energy": 0.0}
    song = make_song(genre="pop", mood="happy", energy=1.0)  # energy gap = 1.0

    score, reasons = score_song(prefs, song)

    # closeness = 1 - 1.0 = 0.0, which is NOT > 0.8, so no energy reason either.
    # Score is exactly 0 and the explanation is empty -> main.py shows
    # "(no strong matches)".
    assert score == 0.0
    assert reasons == []


# ---------------------------------------------------------------------------
# 6. A malformed profile (missing target_energy) raises KeyError
# ---------------------------------------------------------------------------
def test_missing_target_energy_raises_keyerror():
    import pytest

    prefs = {"favorite_genre": "pop", "favorite_mood": "happy"}  # no target_energy
    song = make_song()

    # QUESTIONABLE: there is no graceful handling of incomplete input.
    with pytest.raises(KeyError):
        score_song(prefs, song)


# ---------------------------------------------------------------------------
# 7. Ties resolve to INPUT ORDER (stable sort, no tie-breaker)
# ---------------------------------------------------------------------------
def test_ties_preserve_input_order():
    prefs = {"favorite_genre": "zzz", "favorite_mood": "zzz", "target_energy": 0.5}
    first = make_song(id=10, energy=0.5)   # both score exactly 3.0 on energy
    second = make_song(id=20, energy=0.5)

    ranked = recommend_songs(prefs, [first, second], k=2)

    # Equal scores -> the one that came first in the list stays first.
    assert ranked[0][0]["id"] == 10
    assert ranked[1][0]["id"] == 20
    assert ranked[0][1] == ranked[1][1]  # identical scores


# ---------------------------------------------------------------------------
# 8. likes_acoustic (and other attributes) never affect the score
# ---------------------------------------------------------------------------
def test_likes_acoustic_is_ignored():
    song = make_song(acousticness=0.95)
    likes = {"favorite_genre": "pop", "favorite_mood": "happy",
             "target_energy": 0.5, "likes_acoustic": True}
    dislikes = {"favorite_genre": "pop", "favorite_mood": "happy",
                "target_energy": 0.5, "likes_acoustic": False}

    # QUESTIONABLE: the field is part of the profile schema but score_song
    # never reads it, so the two produce identical scores.
    assert score_song(likes, song)[0] == score_song(dislikes, song)[0]
