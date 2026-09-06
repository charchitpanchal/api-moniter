from app.ai.schemas import IncidentContext

SYSTEM_PROMPT = """You are an expert Site Reliability Engineer analyzing API monitoring incidents.
You will be given structured facts about an API failure. Based ONLY on the information provided,
respond with a root-cause analysis.

Rules:
- Do NOT invent facts, logs, or systems you were not told about.
- Do NOT claim to have access to logs, databases, or infrastructure you cannot see.
- Base your analysis strictly on the evidence given.
- Respond with ONLY a valid JSON object, no other text, no markdown formatting, no code fences.

The JSON object must have exactly these fields:
{
  "severity": "LOW" | "MEDIUM" | "HIGH" | "CRITICAL",
  "probable_cause": "<one sentence, your best inference from the evidence>",
  "evidence": ["<short evidence point>", "..."],
  "recommendation": ["<short actionable step>", "..."],
  "summary": "<2-3 sentence plain-English summary of what happened>"
}"""


def build_incident_analysis_prompt(context: IncidentContext) -> str:
    """
    Builds the user-facing prompt from structured incident context.
    Kept deliberately concise — see Day 21's 'AI cost control' rules.
    """
    errors_list = "\n".join(f"- {err}" for err in context.recent_errors) or "- (none recorded)"

    return f"""Analyze this API monitoring incident:

API Name: {context.api_name}
URL: {context.api_url}
Expected Status Code: {context.expected_status_code}
Actual Status Code: {context.actual_status_code if context.actual_status_code else "No response received"}
Response Time: {context.response_time_ms}ms
Consecutive Failures: {context.failure_count}
Incident Duration: {context.incident_duration_seconds}s

Recent Error Messages:
{errors_list}

Respond with the JSON object as instructed."""