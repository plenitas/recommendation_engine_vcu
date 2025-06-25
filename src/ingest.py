# src/ingest.py
import pandas as pd

def main():
    # 1. Load the CSVs
    watch_df = pd.read_csv("../data/watch_events.csv")
    meta_df  = pd.read_csv("../data/video_metadata.csv")

    # 2. Inspect watch events
    print("=== watch_events.csv head ===")
    print(watch_df.head(), "\n")
    print("=== watch_events.csv info ===")
    print(watch_df.info(), "\n")

    # 3. Clean watch events
    watch_df = watch_df.dropna(subset=["user_id", "video_id"])
    print("After cleaning watch_events, null counts:")
    print(watch_df.isnull().sum(), "\n")

    # 4. Inspect video metadata
    print("=== video_metadata.csv head ===")
    print(meta_df.head(), "\n")
    print("=== video_metadata.csv info ===")
    print(meta_df.info(), "\n")

    # 5. Clean metadata
    meta_df = meta_df.dropna(subset=["video_id", "transcript"])
    print("After cleaning metadata, null counts:")
    print(meta_df.isnull().sum())

if __name__ == "__main__":
    main()
