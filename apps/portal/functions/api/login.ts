// POST /api/login — verify allowlisted identifier + shared password, issue a signed cookie.
// The password is checked here on the edge; it is NEVER shipped to the browser.
import {
  createSessionCookie,
  isAllowed,
  normalizeIdentifier,
  safeEqualStr,
} from "../_lib/session";

interface Env {
  SESSION_SECRET: string;
  SHARED_PASSWORD: string;
  ALLOWLIST: string;
}

const GENERIC_ERROR = "Invalid email/number or password.";

export const onRequestPost: PagesFunction<Env> = async ({ request, env }) => {
  if (!env.SESSION_SECRET || !env.SHARED_PASSWORD) {
    return json({ error: "Portal is not configured. Contact the integrator." }, 500);
  }

  let identifier = "";
  let password = "";
  try {
    const ct = request.headers.get("content-type") || "";
    if (ct.includes("application/json")) {
      const body = (await request.json()) as { identifier?: string; password?: string };
      identifier = body.identifier ?? "";
      password = body.password ?? "";
    } else {
      const form = await request.formData();
      identifier = String(form.get("identifier") ?? "");
      password = String(form.get("password") ?? "");
    }
  } catch {
    return json({ error: GENERIC_ERROR }, 400);
  }

  const passwordOk = safeEqualStr(password, env.SHARED_PASSWORD);
  const userOk = isAllowed(identifier, env.ALLOWLIST || "");

  // Generic message on either failure — do not reveal which field was wrong.
  if (!passwordOk || !userOk) return json({ error: GENERIC_ERROR }, 401);

  const cookie = await createSessionCookie(normalizeIdentifier(identifier), env.SESSION_SECRET);
  return new Response(JSON.stringify({ ok: true }), {
    status: 200,
    headers: { "content-type": "application/json", "cache-control": "no-store", "Set-Cookie": cookie },
  });
};

function json(body: unknown, status: number): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json", "cache-control": "no-store" },
  });
}
