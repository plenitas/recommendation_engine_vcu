# src/user_profile.py
import pandas as pd
import numpy as np
import sys

def main(user_id=None):
    # Paths to data
    watch_csv = "../data/watch_events.csv"
    ids_npy   = "../data/video_ids.npy"
    feats_npy = "../data/video_features.npy"

    # 1. Load watch events and video features
    watch_df    = pd.read_csv(watch_csv)
    video_ids   = np.load(ids_npy)
    video_feats = np.load(feats_npy)

    # 2. Default to first user if none passed
    if user_id is None:
        user_id = watch_df["user_id"].unique()[0]

    # 3. Collect videos this user has watched
    watched = watch_df[watch_df["user_id"] == user_id]["video_id"].tolist()

    # 4. Map video IDs → indices
    id_to_idx = {vid: idx for idx, vid in enumerate(video_ids)}
    indices   = [id_to_idx[v] for v in watched if v in id_to_idx]

    # 5. Sum up those feature vectors
    profile_vec = video_feats[indices].sum(axis=0)

    # 6. Print out a summary
    print(f"User: {user_id}")
    print(f"Profile vector shape: {profile_vec.shape}")
    print("First 5 dimensions:", profile_vec[:5])

if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    main(arg)
