import requests

from test_cases import TEST_CASES


API_URL = "http://127.0.0.1:8000/chat"


def run_test(test_case, index):

    session_id = f"evaluation_{index}"

    if "setup_message" in test_case:

        setup_response = requests.post(
            API_URL,
            json={
                "session_id": session_id,
                "message": test_case["setup_message"],
            },
        )

        if setup_response.status_code != 200:
            return {
                "name": test_case["name"],
                "status": "FAIL",
                "reason": "Setup message failed",
            }

    response = requests.post(
        API_URL,
        json={
            "session_id": session_id,
            "message": test_case["message"],
        },
    )

    if response.status_code != 200:
        return {
            "name": test_case["name"],
            "status": "FAIL",
            "reason": f"HTTP {response.status_code}",
        }

    answer = response.json()["response"]
    answer_lower = answer.lower()

    # Check required concepts
    checks = test_case.get("checks", [])

    missing_checks = [
        word
        for word in checks
        if word.lower() not in answer_lower
    ]

    if missing_checks:
        return {
            "name": test_case["name"],
            "status": "FAIL",
            "reason": f"Missing expected concepts: {missing_checks}",
        }

    # Check forbidden phrases
    forbidden_phrases = test_case.get("must_not_contain", [])

    detected_phrases = [
        phrase
        for phrase in forbidden_phrases
        if phrase.lower() in answer_lower
    ]

    if detected_phrases:
        return {
            "name": test_case["name"],
            "status": "FAIL",
            "reason": f"Found unsafe claims: {detected_phrases}",
        }

    # Check maximum response length
    max_words = test_case.get("max_words")

    if max_words and len(answer.split()) > max_words:
        return {
            "name": test_case["name"],
            "status": "FAIL",
            "reason": f"Response exceeded {max_words} words",
        }

    return {
        "name": test_case["name"],
        "status": "PASS",
        "response": answer,
    }


def main():

    print("\nEnterprise AI Assistant Evaluation\n")
    print("-" * 50)

    results = []

    for index, test_case in enumerate(TEST_CASES):

        result = run_test(test_case, index)

        results.append(result)

        print(f"\n{result['name']}: {result['status']}")

        if result["status"] == "PASS":
            print(f"Response: {result['response']}")
        else:
            print(f"Reason: {result['reason']}")

    passed = sum(
        1
        for result in results
        if result["status"] == "PASS"
    )

    total = len(results)

    print("\n" + "-" * 50)
    print(f"Evaluation Score: {passed}/{total}")
    print(f"Pass Rate: {(passed / total) * 100:.1f}%")


if __name__ == "__main__":
    main()