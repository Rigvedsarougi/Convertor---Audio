mkdir -p ~/.streamlit/
echo "[general]
email = \"rigved.sarougi@henryharvin.com\"
" > ~/.streamlit/credentials.toml
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
