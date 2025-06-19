# Create README.md if needed
cat <<EOF > README.md
# Recommendation Engine POC

Structure:
- **data/**: sample CSVs (watch_events.csv, video_metadata.csv)  
- **scripts/**: helper scripts (e.g. generate_sample_data.py)  
- **notebooks/**: Jupyter notebooks for prototyping  
- **src/**: core Python modules for loading data, building embeddings, generating recs  
- **venv/**: virtual environment  
- **requirements.txt**: pinned Python dependencies  
EOF

git add requirements.txt README.md
git commit -m "Pin dependencies & add README"
git push