/**
 * Public aggregate stats (no personal data).
 */

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
  "Content-Type": "application/json; charset=utf-8",
  "Cache-Control": "public, max-age=30",
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data), { status, headers: CORS });
}

export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS });
}

export async function onRequestGet(context) {
  try {
    const kv = context.env.VISITS;
    if (!kv) return json({ ok: false, error: "VISITS KV not bound" }, 500);

    const total = parseInt((await kv.get("total")) || "0", 10) || 0;

    const countries = {};
    let cursor;
    do {
      const page = await kv.list({ prefix: "country:", cursor, limit: 1000 });
      for (const key of page.keys) {
        const code = key.name.replace(/^country:/, "");
        const n = parseInt((await kv.get(key.name)) || "0", 10) || 0;
        if (n > 0) countries[code] = n;
      }
      cursor = page.list_complete ? undefined : page.cursor;
    } while (cursor);

    const days = {};
    cursor = undefined;
    do {
      const page = await kv.list({ prefix: "day:", cursor, limit: 1000 });
      for (const key of page.keys) {
        const d = key.name.replace(/^day:/, "");
        const n = parseInt((await kv.get(key.name)) || "0", 10) || 0;
        if (n > 0) days[d] = n;
      }
      cursor = page.list_complete ? undefined : page.cursor;
    } while (cursor);

    const topCountries = Object.entries(countries)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 25)
      .map(([code, visits]) => ({ code, visits }));

    const last7 = Object.entries(days)
      .sort((a, b) => (a[0] < b[0] ? 1 : -1))
      .slice(0, 7)
      .map(([day, visits]) => ({ day, visits }));

    return json({
      ok: true,
      site: "Zero²Hero Academy",
      privacy:
        "Anonymous aggregates only. Country code from Cloudflare edge. No names, emails, IPs, or cookies stored.",
      totalVisits: total,
      uniqueCountries: Object.keys(countries).length,
      topCountries,
      last7Days: last7,
      updatedAt: new Date().toISOString(),
      publicPage: "https://snzero2hero.com/stats",
      github: "https://github.com/amahmoud1986c-sketch/snzero2hero-academy",
    });
  } catch (e) {
    return json({ ok: false, error: String(e && e.message ? e.message : e) }, 500);
  }
}
