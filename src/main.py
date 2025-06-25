# src/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI(
    title="Video Recommendation Service",
    description="Returns top-N video recommendations for a given user.",
)

# Enable CORS so that the HTML page can fetch from this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Allow all origins during development
    allow_methods=["*"],      # Allow GET, POST, etc.
    allow_headers=["*"],      # Allow any headers
)

# Serve static HTML from the 'static' directory at the root path
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# Load data once at startup
data_dir = "data"
watch_df    = pd.read_csv(f"{data_dir}/watch_events.csv")
video_ids   = np.load(f"{data_dir}/video_ids.npy")
video_feats = np.load(f"{data_dir}/video_features.npy")

def build_profile(user_id: str) -> np.ndarray:
    """Sum feature vectors of all videos watched by the user."""
    watched = watch_df[watch_df["user_id"] == user_id]["video_id"].tolist()
    if not watched:
        raise ValueError(f"No watch history for user '{user_id}'")
    id_to_idx = {vid: idx for idx, vid in enumerate(video_ids)}
    idxs = [id_to_idx[v] for v in watched if v in id_to_idx]
    return video_feats[idxs].sum(axis=0).reshape(1, -1)

@app.get("/recommendations")
def recommendations(user_id: str, n: int = 5):
    """
    Query parameters:
    - user_id: the user to recommend for
    - n: number of recommendations (default 5)
    """
    if user_id not in watch_df["user_id"].unique():
        raise HTTPException(status_code=404, detail="User not found")

    profile = build_profile(user_id)
    sims    = cosine_similarity(profile, video_feats)[0]
    top_idxs = np.argsort(sims)[-n:][::-1]
    recs    = [video_ids[i] for i in top_idxs]

    return {"user_id": user_id, "recommendations": recs}
