import json
from openai import OpenAI


# LM Studio local server
client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)


SYSTEM_PROMPT = """
You are a movie review extraction assistant.
Extract information from the user's review.

Reply with ONLY a valid JSON object in exactly this format:
{
    "title": "Dune",
    "rating": 9,
    "sentiment": "positive"
}

Rules:
- title must be a non-empty string
- rating must be an integer from 1 to 10
- sentiment must be either "positive" or "negative"
- Do not include Markdown or any explanation.
"""


def ask_llm(prompt: str, system: str) -> str:
    """Send one chat completion and return only message.content."""
    response = client.chat.completions.create(
        model="qwen3-0.6b",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content


def build_prompt(text: str) -> str:
    """Build a prompt asking the model to extract structured JSON."""
    return f"""
Extract the movie review information from this text.

Review:
{text}

Return ONLY a JSON object with exactly these three keys:
"title", "rating", "sentiment"

Example:
{{"title": "Dune", "rating": 9, "sentiment": "positive"}}
"""


def try_parse_json(text):
    """Return parsed JSON or None if JSON is invalid."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def extract_review(text: str) -> dict:
    """Ask the LLM and parse its response as JSON."""
    reply = ask_llm(build_prompt(text), SYSTEM_PROMPT)
    return try_parse_json(reply)


def check_review(d) -> str:
    """Validate the extracted review object."""

    if d is None:
        return "response is not valid JSON"

    if not isinstance(d, dict):
        return "response must be a JSON object"

    if set(d.keys()) != {"title", "rating", "sentiment"}:
        return "keys must be exactly title, rating, sentiment"

    if not isinstance(d["title"], str) or not d["title"].strip():
        return "title must be a non-empty string"

    # bool is a subclass of int, so check it separately
    if (
        isinstance(d["rating"], bool)
        or not isinstance(d["rating"], int)
        or not 1 <= d["rating"] <= 10
    ):
        return "rating must be an integer from 1 to 10"

    if d["sentiment"] not in {"positive", "negative"}:
        return 'sentiment must be "positive" or "negative"'

    return ""


def extract_with_retry(text: str, max_attempts=3) -> dict:
    """Extract a review and retry when JSON or validation fails."""

    prompt = build_prompt(text)

    for attempt in range(1, max_attempts + 1):

        reply = ask_llm(prompt, SYSTEM_PROMPT)
        data = try_parse_json(reply)
        error = check_review(data)

        if error == "":
            return data

        # Prepare correction prompt for the next attempt
        prompt = f"""
Your previous response was invalid.

Validation error:
{error}

Original review:
{text}

Return ONLY corrected JSON with exactly these keys:
"title", "rating", "sentiment"

Rules:
- title: non-empty string
- rating: integer from 1 to 10
- sentiment: "positive" or "negative"

Do not include Markdown or explanation.
"""

    print(f"ERROR: review failed after {max_attempts} attempts: {error}")
    return None


# ---------------------------------------------------------
# Demo
# ---------------------------------------------------------

REVIEWS = [
    "Saw Dune yesterday — absolutely loved it, easily 9/10!",
    "Barbie was ok I guess. 6 out of 10.",
    "Oppenheimer was incredible. I gave it a ten. Definitely positive.",
    "The movie was boring and disappointing. Only 3/10.",
    "Dune Part Two was fantastic, probably an 8 out of 10.",
    "I really disliked Barbie. It was not enjoyable at all, maybe 4/10."
]


if __name__ == "__main__":

    results = []

    positive_count = 0
    negative_count = 0

    for review in REVIEWS:
        result = extract_with_retry(review)

        if result is None:
            continue

        results.append(result)

        if result["sentiment"] == "positive":
            positive_count += 1
        else:
            negative_count += 1

    print("\nMOVIE REVIEW RESULTS")
    print("-" * 55)
    print(f"{'Title':<20} {'Rating':<10} {'Sentiment':<15}")
    print("-" * 55)

    for result in results:
        print(
            f"{result['title']:<20} "
            f"{result['rating']:<10} "
            f"{result['sentiment']:<15}"
        )

    print("-" * 55)
    print(f"Positive reviews: {positive_count}")
    print(f"Negative reviews: {negative_count}")
