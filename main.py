import os
from collections import defaultdict
from typing import Any

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

API_KEY = os.environ.get("API_KEY", "ak_u98ziziqdwwek4hmkibxsd72")
USER_EMAIL = os.environ.get("USER_EMAIL", "shubhamsingh7307529@gmail.com")

app = FastAPI(title="Stateless Analytics API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Event(BaseModel):
    user: str
    amount: float
    ts: int

class AnalyticsRequest(BaseModel):
    events: list[Event] = Field(default_factory=list)

@app.get("/")
def root():
    return {"status": "ok", "endpoint": "POST /analytics"}

@app.post("/analytics")
def analytics(body: AnalyticsRequest, x_api_key: str | None = Header(default=None, alias="X-API-Key")):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_totals: dict[str, float] = defaultdict(float)
    revenue = 0.0
    for event in body.events:
        if event.amount > 0:
            revenue += event.amount
            user_totals[event.user] += event.amount

    top_user = max(user_totals, key=user_totals.get) if user_totals else ""

    return {
        "email": USER_EMAIL,
        "total_events": len(body.events),
        "unique_users": len({event.user for event in body.events}),
        "revenue": revenue,
        "top_user": top_user,
    }
