// Self-contained login page served by the edge middleware to any unauthenticated
// request. Inline CSS + JS only — no external assets — so nothing behind the gate is
// exposed to fetch the login screen.

export function renderLoginPage(): string {
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<meta name="robots" content="noindex, nofollow" />
<title>NOMAD Toronto — Sign in</title>
<style>
  :root { color-scheme: dark; }
  * { box-sizing: border-box; }
  body {
    margin: 0; min-height: 100dvh; display: grid; place-items: center;
    background: radial-gradient(120% 120% at 50% 0%, #1c0407 0%, #0a0a0b 55%);
    color: #f3f3f4; padding: env(safe-area-inset-top) 1.25rem 2rem;
    font: 16px/1.5 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  }
  .card {
    width: 100%; max-width: 380px; background: #141416; border: 1px solid #2a2a2e;
    border-radius: 16px; padding: 1.75rem; box-shadow: 0 20px 60px rgba(0,0,0,.55);
  }
  .brand { text-align: center; margin-bottom: 1.25rem; }
  .brand h1 { margin: 0; font-size: 1.4rem; letter-spacing: .14em; }
  .brand p { margin: .35rem 0 0; color: #a0a0a8; font-size: .82rem; }
  label { display: block; font-size: .8rem; color: #c9c9d0; margin: 0 0 .35rem; }
  input {
    width: 100%; padding: .7rem .8rem; margin-bottom: 1rem; border-radius: 10px;
    border: 1px solid #34343a; background: #0e0e10; color: #fff; font-size: 1rem;
  }
  input:focus { outline: 2px solid #c8102e; border-color: #c8102e; }
  button {
    width: 100%; padding: .8rem; border: 0; border-radius: 10px; cursor: pointer;
    background: #c8102e; color: #fff; font-size: 1rem; font-weight: 600;
  }
  button:disabled { opacity: .6; cursor: progress; }
  .err { color: #ff8a93; font-size: .85rem; min-height: 1.2em; margin: 0 0 .75rem; }
  .hint { color: #7d7d86; font-size: .74rem; margin: 1rem 0 0; text-align: center; }
</style>
</head>
<body>
  <main class="card">
    <div class="brand">
      <h1>NØMAD</h1>
      <p>Venue operations portal</p>
    </div>
    <form id="f" autocomplete="on">
      <label for="identifier">Email or WhatsApp number</label>
      <input id="identifier" name="identifier" type="text" inputmode="email"
             autocapitalize="none" autocomplete="username" required
             placeholder="you@email.com or +1 416 555 0123" />
      <label for="password">Access password</label>
      <input id="password" name="password" type="password"
             autocomplete="current-password" required placeholder="Shared password" />
      <p class="err" id="err" role="alert"></p>
      <button id="btn" type="submit">Sign in</button>
    </form>
    <p class="hint">Access is limited to approved NOMAD stakeholders.</p>
  </main>
<script>
  const f = document.getElementById('f'), btn = document.getElementById('btn'), err = document.getElementById('err');
  f.addEventListener('submit', async (e) => {
    e.preventDefault();
    err.textContent = ''; btn.disabled = true; btn.textContent = 'Signing in…';
    try {
      const res = await fetch('/api/login', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({
          identifier: document.getElementById('identifier').value,
          password: document.getElementById('password').value,
        }),
      });
      if (res.ok) { window.location.assign('/'); return; }
      const data = await res.json().catch(() => ({}));
      err.textContent = data.error || 'Sign in failed. Please try again.';
    } catch (_) {
      err.textContent = 'Network error. Please try again.';
    }
    btn.disabled = false; btn.textContent = 'Sign in';
  });
</script>
</body>
</html>`;
}
