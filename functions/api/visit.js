/**
 * Privacy-friendly visit beacon.
 * Stores ONLY: total count + ISO country code (from Cloudflare CF-IPCountry).
 * No cookies, no emails, no IP storage, no registration.
 */

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
  "Content-Type": "application/json; charset=utf-8",
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data), { status, headers: CORS });
}

async function bump(kv, key) {
  const cur = parseInt((await kv.get(key)) || "0", 10) || 0;
  const next = cur + 1;
  await kv.put(key, String(next));
  return next;
}

export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS });
}

export async function onRequestPost(context) {
  try {
    const kv = context.env.VISITS;
    if (!kv) return json({ ok: false, error: "VISITS KV not bound" }, 500);

    const countryRaw = (context.request.headers.get("CF-IPCountry") || "XX").toUpperCase();
    const country = /^[A-Z]{2}$/.test(countryRaw) ? countryRaw : "XX";
    const day = new Date().toISOString().slice(0, 10);

    const total = await bump(kv, "total");
    const cCount = await bump(kv, `country:${country}`);
    await bump(kv, `day:${day}`);

    return json({
      ok: true,
      privacy: "country-only",
      total,
      country,
      countryCount: cCount,
      day,
    });
  } catch (e) {
    return json({ ok: false, error: String(e && e.message ? e.message : e) }, 500);
  }
}
