# src/build_features.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import os

def main():
    # 1. Load metadata
    meta_df = pd.read_csv("../data/video_metadata.csv")
    video_ids = meta_df["video_id"].tolist()
    transcripts = meta_df["transcript"].tolist()

    # 2. Vectorize all transcripts
    vectorizer = TfidfVectorizer(max_features=50)
    tfidf_matrix = vectorizer.fit_transform(transcripts)
    features = tfidf_matrix.toarray()  # shape: (num_videos, dim)

    # 3. Report shape and sample
    print(f"Built video feature matrix with shape: {features.shape}")
    print("First video ID & vector (first 5 dims):")
    print(video_ids[0], features[0][:5])

    # 4. (Optional) Save to disk for reuse
    os.makedirs("../data", exist_ok=True)
    np.save("../data/video_features.npy", features)
    with open("../data/video_ids.npy", "wb") as f:
        np.save(f, np.array(video_ids))
    print("Saved features to data/video_features.npy and video_ids.npy")

if __name__ == "__main__":
    main()
