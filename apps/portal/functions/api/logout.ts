// /api/logout — clear the session cookie and return to the (gated) home page,
// which will render the login screen. Accepts GET (sidebar link) and POST.
import { clearSessionCookie } from "../_lib/session";

export const onRequest: PagesFunction = async () => {
  return new Response(null, {
    status: 302,
    headers: { Location: "/", "Set-Cookie": clearSessionCookie(), "cache-control": "no-store" },
  });
};
