# Math Games — Streamlit

This repo contains a kid‑friendly **Pokémon Math Mystery** game built with Streamlit.  
Run locally or deploy on Streamlit Community Cloud.

## Quickstart (local)

```bash
# in a fresh virtual environment
pip install -r requirements.txt
streamlit run app.py
```

Put images (PNG/JPG/GIF/WEBP) in the `assets/` folder. In the app, pick **Token Type = Image** and select a file.

## Deploy on Streamlit Community Cloud

1. Push this folder to a **GitHub** repo (e.g., `username/math-games`).
2. Go to https://share.streamlit.io (Community Cloud) → **New app**.
3. Choose your repo + branch, and set **Main file path** to `app.py`.
4. Click **Deploy**. The app will build with `requirements.txt` automatically.

### Repo layout
```
math-games/
├── app.py
├── requirements.txt
├── .gitignore
├── assets/
│   └── (your images go here)
└── README.md
```

### Notes
- If you add more games, create new tabs in `app.py` with `tabs = st.tabs([...])`.
- Large binary assets should be small (<10MB each). For bigger files, use a CDN or cloud storage.
