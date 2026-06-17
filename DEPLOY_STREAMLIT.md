# Auto-deploy Streamlit app from GitHub Actions

This repository contains a GitHub Actions workflow that triggers a Streamlit deploy after a push to `main`.

What you must provide (GitHub repository secrets):

- `STREAMLIT_API_TOKEN` — your Streamlit Cloud API token (or other token accepted by your Streamlit deployment API).
- `STREAMLIT_APP_ID` — the ID of your Streamlit app (how to find: app settings or app URL in Streamlit Cloud).
- `STREAMLIT_DEPLOY_URL` *(optional)* — the base URL of Streamlit's deploy API. If omitted, the workflow uses `https://api.streamlit.io/api/v1` as a placeholder.

How it works:

1. On `push` to `main`, Actions checks out the repo, installs dependencies from `requirements.txt`, runs a quick syntax check, then calls the deploy endpoint:

```
POST $STREAMLIT_DEPLOY_URL/apps/$STREAMLIT_APP_ID/deploy
Authorization: Bearer $STREAMLIT_API_TOKEN
```

2. The workflow expects a 2xx status code from the endpoint to consider the deploy triggered successfully.

Setup:

1. Create the required repo secrets: go to *Settings → Secrets → Actions* and add the three secrets listed above.
2. If you are using Streamlit Cloud, check your app's settings for an API token or consult Streamlit Cloud docs for programmatic deploy options — copy the correct API base URL into `STREAMLIT_DEPLOY_URL` if necessary.

Testing locally with `curl` (example):

```bash
curl -X POST "https://api.streamlit.io/api/v1/apps/<APP_ID>/deploy" \
  -H "Authorization: Bearer <YOUR_TOKEN>" \
  -H "Content-Type: application/json" -d '{}'
```

If you need, I can try to locate the exact Streamlit Cloud API endpoint for you and tailor the workflow to use it directly.

Quick local helper:

You can run the included script `scripts/deploy_streamlit.sh` after exporting your secrets locally:

```bash
export STREAMLIT_API_TOKEN="<YOUR_TOKEN>"
export STREAMLIT_APP_ID="<APP_ID>"
./scripts/deploy_streamlit.sh
```

