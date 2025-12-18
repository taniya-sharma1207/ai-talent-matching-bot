import json
from http.client import HTTPException
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import services
from .models import MatchRequest
app = FastAPI()

# Flexible CORS policy for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Talent Matching Bot Backend is running!"}

# TODO: Implement the /match endpoint
# 1. Define the endpoint with the correct method and response model
# 2. Parse the request body to extract the job details
# 3. Implement the method to evaluate candidates and return the results

@app.post("/match", response_model=List[MatchRequest])
def match_candidates(request: MatchRequest):
    try:
        job_details = request.dict()
        results = services.evaluate_candidates(job_details)
        return results
    except Exception as e:
        raise HTTPException(e)