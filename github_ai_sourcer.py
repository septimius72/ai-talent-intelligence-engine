import os
import csv
import requests
from google import genai
from google.genai import types

# Initialize Gemini Client (automatically reads GEMINI_API_KEY from environment)
client = genai.Client()

def search_github_builders(query, max_results=10):
    """Searches GitHub users based on technical topic/language queries."""
    url = f"https://github.com{query}&per_page={max_results}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get("items", [])

def get_user_details(username):
    """Fetches user profile and their top 3 public repositories."""
    user_url = f"https://github.com{username}"
    repos_url = f"https://github.com{username}/repos?sort=updated&per_page=3"
    
    user_data = requests.get(user_url).json()
    repos_data = requests.get(repos_url).json()
    
    repo_summaries = [
        f"{r.get('name')} ({r.get('language')}): {r.get('description')}"
        for r in repos_data if isinstance(r, dict)
    ]
    
    return {
        "username": username,
        "name": user_data.get("name") or username,
        "bio": user_data.get("bio") or "No bio provided",
        "location": user_data.get("location") or "Unknown",
        "blog": user_data.get("blog") or "",
        "profile_url": user_data.get("html_url"),
        "top_repos": " | ".join(repo_summaries)
    }

def evaluate_builder_with_gemini(profile, role_context):
    """Uses Gemini to score technical relevance and write a custom hook."""
    prompt = f"""
    Role Context: {role_context}
    
    Candidate GitHub Data:
    - Name: {profile['name']}
    - Location: {profile['location']}
    - Bio: {profile['bio']}
    - Recent Repos: {profile['top_repos']}
    
    Task:
    1. Give a Fit Score from 1 to 10 for production AI/Agentic engineering.
    2. Write a 1-sentence technical outreach hook referencing one of their specific repos.
    
    Format output strictly as: SCORE | HOOK
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.2)
    )
    
    parts = response.text.strip().split("|", 1)
    score = parts[0].strip() if len(parts) > 0 else "N/A"
    hook = parts[1].strip() if len(parts) > 1 else response.text.strip()
    return score, hook

if __name__ == "__main__":
    SEARCH_QUERY = "language:python mcp agent"
    ROLE_CONTEXT = "Staff Agentic AI Engineer building secure financial tool-use workflows and guardrails."
    
    print(f"Searching GitHub for: {SEARCH_QUERY}...")
    users = search_github_builders(SEARCH_QUERY, max_results=5)
    
    results = []
    for u in users:
        details = get_user_details(u["login"])
        score, hook = evaluate_builder_with_gemini(details, ROLE_CONTEXT)
        details["fit_score"] = score
        details["outreach_hook"] = hook
        results.append(details)
        print(f"Evaluated {details['username']} -> Score: {score}")

    # Export to CSV for Lever/Recruiter review
    with open("sourced_ai_builders.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    
    print("Saved ranked talent map to sourced_ai_builders.csv")
