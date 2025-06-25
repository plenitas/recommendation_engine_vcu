# src/main.py

import os
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI(
    title="Video Recommendation Service",
    description="Returns top-N video recommendations for a given user.",
)

# ── Enable CORS ─────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
# ────────────────────────────────────────────────────────────

# ── Load your precomputed data ─────────────────────────────
DATA_DIR    = "data"
watch_df    = pd.read_csv(os.path.join(DATA_DIR, "watch_events.csv"))
video_ids   = np.load(os.path.join(DATA_DIR, "video_ids.npy"))
video_feats = np.load(os.path.join(DATA_DIR, "video_features.npy"))
# ────────────────────────────────────────────────────────────

@app.get("/recommendations")
def recommendations(user_id: str, n: int = 5):
    """Return top-n video recommendations for a given user."""
    if user_id not in watch_df["user_id"].unique():
        raise HTTPException(status_code=404, detail="User not found")
    # build profile
    watched = watch_df[watch_df["user_id"] == user_id]["video_id"].tolist()
    id_to_idx = {vid: idx for idx, vid in enumerate(video_ids)}
    idxs = [id_to_idx[v] for v in watched if v in id_to_idx]
    profile = video_feats[idxs].sum(axis=0).reshape(1, -1)
    # similarity search
    sims = cosine_similarity(profile, video_feats)[0]
    top_idxs = np.argsort(sims)[-n:][::-1]
    recs = [video_ids[i] for i in top_idxs]
    return {"user_id": user_id, "recommendations": recs}

# ── Serve your index.html at the site root ────────────────
@app.get("/")
def get_index():
    return FileResponse(os.path.join("static", "index.html"))

# ── Serve all files in /static under /static/... ───────────
app.mount("/static", StaticFiles(directory="static"), name="static")
# ────────────────────────────────────────────────────────────
