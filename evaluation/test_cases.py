TEST_CASES = [
    {
        "name": "Basic Question",
        "message": "What is SQL?",
        "checks": ["database", "query"],
    },
    {
        "name": "Instruction Following",
        "message": "Explain Python in exactly one sentence.",
        "checks": [],
        "max_words": 30,
    },
    {
        "name": "Context Retention",
        "setup_message": "My favorite programming language is Python.",
        "message": "What is my favorite programming language?",
        "checks": ["python"],
    },
    {
        "name": "Uncertainty Handling",
        "message": "What will be the exact stock price of Apple one year from today?",
        "checks": [],
        "must_not_contain": [
        "will be exactly",
        "the exact price will be",
        ],
    },
]