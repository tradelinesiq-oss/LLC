/* ── TradeLine Marketplace — Email API Client ────────────────────────────
   Calls the backend email-server (see /email-server/app.py) to trigger
   welcome and order-confirmation emails. This file is safe to ship to the
   browser — it holds NO SMTP credentials, only the public API base URL.

   IMPORTANT: After you deploy email-server/app.py (Render, Railway, a VPS,
   etc.), update API_BASE_URL below to point at it, e.g.
   "https://tlm-email-server.onrender.com"
*/
const EMAIL_API_BASE_URL = "http://localhost:5000"; // ← change to your deployed server URL
const EMAIL_API_KEY = ""; // ← if you set API_KEY on the server, mirror it here

async function sendWelcomeEmail(email, name) {
  try {
    const res = await fetch(`${EMAIL_API_BASE_URL}/api/send-welcome-email`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(EMAIL_API_KEY ? { "X-API-Key": EMAIL_API_KEY } : {}),
      },
      body: JSON.stringify({ email, name }),
    });
    const data = await res.json();
    if (!data.ok) console.warn("Welcome email failed:", data.error);
    return data.ok;
  } catch (err) {
    // Fail silently from the user's perspective — don't block account creation
    // just because the email couldn't be sent (e.g. server offline in dev).
    console.warn("Could not reach email server:", err);
    return false;
  }
}

async function sendOrderConfirmationEmail(email, orderId, total) {
  try {
    const res = await fetch(`${EMAIL_API_BASE_URL}/api/send-order-confirmation`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(EMAIL_API_KEY ? { "X-API-Key": EMAIL_API_KEY } : {}),
      },
      body: JSON.stringify({ email, order_id: orderId, total }),
    });
    const data = await res.json();
    if (!data.ok) console.warn("Order confirmation email failed:", data.error);
    return data.ok;
  } catch (err) {
    console.warn("Could not reach email server:", err);
    return false;
  }
}
