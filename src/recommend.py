# src/recommend.py
import pandas as pd
import numpy as np
import sys
from sklearn.metrics.pairwise import cosine_similarity

def main(user_id=None, n=5):
    # Paths
    watch_csv = "data/watch_events.csv"
    ids_npy   = "data/video_ids.npy"
    feats_npy = "data/video_features.npy"

    # Load data
    watch_df    = pd.read_csv(watch_csv)
    video_ids   = np.load(ids_npy)
    video_feats = np.load(feats_npy)

    # Default user
    if user_id is None:
        user_id = sorted(watch_df["user_id"].unique())[0]

    # Build profile
    watched = watch_df[watch_df["user_id"] == user_id]["video_id"].tolist()
    id_to_idx = {vid: idx for idx, vid in enumerate(video_ids)}
    idxs      = [id_to_idx[v] for v in watched if v in id_to_idx]
    profile   = video_feats[idxs].sum(axis=0).reshape(1, -1)

    # Similarity search
    sims     = cosine_similarity(profile, video_feats)[0]
    top_idxs = np.argsort(sims)[-n:][::-1]
    recs     = [video_ids[i] for i in top_idxs]

    # Output
    print(f"\nTop {n} recommendations for user '{user_id}':")
    for rank, vid in enumerate(recs, start=1):
        print(f"{rank}. {vid}")

if __name__ == "__main__":
    arg_user = sys.argv[1] if len(sys.argv) > 1 else None
    arg_n    = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    main(arg_user, arg_n)

