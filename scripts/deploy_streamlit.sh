#!/usr/bin/env bash
# Simple deploy trigger script for Streamlit (needs env vars set)
set -euo pipefail

if [ -z "${STREAMLIT_API_TOKEN:-}" ] || [ -z "${STREAMLIT_APP_ID:-}" ]; then
  echo "Please set STREAMLIT_API_TOKEN and STREAMLIT_APP_ID environment variables."
  exit 1
fi

STREAMLIT_DEPLOY_URL=${STREAMLIT_DEPLOY_URL:-https://api.streamlit.io/api/v1}

echo "Triggering deploy for app: $STREAMLIT_APP_ID at $STREAMLIT_DEPLOY_URL"
curl -v -X POST "$STREAMLIT_DEPLOY_URL/apps/$STREAMLIT_APP_ID/deploy" \
  -H "Authorization: Bearer $STREAMLIT_API_TOKEN" \
  -H "Content-Type: application/json" -d '{}' || exit 1

echo "Deploy request sent."
