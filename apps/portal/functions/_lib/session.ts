// Stateless, HMAC-signed session cookie + allowlist/password helpers.
// Runs on the Cloudflare edge (Web Crypto). No third-party auth service, no DB.
// Files/dirs prefixed with "_" are not routable — this is a shared library only.

const COOKIE_NAME = "nomad_session";
const TTL_SECONDS = 60 * 60 * 24 * 30; // 30 days

const enc = new TextEncoder();
const dec = new TextDecoder();

function b64urlFromBytes(bytes: Uint8Array): string {
  let bin = "";
  for (const b of bytes) bin += String.fromCharCode(b);
  return btoa(bin).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

function bytesFromB64url(s: string): Uint8Array {
  const b64 = s.replace(/-/g, "+").replace(/_/g, "/") + "===".slice((s.length + 3) % 4);
  const bin = atob(b64);
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}

async function hmac(secret: string, data: string): Promise<Uint8Array> {
  const key = await crypto.subtle.importKey(
    "raw",
    enc.encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"],
  );
  const sig = await crypto.subtle.sign("HMAC", key, enc.encode(data));
  return new Uint8Array(sig);
}

function timingSafeEqual(a: Uint8Array, b: Uint8Array): boolean {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a[i]! ^ b[i]!;
  return diff === 0;
}

/** Constant-time-ish string compare (for the shared password). */
export function safeEqualStr(a: string, b: string): boolean {
  return timingSafeEqual(enc.encode(a), enc.encode(b));
}

/** Normalize an identifier: emails lowercased; phones to E.164 (NA-friendly). */
export function normalizeIdentifier(raw: string): string {
  const v = (raw ?? "").trim().toLowerCase();
  if (!v) return "";
  if (v.includes("@")) return v;
  if (v.startsWith("+")) return "+" + v.slice(1).replace(/\D/g, "");
  const digits = v.replace(/\D/g, "");
  if (digits.length === 10) return `+1${digits}`;
  if (digits.length === 11 && digits.startsWith("1")) return `+${digits}`;
  return digits ? `+${digits}` : "";
}

/** Is `identifier` present in the comma-separated allowlist? */
export function isAllowed(identifier: string, allowlistRaw: string): boolean {
  const id = normalizeIdentifier(identifier);
  if (!id) return false;
  const set = new Set(
    (allowlistRaw ?? "")
      .split(",")
      .map((s) => normalizeIdentifier(s))
      .filter(Boolean),
  );
  return set.has(id);
}

export async function createSessionCookie(identifier: string, secret: string): Promise<string> {
  const exp = Math.floor(Date.now() / 1000) + TTL_SECONDS;
  const payloadB64 = b64urlFromBytes(enc.encode(JSON.stringify({ sub: identifier, exp })));
  const sigB64 = b64urlFromBytes(await hmac(secret, payloadB64));
  const value = `${payloadB64}.${sigB64}`;
  return `${COOKIE_NAME}=${value}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${TTL_SECONDS}`;
}

export function clearSessionCookie(): string {
  return `${COOKIE_NAME}=; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=0`;
}

function readCookie(cookieHeader: string | null, name: string): string | null {
  if (!cookieHeader) return null;
  for (const part of cookieHeader.split(";")) {
    const idx = part.indexOf("=");
    if (idx === -1) continue;
    if (part.slice(0, idx).trim() === name) return part.slice(idx + 1).trim();
  }
  return null;
}

/** Returns the authenticated identifier if the cookie is valid + unexpired, else null. */
export async function verifySession(
  cookieHeader: string | null,
  secret: string,
): Promise<string | null> {
  if (!secret) return null;
  const token = readCookie(cookieHeader, COOKIE_NAME);
  if (!token) return null;
  const dot = token.indexOf(".");
  if (dot === -1) return null;
  const payloadB64 = token.slice(0, dot);
  const sigB64 = token.slice(dot + 1);
  let expected: Uint8Array;
  let got: Uint8Array;
  try {
    expected = await hmac(secret, payloadB64);
    got = bytesFromB64url(sigB64);
  } catch {
    return null;
  }
  if (!timingSafeEqual(expected, got)) return null;
  try {
    const { sub, exp } = JSON.parse(dec.decode(bytesFromB64url(payloadB64)));
    if (typeof exp !== "number" || exp < Math.floor(Date.now() / 1000)) return null;
    return typeof sub === "string" ? sub : null;
  } catch {
    return null;
  }
}
