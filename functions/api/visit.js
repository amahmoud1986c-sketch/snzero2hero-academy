/**
 * Privacy-friendly visit ping.
 * Stores ONLY: country code, path, referrer host, day — never IP, name, or cookies of identity.
 */
const KEY = "aggregates_v1";

function dayKey(d = new Date()) {
  return d.toISOString().slice(0, 10);
}

function hostOf(url) {
  try {
    if (!url) return "";
    return new URL(url).hostname.replace(/^www\./, "");
  } catch {
    return "";
  }
}

function emptyAgg() {
  return {
    updatedAt: null,
    totalVisits: 0,
    totalSessions: 0,
    byCountry: {},
    byPath: {},
    byReferrer: {},
    byDay: {},
    bySource: { linkedin: 0, github: 0, direct: 0, other: 0 },
  };
}

export async function onRequestPost(context) {
  const { request, env } = context;
  if (!env.VISITS) {
    return json({ ok: false, error: "storage_unavailable" }, 503);
  }

  let body = {};
  try {
    body = await request.json();
  } catch {
    body = {};
  }

  const country = (request.headers.get("CF-IPCountry") || "XX").toUpperCase();
  const path = sanitizePath(body.path || "/");
  const refHost = hostOf(body.referrer || request.headers.get("Referer") || "");
  const utm = String(body.utm_source || "").toLowerCase();
  const isNewSession = Boolean(body.newSession);

  let data = emptyAgg();
  try {
    const raw = await env.VISITS.get(KEY);
    if (raw) data = { ...emptyAgg(), ...JSON.parse(raw) };
  } catch {
    data = emptyAgg();
  }

  data.totalVisits += 1;
  if (isNewSession) data.totalSessions += 1;

  data.byCountry[country] = (data.byCountry[country] || 0) + 1;
  data.byPath[path] = (data.byPath[path] || 0) + 1;

  const day = dayKey();
  data.byDay[day] = (data.byDay[day] || 0) + 1;

  const refLabel = refHost || "direct";
  data.byReferrer[refLabel] = (data.byReferrer[refLabel] || 0) + 1;

  if (utm.includes("linkedin") || refHost.includes("linkedin")) {
    data.bySource.linkedin += 1;
  } else if (utm.includes("github") || refHost.includes("github")) {
    data.bySource.github += 1;
  } else if (!refHost) {
    data.bySource.direct += 1;
  } else {
    data.bySource.other += 1;
  }

  // Keep maps bounded
  data.byPath = topN(data.byPath, 80);
  data.byReferrer = topN(data.byReferrer, 40);
  data.byDay = topN(data.byDay, 60);
  data.updatedAt = new Date().toISOString();

  await env.VISITS.put(KEY, JSON.stringify(data));

  return json({ ok: true, country }, 200, {
    "Access-Control-Allow-Origin": "*",
    "Cache-Control": "no-store",
  });
}

export async function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    },
  });
}

function sanitizePath(p) {
  let s = String(p || "/").split("?")[0].split("#")[0];
  if (!s.startsWith("/")) s = "/" + s;
  if (s.length > 180) s = s.slice(0, 180);
  return s;
}

function topN(obj, n) {
  return Object.fromEntries(
    Object.entries(obj)
      .sort((a, b) => b[1] - a[1])
      .slice(0, n)
  );
}

function json(obj, status = 200, extra = {}) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", ...extra },
  });
}
