def generate_batch_prompt(job, candidates):
    print("generate_batch_prompt job", job)
    """Generates a prompt that evaluates all candidates in a single request."""
    candidate_profiles = "\n".join([
        f"- {c['first_name']} {c['last_name']}, Title: {c['title']}, Skills: {c['skills']}, Experience: {c['years_experience']} years, Industries: {c['industry_experience']}, Location: {c['location']}"
        for c in candidates
    ])

    return f"""
    You are an AI assistant evaluating how well candidates match a job description.

   **Job Description**
    Team Environment: {job.get('client_problem_statement', 'Not provided')}
    Open Role: {job.get('open_role', 'Not specified')}
    Tenure: {job.get('tenure', 'Not specified')}
    Required Skills: {', '.join(job.get('skills', []))}
    Geography: {job.get('geo', 'Not specified')}
    Industry Experience: {job.get('experience', 'Not specified')}
    **Candidates Being Evaluated**
    {candidate_profiles}

    **Task**
    - Rank the candidates from best to worst fit for this job.
    - Provide a score from 1-10 for each candidate.
    - Explain why they are a good or bad fit.

    **Expected Output**
    Return results in the following format:

    Candidate: [First Last Name]
    Score: [Number between 1-10]
    Explanation: [Brief explanation]

    **Important:**
    - Provide a numeric score from 1-10 based on the candidate's fit.
    - Always include an explanation in bullet points.
    - Do not omit the explanation even for low scores.

    Now, evaluate the candidates.
    """