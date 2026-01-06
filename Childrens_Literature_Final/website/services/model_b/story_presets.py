STORY_LENGTH_PRESETS = {
    "Short (3–5 min)": {
        "min_tokens": 120,
        "max_tokens": 180
    },
    "Medium (5–7 min)": {
        "min_tokens": 200,
        "max_tokens": 280
    },
    "Long (7–10 min)": {
        "min_tokens": 320,
        "max_tokens": 420
    }
}

READING_LEVEL_PRESETS = {
    "Early Reader (4–6)": {
        "vocab_level": "simple",
        "target_ttr": 0.25,
        "max_sentence_length": 10
    },
    "Developing Reader (6–8)": {
        "vocab_level": "moderate",
        "target_ttr": 0.35,
        "max_sentence_length": 14
    },
    "Confident Reader (8–10)": {
        "vocab_level": "rich",
        "target_ttr": 0.45,
        "max_sentence_length": 18
    }
}

STORY_TYPE_PRESETS = {
    "Character Adventure": {
        "topic_bucket": "character-driven",
        "num_characters": 1
    },
    "Learning Story": {
        "topic_bucket": "instructional"
    },
    "Counting / Numbers": {
        "topic_bucket": "numeric"
    }
}
