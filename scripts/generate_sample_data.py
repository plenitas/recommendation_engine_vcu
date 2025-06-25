import pandas as pd
import numpy as np
import os

# Ensure data/ exists
os.makedirs("data", exist_ok=True)

# -- Mock watch events (200 rows) --
users = [f"user_{i}" for i in range(1, 6)]
videos = [f"video_{j}" for j in range(1, 21)]
n_events = 200

watch_df = pd.DataFrame({
    "user_id": np.random.choice(users, n_events),
    "video_id": np.random.choice(videos, n_events),
    "watch_seconds": np.random.randint(5, 300, n_events)
})
watch_df.to_csv("data/watch_events.csv", index=False)

# -- Mock video metadata (20 rows) --
meta_df = pd.DataFrame({
    "video_id": videos,
    "transcript": [
        "This is a sample transcript about cooking and recipes." if j % 2 == 0
        else "An action-packed scene with cars and explosions."
        for j in range(1, 21)
    ]
})
meta_df.to_csv("data/video_metadata.csv", index=False)

print("Generated data/watch_events.csv and data/video_metadata.csv")