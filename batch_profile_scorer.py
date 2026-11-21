import pandas as pd
from pydantic import BaseModel
from google import genai
from google.genai import types

client = genai.Client()

# Define strict structured output schema so results never break CSV formatting
class CandidateEvaluation(BaseModel):
    fit_score: int
    primary_strength: str
    risk_or_gap: str
    interview_question: str

def score_candidate_row(name, headline, summary, rubric):
    prompt = f"""
    Evaluate this candidate against our hiring rubric.
    
    RUBRIC:
    {rubric}
    
    CANDIDATE:
    Name: {name}
    Headline: {headline}
    Summary/Experience: {summary}
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=CandidateEvaluation,
            temperature=0.1
        ),
    )
    return CandidateEvaluation.model_validate_json(response.text)

if __name__ == "__main__":
    RUBRIC = """
    - Must have 6+ years of software engineering or product leadership experience.
    - Strong preference for high-throughput fintech, payments, or risk systems.
    - Hands-on production experience with LLM orchestration, guardrails, or AI-native product delivery.
    """
    
    # Example input CSV (replace with your exported LinkedIn/Lever CSV)
    # Expected columns: name, headline, summary
    df = pd.read_csv("candidates_input.csv")
    
    evaluations = []
    for _, row in df.iterrows():
        eval_result = score_candidate_row(
            row["name"], row["headline"], row["summary"], RUBRIC
        )
        evaluations.append(eval_result.model_dump())
        print(f"Scored {row['name']}: {eval_result.fit_score}/10")
        
    eval_df = pd.DataFrame(evaluations)
    final_df = pd.concat([df, eval_df], axis=1).sort_values(by="fit_score", ascending=False)
    final_df.to_csv("calibrated_shortlist.csv", index=False)
    print("Exported ranked shortlist to calibrated_shortlist.csv")
