# src/embed.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def main():
    # 1. Load video metadata
    meta_df = pd.read_csv("../data/video_metadata.csv")

    # 2. Initialize TF-IDF over all transcripts
    vectorizer = TfidfVectorizer(max_features=50)  # 50-dim for demo
    tfidf_matrix = vectorizer.fit_transform(meta_df["transcript"])

    # 3. Inspect the first transcript’s vector
    first_vec = tfidf_matrix[0].toarray()[0]
    print(f"Transcript: {meta_df.loc[0, 'transcript']!r}\n")
    print("Vector dimension:", first_vec.shape[0])
    print("First 5 values:", first_vec[:5])

    # 4. (Optional) Show the feature names
    print("\nFeature names:", vectorizer.get_feature_names_out()[:10])

if __name__ == "__main__":
    main()
