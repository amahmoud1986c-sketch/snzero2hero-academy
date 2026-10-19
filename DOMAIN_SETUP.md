# Fix snzero2hero.com (DNS + Custom Domain)

## Why https://snzero2hero.com is not working

The domain **is registered** and its nameservers already point to Cloudflare (`alexia` / `apollo`), but:

1. There is **no DNS A/CNAME record** publishing the site yet  
2. The custom domain is **not attached** to the Pages project `snzero2hero` yet  
3. The Wrangler OAuth token can **read** the zone, but **cannot write DNS** (`zone:read` only)

Until those two records exist, browsers show “can’t resolve / site can’t be reached”.

## Working URLs right now

- https://snzero2hero.pages.dev/  ← opens Academy (`index.html`)
- https://snzero2hero.pages.dev/academy/
- https://github.com/amahmoud1986c-sketch/snzero2hero-academy (Public)
- https://amahmoud1986c-sketch.github.io/snzero2hero-academy/

## Fix in Cloudflare Dashboard (2 minutes)

1. Open: https://dash.cloudflare.com/  
2. Go to **Workers & Pages** → project **snzero2hero** → **Custom domains**  
3. Click **Set up a custom domain** → add:
   - `snzero2hero.com`
   - `www.snzero2hero.com`
4. Cloudflare will create the DNS records automatically. Wait for SSL = **Active** (often 1–15 minutes).

### Or create DNS manually (DNS → Records)

| Type  | Name | Target / Content              | Proxy |
|-------|------|-------------------------------|-------|
| CNAME | `@`  | `snzero2hero.pages.dev`       | Proxied (orange) |
| CNAME | `www`| `snzero2hero.pages.dev`       | Proxied (orange) |

> If apex CNAME is not allowed in your UI, use the **Custom domains** button on the Pages project — it sets apex correctly.

## After it works

- https://snzero2hero.com/ → Zero²Hero Academy homepage  
- https://snzero2hero.com/portal.html → HR Leave docs portal
