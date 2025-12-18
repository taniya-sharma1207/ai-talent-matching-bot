from pydantic import BaseModel

class JobRequest(BaseModel):
    cst_name: str
    client_problem_statement: str
    open_role: str
    tenure: int
    skills: list
    geo: str
    experience: int
    # TODO: Complete the JobRequest model with the required fields

class MatchRequest(BaseModel):
    job: JobRequest  # Ensure this matches the frontend request structure

# TODO: Create the MatchResult model with the required fields to represent the candidate evaluation results
