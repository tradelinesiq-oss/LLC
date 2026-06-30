"""
TradeLine Marketplace — Email Notification Server
---------------------------------------------------
Small Flask API that the website calls (via fetch) to send transactional
emails. SMTP credentials live ONLY here, on the server — never in the
browser/HTML/JS, which is why this can't be done with plain client-side code.

Endpoints:
  POST /api/send-welcome-email       { "email": "...", "name": "..." }
  POST /api/send-order-confirmation  { "email": "...", "order_id": "...", "total": "..." }

Run locally:
  pip install flask flask-cors python-dotenv
  python app.py

Deploy anywhere that runs Python (Render, Railway, Fly.io, a VPS, etc.)
and point the website's API_BASE_URL (in email-client.js) at it.
"""

import os
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()  # reads variables from a local .env file if present

app = Flask(__name__)

# Restrict CORS to your actual website domain(s) in production.
# For local testing "*" is fine; tighten this before going live.
CORS(app, resources={r"/api/*": {"origins": os.getenv("ALLOWED_ORIGIN", "*")}})

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("email-server")

# ── SMTP CONFIG (all secrets pulled from environment variables) ────────────
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "marketplacetradeline@gmail.com")
SMTP_PASS = os.getenv("SMTP_PASS")  # set this in your environment / .env — never hardcode
FROM_EMAIL = os.getenv("FROM_EMAIL", "marketplacetradeline@gmail.com")
FROM_NAME = os.getenv("FROM_NAME", "TradeLine Marketplace")

# Simple shared-secret check so randoms on the internet can't spam your SMTP
# relay through this endpoint. The website includes this header on every call.
API_KEY = os.getenv("API_KEY", "")


def send_email(to_email: str, subject: str, body_html: str) -> None:
    """Sends a single HTML email via SMTP using STARTTLS."""
    if not SMTP_PASS:
        raise RuntimeError(
            "SMTP_PASS is not set. Set it as an environment variable "
            "(or in a .env file) — never hardcode credentials in source."
        )

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg["To"] = to_email
    msg.attach(MIMEText(body_html, "html"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(FROM_EMAIL, to_email, msg.as_string())


# ── EMAIL TEMPLATES ─────────────────────────────────────────────────────────

def welcome_email_html(username: str) -> str:
    return f"""
    <div style="font-family:'Segoe UI',Arial,sans-serif;max-width:560px;margin:0 auto;background:#F9FAFB;padding:32px">
      <div style="background:#0F1117;border-radius:12px 12px 0 0;padding:28px 32px;text-align:center">
        <span style="color:#fff;font-size:20px;font-weight:700;letter-spacing:0.02em">TradeLine <span style="color:#F59E0B">Marketplace</span></span>
      </div>
      <div style="background:#fff;padding:36px 32px;border-radius:0 0 12px 12px;border:1px solid #E5E7EB;border-top:none">
        <h2 style="color:#0F1117;font-size:22px;margin:0 0 16px">Welcome, {username}!</h2>
        <p style="color:#374151;font-size:15px;line-height:1.6;margin:0 0 16px">
          Thanks for creating an account with TradeLine Marketplace. Your account is ready,
          and you now have access to our full inventory of verified authorized-user tradelines
          starting at just $278.
        </p>
        <a href="https://yourdomain.com/marketplace.html"
           style="display:inline-block;background:#2563EB;color:#fff;text-decoration:none;
                  font-weight:700;padding:12px 24px;border-radius:8px;margin-top:8px;font-size:14px">
          Browse Tradelines →
        </a>
        <p style="color:#6B7280;font-size:13px;margin-top:28px">
          If you didn't create this account, you can safely ignore this email.
        </p>
      </div>
    </div>
    """


def order_confirmation_html(order_id: str, total: str) -> str:
    return f"""
    <div style="font-family:'Segoe UI',Arial,sans-serif;max-width:560px;margin:0 auto;background:#F9FAFB;padding:32px">
      <div style="background:#0F1117;border-radius:12px 12px 0 0;padding:28px 32px;text-align:center">
        <span style="color:#fff;font-size:20px;font-weight:700;letter-spacing:0.02em">TradeLine <span style="color:#F59E0B">Marketplace</span></span>
      </div>
      <div style="background:#fff;padding:36px 32px;border-radius:0 0 12px 12px;border:1px solid #E5E7EB;border-top:none">
        <h2 style="color:#0F1117;font-size:22px;margin:0 0 16px">Order Confirmed ✓</h2>
        <p style="color:#374151;font-size:15px;line-height:1.6;margin:0 0 20px">
          Thanks for your purchase. Here's a summary of your order:
        </p>
        <table style="width:100%;border-collapse:collapse;margin-bottom:20px">
          <tr>
            <td style="padding:10px 0;color:#6B7280;font-size:13px;border-bottom:1px solid #E5E7EB">Order Number</td>
            <td style="padding:10px 0;color:#0F1117;font-size:14px;font-weight:700;text-align:right;border-bottom:1px solid #E5E7EB">#{order_id}</td>
          </tr>
          <tr>
            <td style="padding:10px 0;color:#6B7280;font-size:13px">Total Paid</td>
            <td style="padding:10px 0;color:#0F1117;font-size:14px;font-weight:700;text-align:right">${total}</td>
          </tr>
        </table>
        <p style="color:#374151;font-size:14px;line-height:1.6">
          You'll receive a follow-up email once your tradeline is reporting to the bureaus.
          You can also track this order any time from your account dashboard.
        </p>
        <a href="https://yourdomain.com/account.html"
           style="display:inline-block;background:#2563EB;color:#fff;text-decoration:none;
                  font-weight:700;padding:12px 24px;border-radius:8px;margin-top:8px;font-size:14px">
          View Order in Dashboard →
        </a>
      </div>
    </div>
    """


# ── ROUTES ───────────────────────────────────────────────────────────────────

def _check_api_key(req) -> bool:
    if not API_KEY:
        return True  # no key configured — open (fine for local dev only)
    return req.headers.get("X-API-Key") == API_KEY


@app.route("/api/send-welcome-email", methods=["POST"])
def api_send_welcome_email():
    if not _check_api_key(request):
        return jsonify({"ok": False, "error": "Unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip()
    name = (data.get("name") or "there").strip()

    if not email or "@" not in email:
        return jsonify({"ok": False, "error": "A valid email is required."}), 400

    try:
        send_email(email, "Welcome to TradeLine Marketplace!", welcome_email_html(name))
        log.info(f"Welcome email sent to {email}")
        return jsonify({"ok": True})
    except Exception as e:
        log.exception("Failed to send welcome email")
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/api/send-order-confirmation", methods=["POST"])
def api_send_order_confirmation():
    if not _check_api_key(request):
        return jsonify({"ok": False, "error": "Unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip()
    order_id = (data.get("order_id") or "").strip()
    total = (data.get("total") or "").strip()

    if not email or "@" not in email:
        return jsonify({"ok": False, "error": "A valid email is required."}), 400
    if not order_id or not total:
        return jsonify({"ok": False, "error": "order_id and total are required."}), 400

    try:
        send_email(
            email,
            f"Order Confirmation #{order_id}",
            order_confirmation_html(order_id, total),
        )
        log.info(f"Order confirmation sent to {email} for order #{order_id}")
        return jsonify({"ok": True})
    except Exception as e:
        log.exception("Failed to send order confirmation email")
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"ok": True, "service": "tradeline-email-server"})


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=os.getenv("DEBUG", "0") == "1")
