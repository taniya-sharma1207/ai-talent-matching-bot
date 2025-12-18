import openai
import os
import json
import re
from dotenv import load_dotenv

from app.prompts import generate_batch_prompt

# Load API key from environment variables
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load candidates from the JSON file
CANDIDATES_FILE = os.path.join(os.path.dirname(__file__), "data/candidates.json")

def load_candidates():
    """Loads candidates from a JSON file."""
    with open(CANDIDATES_FILE, "r") as file:
        return json.load(file)

def evaluate_candidates(job):
    """Evaluates all candidates using a SINGLE OpenAI API request."""
    candidates = load_candidates()
    print("Job", job)
    # Generate a detailed prompt
    prompt = generate_batch_prompt(job, candidates)

    # Make a single OpenAI API call with the generated prompt
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are an AI assistant evaluating how well candidates match a job description."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        n=1,
        stop=None,
        temperature=0.7
    )
    print("Response: ", response)
    # Parse the LLM response
    result_text = response.choices[0].message.content.strip()
    results = parse_batch_response(result_text)

    return results

def parse_batch_response(response_text: str):
    """Parses the batch response and extracts scores and explanations for all candidates."""
    results = []

    # Leverage regex to handle varying spaces and multi-line explanations when getting the candidates, their scores, and explanations
    pattern = re.compile(r"Candidate: (.*?)\nScore: (\d+)\nExplanation:\n(.*?)(?=\nCandidate:|\Z)", re.DOTALL)
    matches = pattern.findall(response_text)
    print("matches: ", type(matches))

    # Append each candidate's names, score, explanation, and job to the results list
    for match in matches:
        results.append({
            "candidate": match[0],
            "score": int(match[1]),
            "explanation": match[2]
        })
    # Sort candidates by score in descending order
    # Sort candidates by score in descending order and filter only the top 3
    top_results = sorted(results, key=lambda x: x["score"], reverse=True)[:3]
    return top_results
