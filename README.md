# TradeLine Marketplace — Email Server Setup

This folder contains a small backend that sends transactional emails
(welcome emails + order confirmations) on behalf of the website, using
**marketplacetradeline@gmail.com** as the sender.

## Why a backend at all?

SMTP credentials (username + password) can never be safely placed in
HTML/JavaScript that runs in a visitor's browser — anyone could open dev
tools and steal them. So the website calls a small API (`app.py`) over
HTTPS, and only that server holds the real SMTP login.

```
Website (cart.html / account.html)
        │  fetch('https://your-server.com/api/send-order-confirmation', …)
        ▼
   email-server/app.py  (holds SMTP_PASS secret)
        │  SMTP / STARTTLS
        ▼
     Gmail SMTP  →  customer's inbox
```

## 1. Get a Gmail "App Password"

Gmail will **reject** your normal account password over SMTP unless you
enable 2-Step Verification and create an **App Password** specifically for
this:

1. Go to your Google Account → Security → 2-Step Verification (turn it on
   if it isn't already).
2. Go to Security → App passwords.
3. Create a new app password (name it e.g. "TradeLine Marketplace SMTP").
4. Copy the 16-character password Google gives you — that's your `SMTP_PASS`.

## 2. Configure environment variables

```bash
cd email-server
cp .env.example .env
```

Edit `.env`:

```
SMTP_USER=marketplacetradeline@gmail.com
SMTP_PASS=<the 16-character app password from step 1>
API_KEY=<any long random string — generate with: openssl rand -hex 32>
ALLOWED_ORIGIN=https://yourdomain.com
```

## 3. Install & run locally

```bash
pip install -r requirements.txt
python app.py
```

The server starts on `http://localhost:5000`. Test it:

```bash
curl http://localhost:5000/api/health
```

## 4. Point the website at your server

Open `email-client.js` (in the site's root folder, alongside `index.html`)
and update:

```js
const EMAIL_API_BASE_URL = "http://localhost:5000"; // change to your deployed URL
const EMAIL_API_KEY = "";                            // must match API_KEY in .env
```

## 5. Deploy the server

Any host that runs Python works — a few easy options:

- **Render.com** — connect this `email-server` folder as a Web Service,
  set the same environment variables in the dashboard, build command
  `pip install -r requirements.txt`, start command `python app.py`.
- **Railway.app** — similar one-click deploy from this folder.
- **A VPS** (DigitalOcean, EC2, etc.) — run behind `gunicorn` + nginx for
  production instead of Flask's built-in dev server.

Once deployed, update `EMAIL_API_BASE_URL` in `email-client.js` to the
live URL (e.g. `https://tlm-email-server.onrender.com`) and re-upload that
file to your site.

## What triggers each email

| Email                  | Triggered from                                  |
|-------------------------|--------------------------------------------------|
| Welcome email            | `account.html` → "Create Account" form submit   |
| Order confirmation email | `cart.html` → "Place Order" after payment confirmed |

Both calls fail silently in the browser (logged to console only) if the
email server is unreachable, so a down email server never blocks someone
from creating an account or completing checkout.

## Security notes

- Never commit your real `.env` file — only `.env.example` should be in
  version control.
- Set `ALLOWED_ORIGIN` to your real domain once live, instead of `*`.
- The `API_KEY` header is a basic guard against random internet traffic
  hitting your `/api/*` routes and spamming your SMTP relay — keep it secret.
- For high email volume, consider a transactional provider (SendGrid,
  Postmark, Mailgun, Amazon SES) instead of raw Gmail SMTP, which has
  daily sending limits (~500/day on a normal Gmail account).
