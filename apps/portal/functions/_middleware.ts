// Edge gate for the whole site. Runs on every Cloudflare Pages request (pages + assets).
// Unauthenticated requests get the inline login page (navigations) or 401 (API), so
// nothing behind the gate is served until a valid session cookie is present.
import { verifySession } from "./_lib/session";
import { renderLoginPage } from "./_lib/login-page";

interface Env {
  SESSION_SECRET: string;
  SHARED_PASSWORD: string;
  ALLOWLIST: string;
}

export const onRequest: PagesFunction<Env> = async (ctx) => {
  const { request, env, next } = ctx;
  const path = new URL(request.url).pathname;

  // Auth endpoints handle their own logic (and must be reachable while logged out).
  if (path === "/api/login" || path === "/api/logout") return next();

  const identifier = await verifySession(request.headers.get("Cookie"), env.SESSION_SECRET);
  if (identifier) return next();

  if (path.startsWith("/api/")) {
    return new Response(JSON.stringify({ error: "Unauthorized" }), {
      status: 401,
      headers: { "content-type": "application/json", "cache-control": "no-store" },
    });
  }

  return new Response(renderLoginPage(), {
    status: 200,
    headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store" },
  });
};
