/**
 * Public read-only visit aggregates (no personal data).
 */
const KEY = "aggregates_v1";

export async function onRequestGet(context) {
  const { env } = context;
  if (!env.VISITS) {
    return json({ ok: false, error: "storage_unavailable" }, 503);
  }

  let data = {
    updatedAt: null,
    totalVisits: 0,
    totalSessions: 0,
    byCountry: {},
    byPath: {},
    byReferrer: {},
    byDay: {},
    bySource: { linkedin: 0, github: 0, direct: 0, other: 0 },
  };

  try {
    const raw = await env.VISITS.get(KEY);
    if (raw) data = { ...data, ...JSON.parse(raw) };
  } catch {
    /* keep empty */
  }

  // Sort helpers for UI
  const countries = Object.entries(data.byCountry || {})
    .sort((a, b) => b[1] - a[1])
    .map(([code, visits]) => ({ code, visits }));
  const paths = Object.entries(data.byPath || {})
    .sort((a, b) => b[1] - a[1])
    .slice(0, 25)
    .map(([path, visits]) => ({ path, visits }));
  const days = Object.entries(data.byDay || {})
    .sort((a, b) => a[0].localeCompare(b[0]))
    .map(([day, visits]) => ({ day, visits }));

  return json(
    {
      ok: true,
      privacy:
        "Anonymous aggregates only. No names, emails, or IP addresses are stored.",
      totalVisits: data.totalVisits || 0,
      totalSessions: data.totalSessions || 0,
      updatedAt: data.updatedAt,
      bySource: data.bySource || {},
      countries,
      paths,
      days,
      github: null, // filled client-side from /data/github-traffic.json if present
    },
    200,
    {
      "Access-Control-Allow-Origin": "*",
      "Cache-Control": "public, max-age=30",
    }
  );
}

function json(obj, status = 200, extra = {}) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", ...extra },
  });
}
