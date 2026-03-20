# Deploy contact API to Fly.io

Your **site** stays on **GitHub Pages**. This backend runs on Fly and handles `/contact` + Gmail SMTP.

## 1. Install CLI

```bash
curl -L https://fly.io/install.sh | sh
fly auth login
```

## 2. First deploy (from `backend/`)

```bash
cd backend
fly launch
```

- Pick an app name (or keep `keepmesafe-api` if free).
- Say **yes** to deploy now, or configure first.

If `fly.toml` already exists, you can:

```bash
fly deploy
```

## 3. Secrets (Gmail / Workspace)

Do **not** commit `.env`. Set variables on Fly:

```bash
fly secrets set \
  SMTP_HOST=smtp.gmail.com \
  SMTP_PORT=587 \
  SMTP_USER="michael.grisales@keepmesafe.live" \
  SMTP_PASSWORD="your-app-password" \
  FROM_EMAIL="michael.grisales@keepmesafe.live" \
  CONTACT_RECEIVER_EMAIL="michael.grisales@keepmesafe.live"
```

Redeploy after changing secrets (usually automatic on `fly secrets set`).

## 4. Connect the website

Your API URL looks like: `https://<your-app-name>.fly.dev`

In **`index.html`** (repo root), set:

```html
<meta name="contact-api-base" content="https://YOUR-APP-NAME.fly.dev">
```

Push to GitHub so Pages updates.

## 5. Optional: custom domain

In Fly dashboard: **Certificates** → add `api.keepmesafe.live` (or similar), then point DNS as Fly instructs. Use that HTTPS URL in `contact-api-base`.

## 6. Check health

```bash
curl https://YOUR-APP-NAME.fly.dev/
```

Should return JSON: `{"message":"Welcome to KeepMeSafe API"}`.
