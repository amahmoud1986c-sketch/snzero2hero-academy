#!/usr/bin/env python3
"""Generate aligned chapters 03-16 matching 01_DEVELOPMENT.html shell."""
import re
from pathlib import Path

HTML_DIR = Path(__file__).parent
BASE = "https://dev398980.service-now.com"
STUDIO = (HTML_DIR / "STUDIO_CREATE_ALL_OBJECTS_01_16.html").read_text(encoding="utf-8")
DEV01 = (HTML_DIR / "01_DEVELOPMENT.html").read_text(encoding="utf-8")

STYLE = """  <style>
    .field-table th { white-space: nowrap; }
    .step-num { font-weight: 700; color: var(--brand-2); }
    .demo-box { border-left: 4px solid var(--brand-2); padding: .35rem 0 .35rem .85rem; margin: .75rem 0; }
    .chapter-nav { display: flex; justify-content: space-between; gap: 1rem; margin: 2rem 0 1rem; padding: 1rem; background: #f8fafc; border-radius: 8px; }
  </style>"""

RULE0 = re.search(
    r'<h2 id="rule0">.*?</div>\n<div class="demo-box">.*?</div>',
    DEV01,
    re.S,
).group(0)

CHAPTER_SLUGS = {
    1: "DEVELOPMENT",
    2: "ADMINISTRATION",
    3: "SERVICE_CATALOG",
    4: "SERVICE_PORTAL",
    5: "WORKSPACE_UIBUILDER",
    6: "NOTIFICATIONS_EVENTS_JOBS",
    7: "REPORTS_DASHBOARDS_PA",
    8: "ATF_TESTING",
    9: "MODULES_AND_INTEGRATION",
    10: "IMPLEMENTATION_AND_CONFIG",
    11: "SDK_CURSOR_CLAUDE",
    12: "INTEGRATION_FULL_GUIDE",
    13: "2HOUR_MASTER_SUMMARY",
    14: "AI_SERVICENOW_AGENTS",
    15: "CLAUDE_CLI_CODE_SERVICENOW",
    16: "SDK_FULL_DEV_ADMIN_FROM_SCRATCH",
}
CHAPTER_FILES = {n: f"{n:02d}_{CHAPTER_SLUGS[n]}.html" for n in range(1, 17)}


def fix_links(text):
    mapping = {
        r"STUDIO_CREATE_ALL_OBJECTS_01_16\.html#obj-01": "01_DEVELOPMENT.html#part-1-application",
        r"STUDIO_CREATE_ALL_OBJECTS_01_16\.html#obj-02": "01_DEVELOPMENT.html#part-2-table-employee",
        r"STUDIO_CREATE_ALL_OBJECTS_01_16\.html#obj-03": "01_DEVELOPMENT.html#part-3-table-req",
        r"STUDIO_CREATE_ALL_OBJECTS_01_16\.html#obj-04": "01_DEVELOPMENT.html#part-4-table-bal",
        r"STUDIO_CREATE_ALL_OBJECTS_01_16\.html#obj-05": "01_DEVELOPMENT.html#part-5-table-audit",
        r"STUDIO_CREATE_ALL_OBJECTS_01_16\.html#obj-06": "01_DEVELOPMENT.html#part-6-script-include-leave",
        r"STUDIO_CREATE_ALL_OBJECTS_01_16\.html#obj-07": "01_DEVELOPMENT.html#part-7-script-include-security",
        r"STUDIO_CREATE_ALL_OBJECTS_01_16\.html#obj-08": "01_DEVELOPMENT.html#part-8-br1",
        r"STUDIO_CREATE_ALL_OBJECTS_01_16\.html#obj-09": "01_DEVELOPMENT.html#part-9-br2",
        r"STUDIO_CREATE_ALL_OBJECTS_01_16\.html#obj-10": "01_DEVELOPMENT.html#part-10-br3",
        r"STUDIO_CREATE_ALL_OBJECTS_01_16\.html#obj-11": "01_DEVELOPMENT.html#part-11-br4",
        r"STUDIO_CREATE_ALL_OBJECTS_01_16\.html#obj-12": "01_DEVELOPMENT.html#part-12-cs1",
        r"STUDIO_CREATE_ALL_OBJECTS_01_16\.html#obj-13": "01_DEVELOPMENT.html#part-13-cs2",
        r"STUDIO_CREATE_ALL_OBJECTS_01_16\.html#obj-14": "01_DEVELOPMENT.html#part-14-ui-policy",
        r"STUDIO_CREATE_ALL_OBJECTS_01_16\.html#obj-15": "01_DEVELOPMENT.html#part-15-ui-action",
        r"STUDIO_CREATE_ALL_OBJECTS_01_16\.html#obj-16": "02_ADMINISTRATION.html#part-1-roles",
        r"STUDIO_CREATE_ALL_OBJECTS_01_16\.html#obj-17": "02_ADMINISTRATION.html#part-2-groups",
        r"STUDIO_CREATE_ALL_OBJECTS_01_16\.html#obj-18": "02_ADMINISTRATION.html#part-3-users",
        r"STUDIO_CREATE_ALL_OBJECTS_01_16\.html#obj-19": "02_ADMINISTRATION.html#part-4-acls",
        r"STUDIO_CREATE_ALL_OBJECTS_01_16\.html#obj-20": "02_ADMINISTRATION.html#part-5-properties",
        r"STUDIO_CREATE_ALL_OBJECTS_01_16\.html#obj-21": "06_NOTIFICATIONS_EVENTS_JOBS.html#part-1-events",
        r"STUDIO_CREATE_ALL_OBJECTS_01_16\.html#obj-22": "06_NOTIFICATIONS_EVENTS_JOBS.html#part-2-notifications",
        r"STUDIO_CREATE_ALL_OBJECTS_01_16\.html#obj-23": "06_NOTIFICATIONS_EVENTS_JOBS.html#part-3-job",
        r"STUDIO_CREATE_ALL_OBJECTS_01_16\.html#obj-24": "09_MODULES_AND_INTEGRATION.html#part-1-menu",
        r"STUDIO_CREATE_ALL_OBJECTS_01_16\.html#obj-25": "09_MODULES_AND_INTEGRATION.html#part-2-modules",
        r"STUDIO_CREATE_ALL_OBJECTS_01_16\.html#obj-26": "03_SERVICE_CATALOG.html#part-2-record-producer",
        r"STUDIO_CREATE_ALL_OBJECTS_01_16\.html#obj-27": "09_MODULES_AND_INTEGRATION.html#part-3-flow",
        r"STUDIO_CREATE_ALL_OBJECTS_01_16\.html#obj-28": "04_SERVICE_PORTAL.html#part-1-widget-my-leaves",
        r"STUDIO_CREATE_ALL_OBJECTS_01_16\.html#obj-29": "05_WORKSPACE_UIBUILDER.html#part-1-workspace",
        r"STUDIO_CREATE_ALL_OBJECTS_01_16\.html#obj-30": "07_REPORTS_DASHBOARDS_PA.html#part-1-report",
        r"STUDIO_CREATE_ALL_OBJECTS_01_16\.html#obj-31": "08_ATF_TESTING.html#part-1-suite",
        r"STUDIO_CREATE_ALL_OBJECTS_01_16\.html#obj-32": "12_INTEGRATION_FULL_GUIDE.html#part-2-rest-api",
        r"STUDIO_CREATE_ALL_OBJECTS_01_16\.html#rule0": "01_DEVELOPMENT.html#rule0",
        r"STUDIO_CREATE_ALL_OBJECTS_01_16\.html#e2e-checklist": "10_IMPLEMENTATION_AND_CONFIG.html#part-2-e2e-checklist",
        r"#part-16-roles": "02_ADMINISTRATION.html#part-1-roles",
        r"#part-17-groups": "02_ADMINISTRATION.html#part-2-groups",
        r"#part-18-users": "02_ADMINISTRATION.html#part-3-users",
        r"#part-19-acls": "02_ADMINISTRATION.html#part-4-acls",
        r"#part-20-properties": "02_ADMINISTRATION.html#part-5-properties",
        r"#part-21-events": "06_NOTIFICATIONS_EVENTS_JOBS.html#part-1-events",
        r"#part-22-notifications": "06_NOTIFICATIONS_EVENTS_JOBS.html#part-2-notifications",
        r"#part-23-job": "06_NOTIFICATIONS_EVENTS_JOBS.html#part-3-job",
        r"#part-24-menu": "09_MODULES_AND_INTEGRATION.html#part-1-menu",
        r"#part-25-modules": "09_MODULES_AND_INTEGRATION.html#part-2-modules",
        r"#part-26-catalog": "03_SERVICE_CATALOG.html#part-2-record-producer",
        r"#part-27-flow": "09_MODULES_AND_INTEGRATION.html#part-3-flow",
        r"#part-28-portal": "04_SERVICE_PORTAL.html#part-1-widget-my-leaves",
        r"#part-29-workspace": "05_WORKSPACE_UIBUILDER.html#part-1-workspace",
        r"#part-30-report": "07_REPORTS_DASHBOARDS_PA.html#part-1-report",
        r"#part-31-atf": "08_ATF_TESTING.html#part-1-suite",
        r"#part-32-rest": "12_INTEGRATION_FULL_GUIDE.html#part-2-rest-api",
    }
    for pat, repl in mapping.items():
        text = re.sub(pat, repl, text)
    return text


def extract_part(part_id):
    m = re.search(
        rf'<h2 id="{part_id}">.*?(?=\n<hr />\s*\n<h2 id="part-|\n<h2 id="chapter-map|\Z)',
        STUDIO,
        re.S,
    )
    return m.group(0).strip() if m else ""


def rename_part(section, new_num, new_slug, new_title):
    return re.sub(
        r'<h2 id="part-[^"]+">Part \d+: [^<]+</h2>',
        f'<h2 id="part-{new_num}-{new_slug}">Part {new_num}: {new_title}</h2>',
        section,
        count=1,
    )


def extract_between(text, start_marker, end_marker):
    s = text.find(start_marker)
    if s < 0:
        return ""
    e = text.find(end_marker, s + len(start_marker))
    return text[s:e].strip() if e >= 0 else text[s:].strip()


def part_header(num, slug, title):
    return f'<h2 id="part-{num}-{slug}">Part {num}: {title}</h2>'


def intro_ok(text, prev_file, prev_label):
    return f"""<div class="ok">
<p><strong>Studio-only from scratch:</strong> {text}</p>
<p>Also open: <a href="PROFESSIONAL_HR_CREATE_PROPERTIES_AND_LINKS.html">Properties + Direct Links</a> · <a href="SCHEMA_AND_DATA.html">Schema</a> · <a href="STUDIO_CREATE_ALL_OBJECTS_01_16.html">Studio Create All Objects</a> · Previous: <a href="{prev_file}">{prev_label}</a></p>
</div>"""


def chapter_nav(num):
    prev_link = f'<a href="{CHAPTER_FILES[num - 1]}">← Chapter {num - 1:02d}</a>' if num > 1 else ""
    next_link = (
        f'<a href="{CHAPTER_FILES[num + 1]}">Chapter {num + 1:02d} →</a>'
        if num < 16
        else ""
    )
    return f'<nav class="chapter-nav">{prev_link}<span>Chapter {num:02d}</span>{next_link}</nav>'


def write_chapter(num, title, hero_html, quick_links, body, part_count):
    prev = CHAPTER_FILES[num - 1] if num > 1 else None
    ql = "\n".join(quick_links)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title} | HR Leave Australia</title>
  <link rel="stylesheet" href="assets/docs.css" />
{STYLE}
</head>
<body>
  <header class="topbar">
    <div class="brand">HR Leave · Australia</div>
    <nav>
      <a href="index.html">Portal</a>
      <a href="STUDIO_CREATE_ALL_OBJECTS_01_16.html">Studio Create All</a>
      <a href="PROFESSIONAL_HR_CREATE_PROPERTIES_AND_LINKS.html">Properties + Links</a>
      <a href="SCHEMA_AND_DATA.html">Schema</a>
      <a href="scripts/index.html">Scripts</a>
      <span class="badge">Scope x_786686_hr_leave</span>
      <span class="badge">Chapter {num:02d}</span>
    </nav>
  </header>
  <main class="layout">
    <section class="hero">
{hero_html}
    </section>
    <div class="url-box"><strong>Quick open</strong>
{ql}
    </div>
    <article class="content">
{body}
    </article>
    {chapter_nav(num)}
    <p class="footer">HR Leave · Studio from scratch · scope x_786686_hr_leave · replace {{BASE}} with your instance URL</p>
  </main>

  <script src="assets/docs.js"></script>
  <script>
    (function () {{
      var BASE = '{BASE}';
      document.querySelectorAll('a[href*="{{BASE}}"]').forEach(function (a) {{
        a.href = a.href.split('{{BASE}}').join(BASE);
      }});
    }})();
  </script>
</body>
</html>"""
    (HTML_DIR / CHAPTER_FILES[num]).write_text(html, encoding="utf-8")
    return part_count


RP_SCRIPT = Path(r"C:\SVCProject\HR_Leave_App\src\catalog\RP_submit_leave.js").read_text(encoding="utf-8")


def build_ch03():
    hero = """      <h1>03 — Service Catalog (Studio From Scratch)</h1>
      <p>Category HR Leave, Record Producer Submit Leave Request, variables, producer script, publish</p>
      <div class="meta-grid">
        <div><strong>Scope</strong><code style="color:#fff">x_786686_hr_leave</code></div>
        <div><strong>sys_id</strong><code style="color:#fff;font-size:.72rem">e5f5bc9493a303507520703efaba104d</code></div>
        <div><strong>Instance lab</strong><code style="color:#fff;font-size:.72rem">dev398980</code></div>
        <div><strong>URL token</strong><code style="color:#fff">{BASE}</code></div>
      </div>"""
    ql = [
        '<a href="{BASE}/sc_category_list.do">Categories</a>',
        '<a href="{BASE}/sc_cat_item_producer_list.do">Record Producers</a>',
        '<a href="{BASE}/esc">Employee Center</a>',
    ]
    body = fix_links(intro_ok(
        "Service Catalog intake for leave requests. Requires req_v2 table and employee role from chapters 01–02.",
        "02_ADMINISTRATION.html", "02 Administration",
    ) + """
<h2 id="how-objects-relate">How catalog objects relate</h2>
<div class="ok">
<pre style="white-space:pre-wrap;font-family:var(--mono);font-size:.85rem;background:#0b1220;color:#e2e8f0;padding:1rem;border-radius:12px">
Part 1 Category (HR Leave)
        │
        ▼
Part 2 Record Producer → Part 3 Variables
        │
        ▼
Part 4 Producer script (maps variables → req_v2)
        │
        ▼
Part 5 Publish → Employee Center / Portal catalog
        │
        ▼
BR1 days + approver → BR2 event → Flow approval
</pre>
<p><strong>Flow:</strong> employee1 opens catalog → submits → req_v2 inserted in submitted state → same lifecycle as UI Action Submit.</p>
</div>

<hr />

""" + RULE0 + """

<hr />

""" + part_header(1, "category", "Catalog Category — HR Leave") + """
<h3>Purpose</h3>
<p>Groups the Submit Leave Request record producer under a dedicated HR Leave catalog category.</p>
<h3>Navigation path</h3>
<nav class="section-links"><strong>All &gt;</strong> Service Catalog → Categories</nav>
<h3>Direct URL</h3>
<div class="url-box"><a href="{BASE}/sc_category.do?sys_id=-1">{BASE}/sc_category.do (New)</a></div>
<h3>Prerequisites</h3>
<ul><li><a href="01_DEVELOPMENT.html#part-1-application">Part 1: Application Setup</a> (01 Development).</li><li>Rule 0 Update Set current.</li></ul>
<h3>Form fields</h3>
<table class="field-table"><thead><tr><th>Field</th><th>Value</th></tr></thead><tbody>
<tr><td><strong>Title</strong></td><td>HR Leave</td></tr>
<tr><td><strong>Description</strong></td><td>Leave requests and balances</td></tr>
<tr><td>Active</td><td>true</td></tr>
<tr><td>Order</td><td>100</td></tr>
<tr><td>Application</td><td>HR Leave</td></tr>
</tbody></table>
<h3>Step-by-step create</h3>
<ol>
<li>Service Catalog → Categories → New.</li>
<li>Fill Title, Description, Order from table. Active = true.</li>
<li>Submit. Note category sys_id for record producer.</li>
</ol>
<h3>Verify checklist</h3>
<ul><li>Category HR Leave appears in category list.</li></ul>
<h3>Demo / test</h3>
<div class="demo-box"><p>Open Employee Center → catalog browse → HR Leave category visible (after producer published).</p></div>

<hr />

""" + part_header(2, "record-producer", "Record Producer — Submit Leave Request") + """
<h3>Purpose</h3>
<p>Service Catalog item that inserts submitted req_v2 from catalog variables.</p>
<h3>Navigation path</h3>
<nav class="section-links"><strong>All &gt;</strong> Service Catalog → Record Producers OR Studio → Record Producer</nav>
<h3>Direct URL</h3>
<div class="url-box"><a href="{BASE}/sc_cat_item_producer_list.do?sysparm_query=nameLIKESubmit Leave">{BASE}/sc_cat_item_producer_list.do</a></div>
<h3>Prerequisites</h3>
<ul>
<li><a href="01_DEVELOPMENT.html#part-3-table-req">Part 3: Table — Leave Request</a> (01).</li>
<li><a href="02_ADMINISTRATION.html#part-1-roles">Part 1: Roles</a> employee role (02).</li>
<li><a href="#part-1-category">Part 1: Catalog Category</a>.</li>
</ul>
<h3>Form fields</h3>
<table class="field-table"><thead><tr><th>Field</th><th>Value</th></tr></thead><tbody>
<tr><td><strong>Name</strong></td><td>Submit Leave Request</td></tr>
<tr><td><strong>Table</strong></td><td>x_786686_hr_leave_req_v2</td></tr>
<tr><td><strong>Category</strong></td><td>HR Leave</td></tr>
<tr><td>Roles</td><td>x_786686_hr_leave.employee</td></tr>
<tr><td>Active</td><td>true</td></tr>
<tr><td>Application</td><td>HR Leave</td></tr>
</tbody></table>
<h3>Step-by-step create</h3>
<ol>
<li>Record Producers → New. Fill header fields from table.</li>
<li>Category = HR Leave. Table = req_v2. Roles = employee.</li>
<li>Save. Continue to Part 3 for variables and Part 4 for script.</li>
</ol>
<h3>Verify checklist</h3>
<ul><li>Producer record saved under HR Leave application.</li></ul>
<h3>Demo / test</h3>
<div class="demo-box"><p>Open producer form → Table field shows x_786686_hr_leave_req_v2.</p></div>

<hr />

""" + part_header(3, "variables", "Catalog Variables") + """
<h3>Purpose</h3>
<p>Four question variables mapped by the producer script to req_v2 u_* fields.</p>
<h3>Navigation path</h3>
<nav class="section-links"><strong>All &gt;</strong> Record Producer → Related Lists → Variables</nav>
<h3>Direct URL</h3>
<div class="url-box"><a href="{BASE}/sc_cat_item_producer_list.do">Record Producers</a></div>
<h3>Prerequisites</h3>
<ul><li><a href="#part-2-record-producer">Part 2: Record Producer</a> created.</li></ul>
<h3>Form fields — each variable New</h3>
<table class="field-table"><thead><tr><th>Name</th><th>Label</th><th>Type</th><th>Question</th><th>Mandatory</th></tr></thead><tbody>
<tr><td>leave_type</td><td>Leave Type</td><td>Choice</td><td>Leave Type</td><td>Yes</td></tr>
<tr><td>start_date</td><td>Start Date</td><td>Date</td><td>Start Date</td><td>Yes</td></tr>
<tr><td>end_date</td><td>End Date</td><td>Date</td><td>End Date</td><td>Yes</td></tr>
<tr><td>reason</td><td>Reason</td><td>Multi Line Text</td><td>Reason</td><td>No</td></tr>
</tbody></table>
<p>Choice values for leave_type: annual, sick, personal (match req_v2 u_leave_type choices).</p>
<h3>Step-by-step create</h3>
<ol>
<li>Open Submit Leave Request producer → Variables related list → New.</li>
<li>For each row: Name must match producer.* references in script. Set Label, Type, Mandatory.</li>
<li>Order: leave_type, start_date, end_date, reason.</li>
</ol>
<h3>Verify checklist</h3>
<ul><li>Four variables on producer; names exactly leave_type, start_date, end_date, reason.</li></ul>
<h3>Demo / test</h3>
<div class="demo-box"><p>Try It → variable form renders all four questions.</p></div>

<hr />

""" + part_header(4, "producer-script", "Producer Script") + """
<h3>Purpose</h3>
<p>Server-side script maps catalog variables to req_v2 fields and sets state submitted. Source: <code>src/catalog/RP_submit_leave.js</code>.</p>
<h3>Navigation path</h3>
<nav class="section-links"><strong>All &gt;</strong> Record Producer → Script tab</nav>
<h3>Direct URL</h3>
<div class="url-box"><a href="scripts/src/catalog/RP_submit_leave.js.html">Scripts portal — RP_submit_leave.js</a></div>
<h3>Prerequisites</h3>
<ul><li><a href="#part-3-variables">Part 3: Catalog Variables</a>.</li><li><a href="01_DEVELOPMENT.html#part-8-br1">Part 8: BR1</a> calculates days on insert.</li></ul>
<h3>Step-by-step create</h3>
<ol>
<li>Open producer → Script tab.</li>
<li>Paste full script below.</li>
<li>Save.</li>
</ol>
<h3>Full script (paste-ready)</h3>
<pre><code>""" + RP_SCRIPT.replace("&", "&amp;").replace("<", "&lt;") + """</code></pre>
<h3>Verify checklist</h3>
<ul><li>Script saves without syntax errors.</li></ul>
<h3>Demo / test</h3>
<div class="demo-box"><p>Background: no errors on save. Catalog submit tested in Part 5.</p></div>

<hr />

""" + part_header(5, "publish-test", "Publish and Test") + """
<h3>Purpose</h3>
<p>Publish catalog item and verify end-to-end submit from Employee Center.</p>
<h3>Navigation path</h3>
<nav class="section-links"><strong>All &gt;</strong> Service Catalog → Catalog Items → Publish</nav>
<h3>Direct URL</h3>
<div class="url-box"><a href="{BASE}/esc">Employee Center</a> · <a href="{BASE}/$sp.do">Service Portal</a></div>
<h3>Prerequisites</h3>
<ul><li>Parts 1–4 complete.</li><li>employee1 user with employee role and employee_v2 seeded.</li></ul>
<h3>Step-by-step create</h3>
<ol>
<li>Record Producer → Related Lists → Catalogs → add to HR Leave category.</li>
<li>Service Catalog → open producer → <strong>Publish</strong>.</li>
<li>Login as employee1 → Employee Center → HR Leave → Submit Leave Request.</li>
<li>Fill variables → Submit.</li>
<li>Verify req_v2 created in submitted state; u_days_count and u_approver_user set by BR1.</li>
<li>Verify Flow starts for manager1 approval.</li>
</ol>
<h3>Verify checklist</h3>
<ul>
<li>Catalog item visible to employee role.</li>
<li>Submit creates req_v2 in submitted state.</li>
<li>sysapproval_approver row for manager1.</li>
</ul>
<h3>Demo / test</h3>
<div class="demo-box"><p>employee1 submits → req_v2 row, BR1 sets days + approver, Flow starts.</p></div>

<h2 id="catalog-verify">Service Catalog verify checklist</h2>
<div class="ok"><p>Complete after Parts 1–5.</p></div>
<ol>
<li>HR Leave category active.</li>
<li>Record Producer scoped to HR Leave with four variables.</li>
<li>Producer script from src/catalog/RP_submit_leave.js pasted.</li>
<li>Published and visible in Employee Center.</li>
<li>E2E submit creates submitted req_v2.</li>
</ol>
""")
    return write_chapter(3, "03 — Service Catalog (Studio From Scratch)", hero, ql, body, 5)


def portal_widget_scripts(widget):
    p28 = extract_part("part-28-portal")
    if widget == "my_leaves":
        keys = ["hrlx_my_leaves HTML", "hrlx_my_leaves CSS", "hrlx_my_leaves Client", "hrlx_my_leaves Server"]
    else:
        keys = ["hrlx_balance HTML", "hrlx_balance CSS", "hrlx_balance Client", "hrlx_balance Server"]
    out = []
    for k in keys:
        m = re.search(rf"<h3>Full script — {re.escape(k)}.*?</pre>", p28, re.S)
        if m:
            out.append(m.group(0))
    return "\n".join(out)


def build_ch04():
    hero = """      <h1>04 — Service Portal (Studio From Scratch)</h1>
      <p>Widgets hrlx_my_leaves + hrlx_balance, page hrlx_home, roles, portal URL</p>
      <div class="meta-grid">
        <div><strong>Scope</strong><code style="color:#fff">x_786686_hr_leave</code></div>
        <div><strong>sys_id</strong><code style="color:#fff;font-size:.72rem">e5f5bc9493a303507520703efaba104d</code></div>
        <div><strong>Instance lab</strong><code style="color:#fff;font-size:.72rem">dev398980</code></div>
        <div><strong>URL token</strong><code style="color:#fff">{BASE}</code></div>
      </div>"""
    ql = [
        '<a href="{BASE}/$sp.do">Service Portal</a>',
        '<a href="{BASE}/sp_widget_list.do">Widgets</a>',
        '<a href="{BASE}/hrlx?id=hrlx_home">HR Leave Home</a>',
    ]
    my_scripts = portal_widget_scripts("my_leaves")
    bal_scripts = portal_widget_scripts("balance")
    body = fix_links(intro_ok(
        "Portal widgets use u_* fields on req_v2 and bal_v2. No external build tools.",
        "03_SERVICE_CATALOG.html", "03 Service Catalog",
    ) + """
<h2 id="how-objects-relate">How portal objects relate</h2>
<div class="ok">
<pre style="white-space:pre-wrap;font-family:var(--mono);font-size:.85rem;background:#0b1220;color:#e2e8f0;padding:1rem;border-radius:12px">
Portal (url_suffix hrlx)
  └── Page hrlx_home
        ├── Part 1 Widget hrlx_my_leaves (req_v2 list + cancel)
        └── Part 2 Widget hrlx_balance (bal_v2 cards)
Property x_786686_hr_leave.config.portal_page_id = hrlx_home
</pre>
</div>
<hr />
""" + RULE0 + """
<hr />
""" + part_header(1, "widget-my-leaves", "Widget — hrlx_my_leaves") + """
<h3>Purpose</h3>
<p>Lists current user's leave requests with cancel action for draft/submitted rows.</p>
<h3>Navigation path</h3>
<nav class="section-links"><strong>All &gt;</strong> Service Portal → Widgets OR Studio → Widget</nav>
<h3>Direct URL</h3>
<div class="url-box"><a href="{BASE}/sp_widget_list.do">{BASE}/sp_widget_list.do</a></div>
<h3>Prerequisites</h3>
<ul>
<li><a href="01_DEVELOPMENT.html#part-3-table-req">Part 3: Table — Leave Request</a> (01).</li>
<li><a href="02_ADMINISTRATION.html#part-1-roles">Part 1: Roles</a> employee (02).</li>
</ul>
<h3>Form fields</h3>
<table class="field-table"><thead><tr><th>Field</th><th>Value</th></tr></thead><tbody>
<tr><td><strong>ID</strong></td><td>hrlx_my_leaves</td></tr>
<tr><td><strong>Name</strong></td><td>HRLX My Leaves</td></tr>
<tr><td>Client controller</td><td>HrlxMyLeavesCtrl</td></tr>
<tr><td>Application</td><td>HR Leave</td></tr>
</tbody></table>
<h3>Step-by-step create</h3>
<ol>
<li>SP → Widgets → New → ID hrlx_my_leaves.</li>
<li>Paste HTML template, CSS, Client script, Server script from sections below.</li>
<li>Save.</li>
</ol>
""" + my_scripts + """
<h3>Verify checklist</h3>
<ul><li>Widget saves. Preview shows table structure.</li></ul>
<h3>Demo / test</h3>
<div class="demo-box"><p>After Part 3 page built: employee1 sees own requests.</p></div>
<hr />
""" + part_header(2, "widget-balance", "Widget — hrlx_balance") + """
<h3>Purpose</h3>
<p>Read-only balance cards for current year from bal_v2.</p>
<h3>Navigation path</h3>
<nav class="section-links"><strong>All &gt;</strong> Service Portal → Widgets</nav>
<h3>Direct URL</h3>
<div class="url-box"><a href="{BASE}/sp_widget_list.do">{BASE}/sp_widget_list.do</a></div>
<h3>Prerequisites</h3>
<ul>
<li><a href="01_DEVELOPMENT.html#part-4-table-bal">Part 4: Table — Leave Balance</a> (01).</li>
<li><a href="#part-1-widget-my-leaves">Part 1: Widget hrlx_my_leaves</a> (same portal context).</li>
</ul>
<h3>Form fields</h3>
<table class="field-table"><thead><tr><th>Field</th><th>Value</th></tr></thead><tbody>
<tr><td><strong>ID</strong></td><td>hrlx_balance</td></tr>
<tr><td><strong>Name</strong></td><td>HRLX Balance</td></tr>
<tr><td>Client controller</td><td>HrlxBalanceCtrl</td></tr>
<tr><td>Application</td><td>HR Leave</td></tr>
</tbody></table>
<h3>Step-by-step create</h3>
<ol>
<li>SP → Widgets → New → ID hrlx_balance.</li>
<li>Paste HTML, CSS, Client, Server from below.</li>
<li>Save.</li>
</ol>
""" + bal_scripts + """
<h3>Verify checklist</h3>
<ul><li>Cards show entitled/used/remaining when bal_v2 seeded.</li></ul>
<h3>Demo / test</h3>
<div class="demo-box"><p>employee1 with balance row → remaining displays correctly.</p></div>
<hr />
""" + part_header(3, "page-home", "Portal Page — hrlx_home") + """
<h3>Purpose</h3>
<p>HR Leave home page with balance widget on top and my leaves below.</p>
<h3>Navigation path</h3>
<nav class="section-links"><strong>All &gt;</strong> Service Portal → Portals / Pages</nav>
<h3>Direct URL</h3>
<div class="url-box"><a href="{BASE}/hrlx?id=hrlx_home">{BASE}/hrlx?id=hrlx_home</a></div>
<h3>Prerequisites</h3>
<ul><li><a href="#part-1-widget-my-leaves">Part 1</a> and <a href="#part-2-widget-balance">Part 2</a> widgets exist.</li></ul>
<h3>Form fields — Portal (sp_portal)</h3>
<table class="field-table"><thead><tr><th>Field</th><th>Value</th></tr></thead><tbody>
<tr><td><strong>Title</strong></td><td>HR Leave Portal</td></tr>
<tr><td><strong>URL suffix</strong></td><td>hrlx</td></tr>
<tr><td>Application</td><td>HR Leave</td></tr>
</tbody></table>
<h4>Page (sp_page)</h4>
<table class="field-table"><thead><tr><th>Field</th><th>Value</th></tr></thead><tbody>
<tr><td><strong>ID</strong></td><td>hrlx_home</td></tr>
<tr><td><strong>Title</strong></td><td>HR Leave Home</td></tr>
<tr><td>Application</td><td>HR Leave</td></tr>
<tr><td>Roles</td><td>x_786686_hr_leave.employee</td></tr>
</tbody></table>
<h3>Step-by-step create</h3>
<ol>
<li>Portals → New OR configure dedicated portal url_suffix <code>hrlx</code>.</li>
<li>Pages → New → ID hrlx_home → drag hrlx_balance (top), hrlx_my_leaves (below) on 12-column layout.</li>
<li>Page security → role employee.</li>
<li>Set property <code>x_786686_hr_leave.config.portal_page_id</code> = hrlx_home (02 Administration Part 5).</li>
<li>Save. Open {BASE}/hrlx?id=hrlx_home as employee1.</li>
</ol>
<h3>Verify checklist</h3>
<ul>
<li>employee1 sees own requests and balance.</li>
<li>Cancel button works on draft/submitted.</li>
</ul>
<h3>Demo / test</h3>
<div class="demo-box"><p>Login employee1 → hrlx?id=hrlx_home → requests + balance visible.</p></div>
<h2 id="portal-verify">Service Portal verify checklist</h2>
<div class="ok"><p>Complete after Parts 1–3.</p></div>
<ol>
<li>Two widgets scoped to HR Leave.</li>
<li>Page hrlx_home published with role restriction.</li>
<li>Portal URL opens for employee1.</li>
</ol>
""")
    return write_chapter(4, "04 — Service Portal (Studio From Scratch)", hero, ql, body, 3)


def build_ch05():
    hero = """      <h1>05 — Workspace / UI Builder (Studio From Scratch)</h1>
      <p>UI Builder experience HR Leave Workspace, pages, data resource on req_v2</p>
      <div class="meta-grid">
        <div><strong>Scope</strong><code style="color:#fff">x_786686_hr_leave</code></div>
        <div><strong>sys_id</strong><code style="color:#fff;font-size:.72rem">e5f5bc9493a303507520703efaba104d</code></div>
        <div><strong>Instance lab</strong><code style="color:#fff;font-size:.72rem">dev398980</code></div>
        <div><strong>URL token</strong><code style="color:#fff">{BASE}</code></div>
      </div>"""
    ql = ['<a href="{BASE}/now/build/ui">UI Builder</a>']
    body = fix_links(intro_ok(
        "Now Experience workspace with list pages on req_v2. Studio UI only — no npx or external build.",
        "04_SERVICE_PORTAL.html", "04 Service Portal",
    ) + """
<h2 id="how-objects-relate">How workspace objects relate</h2>
<div class="ok">
<pre style="white-space:pre-wrap;font-family:var(--mono);font-size:.85rem;background:#0b1220;color:#e2e8f0;padding:1rem;border-radius:12px">
Part 1 Experience (HR Leave Workspace)
  ├── Part 2 Pages (My Requests, Team Approvals, Admin)
  ├── Part 3 Data resource → req_v2 table broker
  └── Part 4 List component + role bindings
</pre>
</div>
<hr />
""" + RULE0 + """
<hr />
""" + part_header(1, "workspace", "Create Experience — HR Leave Workspace") + """
<h3>Purpose</h3>
<p>Now Experience workspace container scoped to HR Leave application.</p>
<h3>Navigation path</h3>
<nav class="section-links"><strong>All &gt;</strong> Now Experience → UI Builder</nav>
<h3>Direct URL</h3>
<div class="url-box"><a href="{BASE}/now/build/ui">{BASE}/now/build/ui</a></div>
<h3>Prerequisites</h3>
<ul><li><a href="01_DEVELOPMENT.html#part-3-table-req">Part 3: Table — Leave Request</a> (01).</li><li>Roles from 02 Administration.</li></ul>
<h3>Form fields</h3>
<table class="field-table"><thead><tr><th>Field</th><th>Value</th></tr></thead><tbody>
<tr><td><strong>Name</strong></td><td>HR Leave Workspace</td></tr>
<tr><td><strong>Application</strong></td><td>HR Leave</td></tr>
<tr><td>Experience type</td><td>Workspace / Custom</td></tr>
</tbody></table>
<h3>Step-by-step create</h3>
<ol>
<li>UI Builder → Create experience → fill fields → Create.</li>
<li>Confirm Application = HR Leave in header.</li>
</ol>
<h3>Verify checklist</h3>
<ul><li>Experience opens in UI Builder.</li></ul>
<h3>Demo / test</h3>
<div class="demo-box"><p>Preview URL loads (empty until pages added).</p></div>
<hr />
""" + part_header(2, "pages", "Pages — My Requests, Team Approvals, Admin") + """
<h3>Purpose</h3>
<p>Three routed pages for employee, manager, and HR admin personas.</p>
<h3>Navigation path</h3>
<nav class="section-links"><strong>All &gt;</strong> UI Builder → Pages</nav>
<h3>Prerequisites</h3>
<ul><li><a href="#part-1-workspace">Part 1: Create Experience</a>.</li></ul>
<h3>Form fields</h3>
<table class="field-table"><thead><tr><th>Label</th><th>Route</th><th>Roles</th></tr></thead><tbody>
<tr><td>My Requests</td><td>my-requests</td><td>employee, manager, hr_admin</td></tr>
<tr><td>Team Approvals</td><td>team-approvals</td><td>manager, hr_admin</td></tr>
<tr><td>Admin</td><td>admin</td><td>hr_admin</td></tr>
</tbody></table>
<h3>Step-by-step create</h3>
<ol>
<li>Add page → Name My Requests → Route my-requests.</li>
<li>Repeat for Team Approvals and Admin pages.</li>
<li>Add navigation menu items linking each page (Part 4).</li>
</ol>
<h3>Verify checklist</h3>
<ul><li>Three pages listed in experience.</li></ul>
<h3>Demo / test</h3>
<div class="demo-box"><p>Preview each route — page shell loads.</p></div>
<hr />
""" + part_header(3, "data-resource", "Data Resource — req_v2") + """
<h3>Purpose</h3>
<p>Table data broker feeding list components with req_v2 records.</p>
<h3>Navigation path</h3>
<nav class="section-links"><strong>All &gt;</strong> UI Builder → Data Resources</nav>
<h3>Prerequisites</h3>
<ul><li><a href="#part-2-pages">Part 2: Pages</a>.</li></ul>
<h3>Form fields — My Requests broker</h3>
<table class="field-table"><thead><tr><th>Field</th><th>Value</th></tr></thead><tbody>
<tr><td><strong>Label</strong></td><td>My Leave Requests</td></tr>
<tr><td><strong>Table</strong></td><td>x_786686_hr_leave_req_v2</td></tr>
<tr><td>Condition</td><td><code>u_requested_for_user=javascript:gs.getUserID()</code></td></tr>
</tbody></table>
<h4>Team Approvals broker</h4>
<table class="field-table"><tr><th>Condition</th><td>u_state=submitted AND u_approver_user=current user</td></tr></table>
<h3>Step-by-step create</h3>
<ol>
<li>Data Resources → Create → Table → req_v2.</li>
<li>Set conditions per page persona.</li>
<li>Columns: Number, Leave Type, Start, End, Days, State.</li>
</ol>
<h3>Verify checklist</h3>
<ul><li>Data resource preview returns rows for test user.</li></ul>
<h3>Demo / test</h3>
<div class="demo-box"><p>Preview broker as employee1 → only own requests.</p></div>
<hr />
""" + part_header(4, "bind-list-roles", "Bind List + Role Restrictions") + """
<h3>Purpose</h3>
<p>Attach list components to data resources and publish workspace with role access.</p>
<h3>Navigation path</h3>
<nav class="section-links"><strong>All &gt;</strong> UI Builder → Page editor → Components</nav>
<h3>Prerequisites</h3>
<ul><li><a href="#part-3-data-resource">Part 3: Data Resource</a>.</li></ul>
<h3>Step-by-step create</h3>
<ol>
<li>My Requests page → drag List → bind My Leave Requests data resource.</li>
<li>Team Approvals page → List → team broker filter.</li>
<li>Admin page → Lists for employee_v2 and bal_v2 — hr_admin only.</li>
<li>Navigation: menu items with role restrictions per page.</li>
<li><strong>Publish</strong> workspace → assign roles employee, manager, hr_admin.</li>
<li>Impersonate each test user → open workspace URL.</li>
</ol>
<h3>Verify checklist</h3>
<ul>
<li>employee sees only own requests on My Requests.</li>
<li>manager sees submitted items awaiting approval.</li>
<li>hr_admin sees admin lists.</li>
</ul>
<h3>Demo / test</h3>
<div class="demo-box"><p>Impersonate each role → list data matches ACL expectations.</p></div>
<h2 id="workspace-verify">Workspace verify checklist</h2>
<div class="ok"><p>Complete after Parts 1–4.</p></div>
<ol>
<li>Experience published under HR Leave.</li>
<li>Three pages with correct role gates.</li>
<li>req_v2 list filtered per persona.</li>
</ol>
""")
    return write_chapter(5, "05 — Workspace / UI Builder (Studio From Scratch)", hero, ql, body, 4)


def build_ch06():
    hero = """      <h1>06 — Notifications, Events & Jobs (Studio From Scratch)</h1>
      <p>3 events, 3 email notifications, scheduled accrual job with full script</p>
      <div class="meta-grid">
        <div><strong>Scope</strong><code style="color:#fff">x_786686_hr_leave</code></div>
        <div><strong>sys_id</strong><code style="color:#fff;font-size:.72rem">e5f5bc9493a303507520703efaba104d</code></div>
        <div><strong>Instance lab</strong><code style="color:#fff;font-size:.72rem">dev398980</code></div>
        <div><strong>URL token</strong><code style="color:#fff">{BASE}</code></div>
      </div>"""
    ql = [
        '<a href="{BASE}/sysevent_register_list.do?sysparm_query=event_nameSTARTSWITHx_786686_hr_leave">Events</a>',
        '<a href="{BASE}/sysevent_email_action_list.do?sysparm_query=event_nameSTARTSWITHx_786686_hr_leave">Notifications</a>',
        '<a href="{BASE}/sysauto_script_list.do">Scheduled Jobs</a>',
    ]
    p21 = fix_links(rename_part(extract_part("part-21-events"), 1, "events", "Event Registry"))
    p22 = fix_links(rename_part(extract_part("part-22-notifications"), 2, "notifications", "Notifications"))
    p23 = fix_links(rename_part(extract_part("part-23-job"), 3, "job", "Scheduled Job — Annual Accrual"))
    body = fix_links(intro_ok(
        "Events are queued by BR2 and BR4 from 01 Development. Notifications and accrual job complete the async layer.",
        "05_WORKSPACE_UIBUILDER.html", "05 Workspace",
    ) + """
<h2 id="how-objects-relate">How events, notifications, and jobs relate</h2>
<div class="ok">
<pre style="white-space:pre-wrap;font-family:var(--mono);font-size:.85rem;background:#0b1220;color:#e2e8f0;padding:1rem;border-radius:12px">
BR2 submit → Part 1 Event leave_v2.submitted → Part 2 Notification to approver
BR4 approve/reject → events approved/rejected → Part 2 Notifications to requester
Part 3 Scheduled Job → creates bal_v2 rows from property annual_days
</pre>
</div>
<hr />
""" + RULE0 + """
<hr />
""" + p21 + """
<hr />
""" + p22 + """
<hr />
""" + p23 + """
<h2 id="notif-verify">Notifications & Jobs verify checklist</h2>
<div class="ok"><p>Complete after Parts 1–3.</p></div>
<ol>
<li>Three events registered on req_v2.</li>
<li>Three email notifications active.</li>
<li>Accrual job creates balance rows without duplicates.</li>
</ol>
""")
    return write_chapter(6, "06 — Notifications, Events & Jobs (Studio From Scratch)", hero, ql, body, 3)


def build_ch07():
    hero = """      <h1>07 — Reports & Dashboards (Studio From Scratch)</h1>
      <p>Report Leave Requests by State + dashboard widget — every wizard property</p>
      <div class="meta-grid">
        <div><strong>Scope</strong><code style="color:#fff">x_786686_hr_leave</code></div>
        <div><strong>sys_id</strong><code style="color:#fff;font-size:.72rem">e5f5bc9493a303507520703efaba104d</code></div>
        <div><strong>Instance lab</strong><code style="color:#fff;font-size:.72rem">dev398980</code></div>
        <div><strong>URL token</strong><code style="color:#fff">{BASE}</code></div>
      </div>"""
    ql = ['<a href="{BASE}/sys_report_list.do">Reports</a>', '<a href="{BASE}/$pa_dashboard.do">Dashboards</a>']
    body = fix_links(intro_ok(
        "Build reports in the Reports module wizard — no external tooling.",
        "06_NOTIFICATIONS_EVENTS_JOBS.html", "06 Notifications",
    ) + """
<h2 id="how-objects-relate">How reports and dashboards relate</h2>
<div class="ok"><p>Part 1 Report groups req_v2 by u_state → Part 2 Dashboard embeds report as widget for hr_admin/manager.</p></div>
<hr />
""" + RULE0 + """
<hr />
""" + part_header(1, "report", "Report Wizard — Leave Requests by State") + """
<h3>Purpose</h3>
<p>Visual report grouping leave requests by state.</p>
<h3>Navigation path</h3>
<nav class="section-links"><strong>All &gt;</strong> Reports → Create New</nav>
<h3>Direct URL</h3>
<div class="url-box"><a href="{BASE}/sys_report_list.do">{BASE}/sys_report_list.do</a></div>
<h3>Prerequisites</h3>
<ul><li><a href="01_DEVELOPMENT.html#part-3-table-req">Part 3: Table — Leave Request</a> with seeded mixed states.</li></ul>
<h3>Form fields — Report wizard</h3>
<table class="field-table"><thead><tr><th>Wizard step</th><th>Selection</th></tr></thead><tbody>
<tr><td>1 Source type</td><td>Table</td></tr>
<tr><td>2 Table</td><td>Leave Request [x_786686_hr_leave_req_v2]</td></tr>
<tr><td>3 Report type</td><td>Bar chart or Pie chart</td></tr>
<tr><td>4 Configure</td><td>Group by: State (u_state), Aggregate: Count</td></tr>
<tr><td>5 Title</td><td>Leave Requests by State</td></tr>
<tr><td>Application</td><td>HR Leave</td></tr>
</tbody></table>
<h3>Step-by-step create</h3>
<ol>
<li>Reports → Create New → Table → req_v2.</li>
<li>Choose Bar or Pie → Group by u_state → Count.</li>
<li>Title: Leave Requests by State. Application HR Leave.</li>
<li>Run report → verify segments for draft/submitted/approved.</li>
</ol>
<h3>Verify checklist</h3>
<ul><li>Report renders with correct counts.</li></ul>
<h3>Demo / test</h3>
<div class="demo-box"><p>Seed 2 draft, 3 submitted, 1 approved → chart reflects counts.</p></div>
<hr />
""" + part_header(2, "dashboard", "Dashboard + Widget") + """
<h3>Purpose</h3>
<p>HR Leave dashboard with embedded report widget.</p>
<h3>Navigation path</h3>
<nav class="section-links"><strong>All &gt;</strong> Self-Service → Dashboards</nav>
<h3>Direct URL</h3>
<div class="url-box"><a href="{BASE}/$pa_dashboard.do">{BASE}/$pa_dashboard.do</a></div>
<h3>Prerequisites</h3>
<ul><li><a href="#part-1-report">Part 1: Report Wizard</a>.</li></ul>
<h3>Form fields</h3>
<table class="field-table"><thead><tr><th>Field</th><th>Value</th></tr></thead><tbody>
<tr><td><strong>Name</strong></td><td>HR Leave Dashboard</td></tr>
<tr><td>Widget type</td><td>Report</td></tr>
<tr><td>Report</td><td>Leave Requests by State</td></tr>
<tr><td>Roles</td><td>hr_admin, manager</td></tr>
</tbody></table>
<h3>Step-by-step create</h3>
<ol>
<li>Dashboards → New → Name HR Leave Dashboard.</li>
<li>Add widget → Report → select report from Part 1.</li>
<li>Share with roles hr_admin, manager. Save dashboard.</li>
</ol>
<h3>Verify checklist</h3>
<ul><li>Dashboard widget displays report.</li></ul>
<h3>Demo / test</h3>
<div class="demo-box"><p>manager1 opens dashboard → chart visible.</p></div>
<h2 id="reports-verify">Reports verify checklist</h2>
<ol><li>Report scoped to HR Leave.</li><li>Dashboard shared with manager/hr_admin.</li></ol>
""")
    return write_chapter(7, "07 — Reports & Dashboards (Studio From Scratch)", hero, ql, body, 2)


def build_ch08():
    hero = """      <h1>08 — ATF Testing (Studio From Scratch)</h1>
      <p>Suite HRLX Leave Core + 3 tests with concrete steps</p>
      <div class="meta-grid">
        <div><strong>Scope</strong><code style="color:#fff">x_786686_hr_leave</code></div>
        <div><strong>sys_id</strong><code style="color:#fff;font-size:.72rem">e5f5bc9493a303507520703efaba104d</code></div>
        <div><strong>Instance lab</strong><code style="color:#fff;font-size:.72rem">dev398980</code></div>
        <div><strong>URL token</strong><code style="color:#fff">{BASE}</code></div>
      </div>"""
    ql = ['<a href="{BASE}/sys_atf_test_suite_list.do">Test Suites</a>', '<a href="{BASE}/sys_atf_test_list.do">Tests</a>']
    body = fix_links(intro_ok(
        "ATF runs in-instance after core app from chapters 01–02 exists.",
        "07_REPORTS_DASHBOARDS_PA.html", "07 Reports",
    ) + """
<h2 id="how-objects-relate">How ATF objects relate</h2>
<div class="ok"><p>Part 1 Suite groups Parts 2–4 individual tests (server BR1, client CS2, ACL isolation).</p></div>
<hr />
""" + RULE0 + """
<hr />
""" + part_header(1, "suite", "Test Suite — HRLX Leave Core") + """
<h3>Purpose</h3>
<p>Container suite for all HR Leave automated tests.</p>
<h3>Navigation path</h3>
<nav class="section-links"><strong>All &gt;</strong> Automated Test Framework → Test Suites</nav>
<h3>Direct URL</h3>
<div class="url-box"><a href="{BASE}/sys_atf_test_suite_list.do">{BASE}/sys_atf_test_suite_list.do</a></div>
<h3>Prerequisites</h3>
<ul><li><a href="01_DEVELOPMENT.html#part-1-application">Part 1: Application Setup</a>. ATF plugin active.</li></ul>
<h3>Form fields</h3>
<table class="field-table"><thead><tr><th>Field</th><th>Value</th></tr></thead><tbody>
<tr><td><strong>Name</strong></td><td>HRLX Leave Core</td></tr>
<tr><td><strong>Application</strong></td><td>HR Leave</td></tr>
<tr><td>Active</td><td>true</td></tr>
</tbody></table>
<h3>Step-by-step create</h3>
<ol>
<li>Test Suite → New → fill fields.</li>
<li>After Parts 2–4: Related list Tests → Add all three tests.</li>
<li>Run Suite → all green.</li>
</ol>
<h3>Verify checklist</h3>
<ul><li>Suite lists three tests.</li></ul>
<h3>Demo / test</h3>
<div class="demo-box"><p>Run HRLX Leave Core suite after E2E seed → 3/3 pass.</p></div>
<hr />
""" + part_header(2, "test-server-days", "Test — BR1 Business Days (Server)") + """
<h3>Purpose</h3>
<p>Validates BR1 sets u_days_count = 5 for Mon–Fri range.</p>
<h3>Navigation path</h3>
<nav class="section-links"><strong>All &gt;</strong> ATF → Tests → New</nav>
<h3>Prerequisites</h3>
<ul><li><a href="01_DEVELOPMENT.html#part-8-br1">Part 8: BR1</a> active.</li></ul>
<h3>Form fields</h3>
<table class="field-table"><tr><th>Field</th><th>Value</th></tr>
<tr><td><strong>Name</strong></td><td>HRLX BR1 Days Calculation</td></tr>
<tr><td>Application</td><td>HR Leave</td></tr></table>
<h3>Step-by-step create</h3>
<ol>
<li>ATF → Tests → New → Name: HRLX BR1 Days Calculation.</li>
<li>Step 1: <strong>Create a Record</strong> → Table req_v2 → u_start_date=2026-06-01, u_end_date=2026-06-05, u_state=draft.</li>
<li>Step 2: <strong>Run Server Side Script</strong> → assertion below.</li>
</ol>
<h3>Full script (assertion step)</h3>
<pre><code>(function(outputs, steps, stepResult, assertEqual) {
  var gr = new GlideRecord('x_786686_hr_leave_req_v2');
  gr.get(steps('Create a Record').record_id);
  assertEqual({ name: 'days', expected: '5', actual: gr.getValue('u_days_count') });
})(outputs, steps, stepResult, assertEqual);</code></pre>
<h3>Verify checklist</h3>
<ul><li>Test passes on clean instance.</li></ul>
<h3>Demo / test</h3>
<div class="demo-box"><p>Run test alone → green.</p></div>
<hr />
""" + part_header(3, "test-client-dates", "Test — CS2 Form Days (Client)") + """
<h3>Purpose</h3>
<p>Client test: changing dates on form fills u_days_count via GlideAjax.</p>
<h3>Navigation path</h3>
<nav class="section-links"><strong>All &gt;</strong> ATF → Tests → New (Client test)</nav>
<h3>Prerequisites</h3>
<ul><li><a href="01_DEVELOPMENT.html#part-13-cs2">Part 13: CS2</a> active.</li></ul>
<h3>Form fields</h3>
<table class="field-table"><tr><th>Field</th><th>Value</th></tr>
<tr><td><strong>Name</strong></td><td>HRLX CS2 Form Days</td></tr></table>
<h3>Step-by-step create</h3>
<ol>
<li>New client test: HRLX CS2 Form Days.</li>
<li>Step: Open/New req_v2 form.</li>
<li>Step: Set Field Values u_start_date, u_end_date.</li>
<li>Step: Assert Field Value u_days_count equals 5.</li>
</ol>
<h3>Verify checklist</h3>
<ul><li>Client test passes.</li></ul>
<h3>Demo / test</h3>
<div class="demo-box"><p>Run test → u_days_count populated.</p></div>
<hr />
""" + part_header(4, "test-acl-impersonate", "Test — ACL Employee Isolation (Server)") + """
<h3>Purpose</h3>
<p>Impersonate employee1 → query returns only own req_v2 records.</p>
<h3>Navigation path</h3>
<nav class="section-links"><strong>All &gt;</strong> ATF → Tests → New</nav>
<h3>Prerequisites</h3>
<ul><li><a href="02_ADMINISTRATION.html#part-4-acls">Part 4: ACLs</a> (02).</li></ul>
<h3>Form fields</h3>
<table class="field-table"><tr><th>Field</th><th>Value</th></tr>
<tr><td><strong>Name</strong></td><td>HRLX ACL Employee Isolation</td></tr></table>
<h3>Step-by-step create</h3>
<ol>
<li>Test: HRLX ACL Employee Isolation.</li>
<li>Step: Impersonate user employee1.</li>
<li>Step: Record Query req_v2 → assert count matches only own records.</li>
</ol>
<h3>Verify checklist</h3>
<ul><li>Isolation test passes.</li></ul>
<h3>Demo / test</h3>
<div class="demo-box"><p>Add to suite Part 1 → run full suite.</p></div>
<h2 id="atf-verify">ATF verify checklist</h2>
<ol><li>Three tests in HRLX Leave Core suite.</li><li>Suite runs without failure.</li></ol>
""")
    return write_chapter(8, "08 — ATF Testing (Studio From Scratch)", hero, ql, body, 4)


def build_ch09():
    hero = """      <h1>09 — Modules & Integration (Studio From Scratch)</h1>
      <p>Application Menu, Modules, Flow — full create; cross-module study abbreviated</p>
      <div class="meta-grid">
        <div><strong>Scope</strong><code style="color:#fff">x_786686_hr_leave</code></div>
        <div><strong>sys_id</strong><code style="color:#fff;font-size:.72rem">e5f5bc9493a303507520703efaba104d</code></div>
        <div><strong>Instance lab</strong><code style="color:#fff;font-size:.72rem">dev398980</code></div>
        <div><strong>URL token</strong><code style="color:#fff">{BASE}</code></div>
      </div>"""
    ql = [
        '<a href="{BASE}/sys_app_application_list.do?sysparm_query=name=HR Leave">App Menu</a>',
        '<a href="{BASE}/sys_app_module_list.do?sysparm_query=application.name=HR Leave">Modules</a>',
        '<a href="{BASE}/now/flow-designer">Flow Designer</a>',
    ]
    p24 = fix_links(rename_part(extract_part("part-24-menu"), 1, "menu", "Application Menu"))
    p25 = fix_links(rename_part(extract_part("part-25-modules"), 2, "modules", "Modules"))
    p27 = fix_links(rename_part(extract_part("part-27-flow"), 3, "flow", "Flow Designer — Leave Approval"))
    body = fix_links(intro_ok(
        "Full create steps for navigator and approval flow. Cross-module study is optional reading.",
        "08_ATF_TESTING.html", "08 ATF Testing",
    ) + """
<h2 id="how-objects-relate">How menu, modules, and flow relate</h2>
<div class="ok">
<pre style="white-space:pre-wrap;font-family:var(--mono);font-size:.85rem;background:#0b1220;color:#e2e8f0;padding:1rem;border-radius:12px">
Part 1 Application Menu → Part 2 Modules (4 list links)
Submit (UI Action / Catalog) → Part 3 Flow → Approval → BR3/BR4
</pre>
</div>
<hr />
""" + RULE0 + """
<hr />
""" + p24 + """
<hr />
""" + p25 + """
<hr />
""" + p27 + """
<hr />
""" + part_header(4, "cross-module", "Cross-Module Note") + """
<h3>Purpose</h3>
<p>Optional consultant reading — HR Leave is a scoped custom app; these modules are not required for the lab.</p>
<h3>Navigation path</h3>
<nav class="section-links"><strong>Reference</strong> Module study guides in html/modules/</nav>
<h3>Prerequisites</h3>
<ul><li>Parts 1–3 complete for core HR Leave.</li></ul>
<h3>Related guides</h3>
<ul>
<li><a href="modules/ITSM.html">ITSM</a> — incident/change patterns (not used by this app)</li>
<li><a href="modules/HRSD.html">HRSD</a> — enterprise HR case management (complementary)</li>
<li><a href="12_INTEGRATION_FULL_GUIDE.html">12 Integration</a> — Scripted REST after menu/flow works</li>
</ul>
<h3>Verify checklist</h3>
<ul><li>Core app E2E works without optional modules.</li></ul>
<h3>Demo / test</h3>
<div class="demo-box"><p>employee1 → HR Leave menu → submit → manager approves.</p></div>
<h2 id="modules-verify">Modules verify checklist</h2>
<ol><li>HR Leave menu visible.</li><li>Four modules with correct roles.</li><li>Flow published and approving.</li></ol>
""")
    return write_chapter(9, "09 — Modules & Integration (Studio From Scratch)", hero, ql, body, 4)


SEED_SCRIPT = """(function () {
  var empUser = 'PASTE_EMPLOYEE1_SYS_ID';
  var mgrUser = 'PASTE_MANAGER1_SYS_ID';
  var emp = new GlideRecord('x_786686_hr_leave_employee_v2');
  emp.initialize();
  emp.u_user = empUser;
  emp.u_employee_id = 'E-1001';
  emp.u_department = 'People Ops';
  emp.u_manager = mgrUser;
  emp.u_join_date = '2024-01-15';
  emp.u_grade = 'G5';
  var empId = emp.insert();
  var bal = new GlideRecord('x_786686_hr_leave_bal_v2');
  bal.initialize();
  bal.u_employee_ref = empId;
  bal.u_year = 2026;
  bal.u_leave_type = 'annual';
  bal.u_entitled = parseInt(gs.getProperty('x_786686_hr_leave.config.annual_days', 20), 10);
  bal.u_used = 0;
  bal.u_remaining = bal.u_entitled;
  bal.insert();
  gs.info('Seeded employee=' + empId);
})();"""

E2E_CHECKLIST = """
<ol>
<li><strong>Update Set current</strong> — HR Leave – Build (<a href="01_DEVELOPMENT.html#rule0">Rule 0</a>).</li>
<li><strong>Seed employee</strong> — <a href="01_DEVELOPMENT.html#part-2-table-employee">Part 2: employee_v2</a>, <a href="02_ADMINISTRATION.html#part-3-users">Part 3: Users</a>.</li>
<li><strong>Seed balance</strong> — <a href="01_DEVELOPMENT.html#part-4-table-bal">Part 4: bal_v2</a>.</li>
<li><strong>Create request</strong> — <a href="01_DEVELOPMENT.html#part-3-table-req">Part 3: req_v2</a> OR <a href="03_SERVICE_CATALOG.html#part-2-record-producer">Part 2: Record Producer</a>.</li>
<li><strong>Submit</strong> — <a href="01_DEVELOPMENT.html#part-15-ui-action">Part 15: UI Action</a>, <a href="01_DEVELOPMENT.html#part-9-br2">Part 9: BR2</a>.</li>
<li><strong>Flow approval</strong> — <a href="09_MODULES_AND_INTEGRATION.html#part-3-flow">Part 3: Flow</a>.</li>
<li><strong>Audit</strong> — <a href="01_DEVELOPMENT.html#part-10-br3">Part 10: BR3</a>.</li>
<li><strong>Balance</strong> — BR3 updates bal_v2.</li>
<li><strong>Notification</strong> — <a href="06_NOTIFICATIONS_EVENTS_JOBS.html#part-2-notifications">Part 2: Notifications</a>.</li>
<li><strong>Security</strong> — <a href="02_ADMINISTRATION.html#part-4-acls">Part 4: ACLs</a>.</li>
<li><strong>Portal</strong> — <a href="04_SERVICE_PORTAL.html#part-3-page-home">Part 3: hrlx_home</a>.</li>
<li><strong>REST</strong> — <a href="12_INTEGRATION_FULL_GUIDE.html#part-4-rest-explorer">Part 4: REST Explorer</a>.</li>
</ol>"""


def build_ch10():
    hero = """      <h1>10 — Implementation & Config (Studio From Scratch)</h1>
      <p>E2E UAT checklist, seed data, update set complete/export — professional go-live</p>
      <div class="meta-grid">
        <div><strong>Scope</strong><code style="color:#fff">x_786686_hr_leave</code></div>
        <div><strong>sys_id</strong><code style="color:#fff;font-size:.72rem">e5f5bc9493a303507520703efaba104d</code></div>
        <div><strong>Instance lab</strong><code style="color:#fff;font-size:.72rem">dev398980</code></div>
        <div><strong>URL token</strong><code style="color:#fff">{BASE}</code></div>
      </div>"""
    ql = ['<a href="{BASE}/sys_update_set_list.do">Update Sets</a>', '<a href="{BASE}/x_786686_hr_leave_req_v2_list.do">Leave Requests</a>']
    body = fix_links(intro_ok(
        "Go-live checklist after creating objects via Studio chapters 01–09 (and optional 03–08).",
        "09_MODULES_AND_INTEGRATION.html", "09 Modules",
    ) + """
<h2 id="how-objects-relate">How implementation artifacts relate</h2>
<div class="ok"><p>Seed data → E2E demo → Update Set export → UAT sign-off matrix.</p></div>
<hr />
""" + RULE0 + """
<hr />
""" + part_header(1, "seed-data", "Seed Data") + """
<h3>Purpose</h3>
<p>Lab employee, manager link, and opening balance for E2E demos.</p>
<h3>Navigation path</h3>
<nav class="section-links"><strong>All &gt;</strong> System Definition → Scripts – Background</nav>
<h3>Prerequisites</h3>
<ul><li>Chapters 01–02 complete (tables, users, properties).</li></ul>
<h3>Step-by-step create</h3>
<ol>
<li>Lookup sys_ids for employee1 and manager1 users.</li>
<li>Run background script below as admin, Application = HR Leave.</li>
<li>Verify employee_v2 and bal_v2 rows.</li>
</ol>
<h3>Full script (paste-ready)</h3>
<pre><code>""" + SEED_SCRIPT + """</code></pre>
<h3>Verify checklist</h3>
<ul><li>employee_v2 links employee1 → manager1.</li><li>bal_v2 year 2026 with entitled from property.</li></ul>
<h3>Demo / test</h3>
<div class="demo-box"><p>employee1 creates req_v2 → BR1 sets approver manager1.</p></div>
<hr />
""" + part_header(2, "e2e-checklist", "E2E Demo Checklist") + """
<h3>Purpose</h3>
<p>Prove full leave lifecycle from draft/submit through approval, audit, balance, notifications, portal, REST.</p>
<h3>Prerequisites</h3>
<ul><li><a href="#part-1-seed-data">Part 1: Seed Data</a>.</li></ul>
<h3>Verify checklist</h3>
<div class="ok"><p>Complete after Application Setup through Flow (extended: Portal, REST).</p></div>
""" + fix_links(E2E_CHECKLIST) + """
<h3>Demo / test</h3>
<div class="demo-box"><p>Walk checklist top-to-bottom as three personas.</p></div>
<hr />
""" + part_header(3, "update-set-export", "Update Set Export") + """
<h3>Purpose</h3>
<p>Complete and export HR Leave – Build for target instance promotion.</p>
<h3>Navigation path</h3>
<nav class="section-links"><strong>All &gt;</strong> System Update Sets → Local Update Sets</nav>
<h3>Direct URL</h3>
<div class="url-box"><a href="{BASE}/sys_update_set_list.do">Local Update Sets</a> · <a href="{BASE}/sys_remote_update_set_list.do">Retrieved Update Sets</a></div>
<h3>Form fields</h3>
<table class="field-table"><tr><th>Field</th><th>Value</th></tr>
<tr><td>Name</td><td>HR Leave – Build</td></tr>
<tr><td>State</td><td>Complete</td></tr>
<tr><td>Application</td><td>HR Leave</td></tr></table>
<h3>Step-by-step create</h3>
<ol>
<li>HR Leave – Build → State = Complete.</li>
<li>Export via Retrieved Update Sets or XML per process.</li>
<li>Target: Import → Preview → Commit.</li>
<li>Post-import: users/groups if missing; verify 9 properties; run accrual job once.</li>
<li>Smoke test: employee1 submit → manager1 approve → balance updated.</li>
</ol>
<div class="warn"><p>Never promote Global artifacts. Confirm Application = HR Leave on every captured file.</p></div>
<h3>Verify checklist</h3>
<ul><li>Customer Updates lists all scoped artifacts.</li></ul>
<h3>Demo / test</h3>
<div class="demo-box"><p>Import to second PDI → smoke test.</p></div>
<hr />
""" + part_header(4, "uat-matrix", "UAT Matrix") + """
<h3>Purpose</h3>
<p>Sign-off matrix for lab personas and expected outcomes.</p>
<h3>Form fields — test matrix</h3>
<table class="field-table"><thead><tr><th>Persona</th><th>Test</th><th>Expected</th></tr></thead><tbody>
<tr><td>employee1</td><td>Create + submit leave</td><td>State submitted, approver = manager1</td></tr>
<tr><td>manager1</td><td>Approve in My Approvals</td><td>State approved, notification sent</td></tr>
<tr><td>hradmin</td><td>View all modules</td><td>Employees, Balances, Audit visible</td></tr>
<tr><td>employee1</td><td>Open coworker req URL</td><td>ACL denied</td></tr>
</tbody></table>
<p>Seed values: <a href="SCHEMA_AND_DATA.html">SCHEMA_AND_DATA.html</a></p>
<h3>Verify checklist</h3>
<ul><li>All four UAT rows pass.</li></ul>
<h3>Demo / test</h3>
<div class="demo-box"><p>Record pass/fail per row before go-live.</p></div>
<h2 id="admin-verify">Implementation verify checklist</h2>
<ol><li>Seed data present.</li><li>E2E checklist green.</li><li>Update Set exported.</li><li>UAT matrix signed.</li></ol>
""")
    return write_chapter(10, "10 — Implementation & Config (Studio From Scratch)", hero, ql, body, 4)


def build_ch11():
    hero = """      <h1>11 — Studio Practice Companion</h1>
      <p>Day-to-day Studio workflow — points to chapters 01–12. No external CLI.</p>
      <div class="meta-grid">
        <div><strong>Scope</strong><code style="color:#fff">x_786686_hr_leave</code></div>
        <div><strong>sys_id</strong><code style="color:#fff;font-size:.72rem">e5f5bc9493a303507520703efaba104d</code></div>
        <div><strong>Instance lab</strong><code style="color:#fff;font-size:.72rem">dev398980</code></div>
        <div><strong>URL token</strong><code style="color:#fff">{BASE}</code></div>
      </div>"""
    ql = ['<a href="{BASE}/$studio.do">Studio</a>', '<a href="scripts/index.html">Scripts portal</a>']
    body = fix_links(intro_ok(
        "Studio practice companion only. Build the core app via 01 Development and Studio Create All first.",
        "10_IMPLEMENTATION_AND_CONFIG.html", "10 Implementation",
    ) + """
<h2 id="how-objects-relate">How chapters map to Studio work</h2>
<div class="ok"><p>Part 1 daily workflow → Part 2 object-type table (chapters 01–12) → Part 3 scripts portal for paste-ready code.</p></div>
<hr />
""" + RULE0 + """
<hr />
""" + part_header(1, "daily-workflow", "Daily Workflow in Studio") + """
<h3>Purpose</h3>
<p>Repeatable steps every time you create or edit HR Leave artifacts.</p>
<h3>Navigation path</h3>
<nav class="section-links"><strong>All &gt;</strong> Studio → HR Leave application</nav>
<h3>Step-by-step create</h3>
<ol>
<li>Set Application picker to <strong>HR Leave</strong> (<code>x_786686_hr_leave</code>).</li>
<li>Set Local Update Set current (HR Leave – Build).</li>
<li>Open <a href="{BASE}/$studio.do">Studio</a> → select HR Leave.</li>
<li>Create Application File → choose type (Table, Business Rule, Client Script, Script Include, …).</li>
<li>Fill every form field from the matching chapter Part section.</li>
<li>Paste script from embedded <code>&lt;pre&gt;</code> blocks or <a href="scripts/index.html">Scripts portal</a>.</li>
<li>Save → open list/form URL → run Verify + Demo for that Part.</li>
</ol>
<h3>Verify checklist</h3>
<ul><li>Customer Updates shows new artifact in HR Leave – Build.</li></ul>
<h3>Demo / test</h3>
<div class="demo-box"><p>One object per session: create → verify → demo before moving on.</p></div>
<hr />
""" + part_header(2, "object-type-table", "Object Type → Chapter Map (01–12)") + """
<h3>Purpose</h3>
<p>Quick lookup: which chapter documents each ServiceNow object type.</p>
<table class="field-table"><thead><tr><th>Object</th><th>Studio / Navigation</th><th>Chapter · Part</th></tr></thead><tbody>
<tr><td>Application / Tables / SI / BR / CS / UI</td><td>Studio → Create Application File</td><td><a href="01_DEVELOPMENT.html">01</a> Parts 1–15</td></tr>
<tr><td>Roles / Groups / Users / ACLs / Properties</td><td>Security / User Administration</td><td><a href="02_ADMINISTRATION.html">02</a> Parts 1–6</td></tr>
<tr><td>Record Producer / Category</td><td>Service Catalog</td><td><a href="03_SERVICE_CATALOG.html">03</a> Parts 1–5</td></tr>
<tr><td>Portal widgets / Page</td><td>Service Portal</td><td><a href="04_SERVICE_PORTAL.html">04</a> Parts 1–3</td></tr>
<tr><td>UI Builder workspace</td><td>Now Experience → UI Builder</td><td><a href="05_WORKSPACE_UIBUILDER.html">05</a> Parts 1–4</td></tr>
<tr><td>Events / Notifications / Jobs</td><td>System Policy / System Definition</td><td><a href="06_NOTIFICATIONS_EVENTS_JOBS.html">06</a> Parts 1–3</td></tr>
<tr><td>Reports / Dashboard</td><td>Reports / Dashboards</td><td><a href="07_REPORTS_DASHBOARDS_PA.html">07</a> Parts 1–2</td></tr>
<tr><td>ATF</td><td>Automated Test Framework</td><td><a href="08_ATF_TESTING.html">08</a> Parts 1–4</td></tr>
<tr><td>Menu / Modules / Flow</td><td>Application Menus / Flow Designer</td><td><a href="09_MODULES_AND_INTEGRATION.html">09</a> Parts 1–3</td></tr>
<tr><td>Seed / UAT / Update Set</td><td>Background scripts / Update Sets</td><td><a href="10_IMPLEMENTATION_AND_CONFIG.html">10</a> Parts 1–4</td></tr>
<tr><td>Scripted REST</td><td>System Web Services</td><td><a href="12_INTEGRATION_FULL_GUIDE.html">12</a> Parts 1–4</td></tr>
</tbody></table>
<h3>Verify checklist</h3>
<ul><li>Every row links to a chapter with Part anchors (not OBJ).</li></ul>
<hr />
""" + part_header(3, "scripts-portal", "Scripts Portal") + """
<h3>Purpose</h3>
<p>Browse paste-ready scripts mirrored from <code>HR_Leave_App/src/</code> on disk.</p>
<h3>Navigation path</h3>
<nav class="section-links"><strong>Local</strong> <a href="scripts/index.html">Scripts portal</a> · <strong>Studio paste</strong> matching chapter Part Full script blocks</nav>
<h3>Direct URL</h3>
<div class="url-box"><a href="scripts/index.html">scripts/index.html</a> · <a href="15_CLAUDE_CLI_CODE_SERVICENOW.html">15 Scripts mapping</a></div>
<h3>Step-by-step create</h3>
<ol>
<li>Open Scripts portal → find script by name (e.g. RP_submit_leave.js, annual_accrual.js).</li>
<li>Copy from HTML pre block OR open chapter Part Full script section.</li>
<li>Paste into Studio form Script field while Application = HR Leave.</li>
</ol>
<h3>Verify checklist</h3>
<ul><li>Script saves without syntax errors in Studio.</li></ul>
<h3>Demo / test</h3>
<div class="demo-box"><p><a href="STUDIO_CREATE_ALL_OBJECTS_01_16.html">Studio Create All Objects</a> · <a href="16_SDK_FULL_DEV_ADMIN_FROM_SCRATCH.html">16 Master Path</a></p></div>
<h2 id="practice-verify">Practice companion verify checklist</h2>
<ol><li>Workflow habit: picker + Update Set before every create.</li><li>Object table bookmarked.</li><li>Scripts portal used for paste source.</li></ol>
""")
    return write_chapter(11, "11 — Studio Practice Companion", hero, ql, body, 3)


def build_ch12():
    p32 = extract_part("part-32-rest")
    si_block = extract_between(p32, "<h3>Full script — HRLXProIntegrationUtilsV2", "<h3>Form fields — Scripted REST API")
    rest_fields = extract_between(p32, "<h3>Form fields — Scripted REST API", "<h3>Form fields — Resource POST /leave")
    resource_fields = extract_between(p32, "<h3>Form fields — Resource POST /leave", "<h3>Full script — Resource (POST /leave)")
    resource_script = extract_between(p32, "<h3>Full script — Resource (POST /leave)", "<h3>Step-by-step create")
    steps_block = extract_between(p32, "<h3>Step-by-step create", "<h3>Verify checklist")
    verify_block = extract_between(p32, "<h3>Verify checklist", "<h3>Demo / test")
    demo_block = extract_between(p32, "<h3>Demo / test", "<hr />")
    hero = """      <h1>12 — Integration Full Guide (Studio From Scratch)</h1>
      <p>Scripted REST + Integration Script Include — REST Explorer test</p>
      <div class="meta-grid">
        <div><strong>Scope</strong><code style="color:#fff">x_786686_hr_leave</code></div>
        <div><strong>sys_id</strong><code style="color:#fff;font-size:.72rem">e5f5bc9493a303507520703efaba104d</code></div>
        <div><strong>Instance lab</strong><code style="color:#fff;font-size:.72rem">dev398980</code></div>
        <div><strong>URL token</strong><code style="color:#fff">{BASE}</code></div>
      </div>"""
    ql = ['<a href="{BASE}/$restapi.do">REST API Explorer</a>', '<a href="{BASE}/sys_ws_definition_list.do">Scripted REST APIs</a>']
    body = fix_links(intro_ok(
        "Scripted REST + Integration Script Include — create in ServiceNow UI only. Test with REST API Explorer.",
        "11_SDK_CURSOR_CLAUDE.html", "11 Studio Practice",
    ) + """
<h2 id="how-objects-relate">How integration objects relate</h2>
<div class="ok">
<pre style="white-space:pre-wrap;font-family:var(--mono);font-size:.85rem;background:#0b1220;color:#e2e8f0;padding:1rem;border-radius:12px">
Part 1 HRLXProIntegrationUtilsV2 (SI)
  └── Part 2 REST API definition (hrlx_api_v2)
        └── Part 3 POST /leave resource script
              └── Part 4 REST Explorer test (201 + sys_id)
</pre>
</div>
<hr />
""" + RULE0 + """
<hr />
""" + part_header(1, "integration-si", "Script Include — HRLXProIntegrationUtilsV2") + """
<h3>Purpose</h3>
<p>Inbound create + outbound ERP push helpers for REST integration.</p>
<h3>Navigation path</h3>
<nav class="section-links"><strong>All &gt;</strong> Studio → Script Include</nav>
<h3>Direct URL</h3>
<div class="url-box"><a href="{BASE}/sys_script_include_list.do?sysparm_query=name=HRLXProIntegrationUtilsV2">{BASE}/sys_script_include_list.do</a></div>
<h3>Prerequisites</h3>
<ul>
<li><a href="02_ADMINISTRATION.html#part-1-roles">Part 1: Roles</a> integration role.</li>
<li><a href="01_DEVELOPMENT.html#part-3-table-req">Part 3: req_v2</a>.</li>
</ul>
<h3>Form fields</h3>
<table class="field-table"><thead><tr><th>Field</th><th>Value</th></tr></thead><tbody>
<tr><td><strong>Name</strong></td><td>HRLXProIntegrationUtilsV2</td></tr>
<tr><td>Client callable</td><td>false</td></tr>
<tr><td>Active</td><td>true</td></tr>
<tr><td>Application</td><td>HR Leave</td></tr>
</tbody></table>
<h3>Step-by-step create</h3>
<ol><li>Studio → Script Include → New → fill fields → paste script → Save.</li></ol>
""" + si_block + """
<h3>Verify checklist</h3>
<ul><li>Script Include active under HR Leave.</li></ul>
<h3>Demo / test</h3>
<div class="demo-box"><p>Background: <code>new x_786686_hr_leave.HRLXProIntegrationUtilsV2()</code> instantiates.</p></div>
<hr />
""" + part_header(2, "rest-api", "Scripted REST API Definition") + """
<h3>Purpose</h3>
<p>Defines scoped API hrlx_api_v2 with authentication and default ACLs.</p>
<h3>Navigation path</h3>
<nav class="section-links"><strong>All &gt;</strong> System Web Services → Scripted REST APIs</nav>
<h3>Direct URL</h3>
<div class="url-box"><a href="{BASE}/sys_ws_definition_list.do">{BASE}/sys_ws_definition_list.do</a></div>
<h3>Prerequisites</h3>
<ul><li><a href="#part-1-integration-si">Part 1: Integration SI</a>.</li></ul>
""" + rest_fields + """
<h3>Step-by-step create</h3>
<ol>
<li>Scripted REST APIs → New → fill API fields.</li>
<li>Security → Default ACLs → execute requires integration role.</li>
<li>Submit API record before adding resource in Part 3.</li>
</ol>
<h3>Verify checklist</h3>
<ul><li>API ID hrlx_api_v2 under HR Leave (not Global).</li></ul>
<h3>Demo / test</h3>
<div class="demo-box"><p>API appears in REST Explorer namespace list.</p></div>
<hr />
""" + part_header(3, "post-leave", "Resource Script — POST /leave") + """
<h3>Purpose</h3>
<p>POST /api/x_786686_hr_leave/hrlx_api_v2/leave creates submitted req_v2 from JSON.</p>
<h3>Navigation path</h3>
<nav class="section-links"><strong>All &gt;</strong> Scripted REST API → Resources → New</nav>
<h3>Prerequisites</h3>
<ul><li><a href="#part-2-rest-api">Part 2: REST API Definition</a>.</li><li>employee_v2 with u_employee_id = EMP001.</li></ul>
""" + resource_fields + """
<h3>Step-by-step create</h3>
<ol><li>Related Resources → New → POST /leave → paste resource script → Submit.</li></ol>
""" + resource_script + """
<h3>Verify checklist</h3>
<ul><li>Resource active; path /leave relative to API.</li></ul>
<h3>Demo / test</h3>
<div class="demo-box"><p>Test in Part 4 REST Explorer.</p></div>
<hr />
""" + part_header(4, "rest-explorer", "REST Explorer Test") + """
<h3>Purpose</h3>
<p>Validate inbound POST returns 201 and creates req_v2 as integration user.</p>
<h3>Navigation path</h3>
<nav class="section-links"><strong>All &gt;</strong> System Web Services → REST API Explorer</nav>
<h3>Direct URL</h3>
<div class="url-box"><a href="{BASE}/$restapi.do">{BASE}/$restapi.do</a> · Endpoint: <code>/api/x_786686_hr_leave/hrlx_api_v2/leave</code></div>
<h3>Prerequisites</h3>
<ul><li>Parts 1–3 complete.</li><li>User hrlx.integration with integration + rest_service roles.</li></ul>
<h3>Step-by-step create</h3>
""" + steps_block.replace("<h3>Step-by-step create</h3>", "") + """
<h3>Verify checklist</h3>
""" + verify_block.replace("<h3>Verify checklist</h3>", "") + """
<h3>Demo / test</h3>
""" + demo_block + """
<h2 id="integration-verify">Integration verify checklist</h2>
<ol><li>SI + API + resource scoped to HR Leave.</li><li>POST returns 201.</li><li>req_v2 row in submitted state.</li><li>403 without integration role.</li></ol>
""")
    return write_chapter(12, "12 — Integration Full Guide (Studio From Scratch)", hero, ql, body, 4)


def build_ch13():
    hero = """      <h1>13 — 2-Hour Master Summary (Studio Revision)</h1>
      <p>Revision checklist linking chapter Parts — Studio only</p>
      <div class="meta-grid">
        <div><strong>Scope</strong><code style="color:#fff">x_786686_hr_leave</code></div>
        <div><strong>sys_id</strong><code style="color:#fff;font-size:.72rem">e5f5bc9493a303507520703efaba104d</code></div>
        <div><strong>Instance lab</strong><code style="color:#fff;font-size:.72rem">dev398980</code></div>
        <div><strong>URL token</strong><code style="color:#fff">{BASE}</code></div>
      </div>"""
    ql = ['<a href="STUDIO_CREATE_ALL_OBJECTS_01_16.html">Studio Create All</a>', '<a href="16_SDK_FULL_DEV_ADMIN_FROM_SCRATCH.html">16 Master Path</a>']
    checklist_table = """
<table class="field-table"><thead><tr><th>Area</th><th>Object</th><th>Chapter · Part</th></tr></thead><tbody>
<tr><td>00</td><td>Update Set HR Leave – Build</td><td><a href="01_DEVELOPMENT.html#rule0">01 Rule 0</a></td></tr>
<tr><td>01</td><td>Application HR Leave</td><td><a href="01_DEVELOPMENT.html#part-1-application">01 Part 1</a></td></tr>
<tr><td>02–05</td><td>Tables employee/req/bal/audit _v2</td><td><a href="01_DEVELOPMENT.html#part-2-table-employee">01 Parts 2–5</a></td></tr>
<tr><td>06–07</td><td>Script Includes</td><td><a href="01_DEVELOPMENT.html#part-6-script-include-leave">01 Parts 6–7</a></td></tr>
<tr><td>08–11</td><td>BR1–BR4</td><td><a href="01_DEVELOPMENT.html#part-8-br1">01 Parts 8–11</a></td></tr>
<tr><td>12–15</td><td>CS, UI Policy, UI Action, Menu, Flow</td><td><a href="01_DEVELOPMENT.html#part-12-cs1">01 Parts 12–15+</a></td></tr>
<tr><td>16–20</td><td>Roles, Groups, Users, ACLs, Properties</td><td><a href="02_ADMINISTRATION.html#part-1-roles">02 Parts 1–5</a></td></tr>
<tr><td>21–23</td><td>Events, Notifications, Job</td><td><a href="06_NOTIFICATIONS_EVENTS_JOBS.html#part-1-events">06 Parts 1–3</a></td></tr>
<tr><td>24–27</td><td>Menu, Modules, Flow</td><td><a href="09_MODULES_AND_INTEGRATION.html#part-1-menu">09 Parts 1–3</a></td></tr>
<tr><td>26</td><td>Record Producer</td><td><a href="03_SERVICE_CATALOG.html#part-2-record-producer">03 Part 2</a></td></tr>
<tr><td>28</td><td>Portal widgets + page</td><td><a href="04_SERVICE_PORTAL.html#part-1-widget-my-leaves">04 Parts 1–3</a></td></tr>
<tr><td>29</td><td>UI Builder workspace</td><td><a href="05_WORKSPACE_UIBUILDER.html#part-1-workspace">05 Parts 1–4</a></td></tr>
<tr><td>30</td><td>Report + Dashboard</td><td><a href="07_REPORTS_DASHBOARDS_PA.html#part-1-report">07 Parts 1–2</a></td></tr>
<tr><td>31</td><td>ATF suite</td><td><a href="08_ATF_TESTING.html#part-1-suite">08 Parts 1–4</a></td></tr>
<tr><td>32</td><td>Scripted REST</td><td><a href="12_INTEGRATION_FULL_GUIDE.html#part-2-rest-api">12 Parts 1–4</a></td></tr>
</tbody></table>"""
    body = fix_links(intro_ok(
        "2-hour revision checklist — confirm every Part exists before demo or interview.",
        "12_INTEGRATION_FULL_GUIDE.html", "12 Integration",
    ) + """
<h2 id="how-objects-relate">Revision map</h2>
<div class="ok"><p>Part 1 quick checklist → Part 2 E2E demo → Part 3 optional gaps.</p></div>
<hr />
""" + RULE0 + """
<hr />
""" + part_header(1, "quick-checklist", "Quick Checklist (Chapter Parts)") + """
<h3>Purpose</h3>
<p>Fast pass/fail review of all create objects linked by chapter Part anchors.</p>
<h3>Verify checklist</h3>
""" + fix_links(checklist_table) + """
<hr />
""" + part_header(2, "e2e-demo", "E2E Demo") + """
<h3>Purpose</h3>
<p>Single scripted walkthrough proving leave lifecycle.</p>
<div class="ok"><p>Complete after core Parts through Flow (extended: Portal, REST).</p></div>
""" + fix_links(E2E_CHECKLIST) + """
<h3>Demo / test</h3>
<div class="demo-box"><p>Timebox: 30 minutes for full E2E as three personas.</p></div>
<hr />
""" + part_header(3, "gaps-optional", "Gaps (Optional)") + """
<h3>Purpose</h3>
<p>Items often skipped in a 2-hour sprint — schedule if time allows.</p>
<ul>
<li><a href="05_WORKSPACE_UIBUILDER.html">05 Workspace</a> — Now Experience lists</li>
<li><a href="07_REPORTS_DASHBOARDS_PA.html">07 Reports</a> — dashboard for managers</li>
<li><a href="08_ATF_TESTING.html">08 ATF</a> — regression suite</li>
<li><a href="12_INTEGRATION_FULL_GUIDE.html">12 REST</a> — inbound POST /leave</li>
<li><a href="14_AI_SERVICENOW_AGENTS.html">14 AI Agents</a> — platform AI (post core app)</li>
</ul>
<h3>Verify checklist</h3>
<ul><li>Core path (01, 02, 03, 06, 09, 10) complete before optional gaps.</li></ul>
<h3>Demo / test</h3>
<div class="demo-box"><p><a href="16_SDK_FULL_DEV_ADMIN_FROM_SCRATCH.html#part-3-e2e-gate">16 Part 3 E2E gate</a></p></div>
<h2 id="summary-verify">Summary verify checklist</h2>
<ol><li>All Part links resolve.</li><li>E2E demo passes.</li><li>Gaps documented if deferred.</li></ol>
""")
    return write_chapter(13, "13 — 2-Hour Master Summary (Studio Revision)", hero, ql, body, 3)


def build_ch14():
    existing = (HTML_DIR / "14_AI_SERVICENOW_AGENTS.html").read_text(encoding="utf-8")
    m = re.search(r"<article class=\"content\">(.*)", existing, re.S)
    ai_body = m.group(1) if m else ""
    ai_body = re.sub(r"\s*<nav class=\"chapter-nav\">.*?</html>\s*", "", ai_body, flags=re.S)
    ai_body = re.sub(r"\s*</article>.*", "", ai_body, flags=re.S)
    # Strip wrapper-only SDK refs from first ~40 lines of old content; keep deep AI sections
    ai_body = re.sub(
        r"<div class=\"warn\">.*?</div>\s*<div class=\"ok\">.*?</div>\s*<p class=\"nav-coverage\">.*?</p>\s*",
        "",
        ai_body,
        count=1,
        flags=re.S,
    )
    hero = """      <h1>14 — AI in ServiceNow + Agents</h1>
      <p>Platform AI features after core Studio app (01–12) exists.</p>
      <div class="meta-grid">
        <div><strong>Scope</strong><code style="color:#fff">x_786686_hr_leave</code></div>
        <div><strong>sys_id</strong><code style="color:#fff;font-size:.72rem">e5f5bc9493a303507520703efaba104d</code></div>
        <div><strong>Instance lab</strong><code style="color:#fff;font-size:.72rem">dev398980</code></div>
        <div><strong>URL token</strong><code style="color:#fff">{BASE}</code></div>
      </div>"""
    ql = ['<a href="{BASE}/now/assist">Now Assist</a>']
    wrapper = fix_links("""
<div class="warn"><p><strong>Prerequisite:</strong> Create the core HR Leave app via Studio chapters <a href="01_DEVELOPMENT.html">01</a> through <a href="12_INTEGRATION_FULL_GUIDE.html">12</a> before enabling AI features. All tables, BR, Flow, and ACLs must exist on the instance.</p></div>
<div class="ok"><p><strong>Studio-only for core app.</strong> AI configuration uses ServiceNow platform UI (Now Assist, AI Agent Studio, Virtual Agent). Build core artifacts in Studio first.</p></div>

<h2 id="how-objects-relate">How AI features relate to HR Leave</h2>
<div class="ok">
<pre style="white-space:pre-wrap;font-family:var(--mono);font-size:.85rem;background:#0b1220;color:#e2e8f0;padding:1rem;border-radius:12px">
Core app (ch.01–12) — tables, BR, Flow, ACLs
        │
        ▼
Platform AI (this chapter) — Now Assist, Agents, VA, Search
        │
        ▼
Optional: HR Leave skills/topics referencing req_v2 / bal_v2 data
</pre>
<p>AI layers sit <em>on top of</em> the scoped app — they do not replace Studio create steps in chapters 01–12.</p>
</div>

<hr />

""" + RULE0 + """

<hr />

<p><em>Deep-dive sections below — original AI implementation guide content.</em></p>
<hr />
""")
    body = wrapper + fix_links(ai_body)
    part_count = len(re.findall(r'<h2 id="part-', body))
    return write_chapter(14, "14 — AI in ServiceNow + Agents", hero, ql, body, max(part_count, 1))


def build_ch15():
    hero = """      <h1>15 — Scripts: Copy Into Studio Only</h1>
      <p>Paste-ready script mapping — link to chapter Parts, do not duplicate huge scripts here</p>
      <div class="meta-grid">
        <div><strong>Scope</strong><code style="color:#fff">x_786686_hr_leave</code></div>
        <div><strong>sys_id</strong><code style="color:#fff;font-size:.72rem">e5f5bc9493a303507520703efaba104d</code></div>
        <div><strong>Instance lab</strong><code style="color:#fff;font-size:.72rem">dev398980</code></div>
        <div><strong>URL token</strong><code style="color:#fff">{BASE}</code></div>
      </div>"""
    ql = ['<a href="scripts/index.html">Scripts portal</a>', '<a href="{BASE}/$studio.do">Studio</a>']
    body = fix_links(intro_ok(
        "Use AI assistants or local editors to draft code, then paste into matching ServiceNow Studio forms while Application = HR Leave.",
        "14_AI_SERVICENOW_AGENTS.html", "14 AI Agents",
    ) + """
<h2 id="how-objects-relate">How script files map to chapters</h2>
<div class="ok"><p>Part 1 paste workflow → Part 2 mapping table (file → chapter Part). Full scripts live in linked Parts — not duplicated here.</p></div>
<hr />
""" + RULE0 + """
<hr />
""" + part_header(1, "paste-studio", "Paste Into Studio Instructions") + """
<h3>Purpose</h3>
<p>Standard workflow for copying scripts from disk or Scripts portal into Studio forms.</p>
<h3>Navigation path</h3>
<nav class="section-links"><strong>All &gt;</strong> Studio → HR Leave → open target object → Script field</nav>
<h3>Step-by-step create</h3>
<ol>
<li>Application picker = <strong>HR Leave</strong> (<code>x_786686_hr_leave</code>).</li>
<li>Update Set <strong>HR Leave – Build</strong> = current.</li>
<li>Open the chapter Part for the object (form fields + navigation path).</li>
<li>Open matching file under <code>HR_Leave_App/src/</code> OR <a href="scripts/index.html">Scripts portal</a>.</li>
<li>Copy entire script — include header comment block.</li>
<li>Paste into Studio Script field (Business Rule, Script Include, Record Producer, Widget server, etc.).</li>
<li>Save → run that Part Verify + Demo checklist.</li>
</ol>
<div class="warn"><p>Do not paste into Global-scoped records. Confirm Application = HR Leave on the form before save.</p></div>
<h3>Verify checklist</h3>
<ul><li>No syntax errors on save.</li><li>Customer Updates captures the script change.</li></ul>
<h3>Demo / test</h3>
<div class="demo-box"><p>One script at a time: paste → save → verify behavior before next file.</p></div>
<hr />
""" + part_header(2, "mapping-table", "Script File → Chapter Part Mapping") + """
<h3>Purpose</h3>
<p>Quick index: which source file maps to which chapter Part (links — not full script bodies).</p>
<table class="field-table"><thead><tr><th>Source file (src/)</th><th>Object</th><th>Chapter · Part (Full script)</th></tr></thead><tbody>
<tr><td><code>server/script_includes/HRLXProLeaveUtilsV2.js</code></td><td>Script Include</td><td><a href="01_DEVELOPMENT.html#part-6-script-include-leave">01 Part 6</a></td></tr>
<tr><td><code>server/script_includes/HRLXProSecurityUtilsV2.js</code></td><td>Script Include</td><td><a href="01_DEVELOPMENT.html#part-7-script-include-security">01 Part 7</a></td></tr>
<tr><td><code>server/business_rules/BR1_calculate_days.js</code></td><td>Business Rule</td><td><a href="01_DEVELOPMENT.html#part-8-br1">01 Part 8</a></td></tr>
<tr><td><code>server/business_rules/BR2_on_submit_event.js</code></td><td>Business Rule</td><td><a href="01_DEVELOPMENT.html#part-9-br2">01 Part 9</a></td></tr>
<tr><td><code>server/business_rules/BR3_audit_state_change.js</code></td><td>Business Rule</td><td><a href="01_DEVELOPMENT.html#part-10-br3">01 Part 10</a></td></tr>
<tr><td><code>server/business_rules/BR4_on_approve_reject_event.js</code></td><td>Business Rule</td><td><a href="01_DEVELOPMENT.html#part-11-br4">01 Part 11</a></td></tr>
<tr><td><code>client/client_scripts/CS1_validate_dates.js</code></td><td>Client Script</td><td><a href="01_DEVELOPMENT.html#part-12-cs1">01 Part 12</a></td></tr>
<tr><td><code>client/client_scripts/CS2_calc_days_glideajax.js</code></td><td>Client Script</td><td><a href="01_DEVELOPMENT.html#part-13-cs2">01 Part 13</a></td></tr>
<tr><td><code>catalog/RP_submit_leave.js</code></td><td>Record Producer</td><td><a href="03_SERVICE_CATALOG.html#part-4-producer-script">03 Part 4</a></td></tr>
<tr><td><code>server/scheduled_jobs/annual_accrual.js</code></td><td>Scheduled Job</td><td><a href="06_NOTIFICATIONS_EVENTS_JOBS.html#part-3-job">06 Part 3</a></td></tr>
<tr><td><code>portal/widgets/hrlx_my_leaves/*.js</code></td><td>Widget client/server</td><td><a href="04_SERVICE_PORTAL.html#part-1-widget-my-leaves">04 Part 1</a></td></tr>
<tr><td><code>portal/widgets/hrlx_balance/*.js</code></td><td>Widget client/server</td><td><a href="04_SERVICE_PORTAL.html#part-2-widget-balance">04 Part 2</a></td></tr>
<tr><td><code>server/script_includes/HRLXProIntegrationUtilsV2.js</code></td><td>Script Include</td><td><a href="12_INTEGRATION_FULL_GUIDE.html#part-1-integration-si">12 Part 1</a></td></tr>
<tr><td><code>server/rest/inbound_scripted_rest_leave.js</code></td><td>REST resource</td><td><a href="12_INTEGRATION_FULL_GUIDE.html#part-3-post-leave">12 Part 3</a></td></tr>
</tbody></table>
<p>Browse all: <a href="scripts/index.html">Scripts portal</a> · Inventory: <a href="SCRIPTS_INVENTORY.html">SCRIPTS_INVENTORY.html</a></p>
<h3>Verify checklist</h3>
<ul><li>Every row opens a Part with Full script block.</li></ul>
<h3>Demo / test</h3>
<div class="demo-box"><p>Pick one row → paste → run linked Part demo.</p></div>
<h2 id="scripts-verify">Scripts chapter verify checklist</h2>
<ol><li>Paste workflow followed.</li><li>Mapping table covers BR, SI, catalog, job, portal, REST.</li></ol>
""")
    return write_chapter(15, "15 — Scripts: Copy Into Studio Only", hero, ql, body, 2)


def build_ch16():
    hero = """      <h1>16 — Studio From Scratch Master Path</h1>
      <p>Ordered create path 01→15 with Part anchors, master links, E2E gate</p>
      <div class="meta-grid">
        <div><strong>Scope</strong><code style="color:#fff">x_786686_hr_leave</code></div>
        <div><strong>sys_id</strong><code style="color:#fff;font-size:.72rem">e5f5bc9493a303507520703efaba104d</code></div>
        <div><strong>Instance lab</strong><code style="color:#fff;font-size:.72rem">dev398980</code></div>
        <div><strong>URL token</strong><code style="color:#fff">{BASE}</code></div>
      </div>"""
    ql = [
        '<a href="STUDIO_CREATE_ALL_OBJECTS_01_16.html">Studio Create All Objects</a>',
        '<a href="PROFESSIONAL_HR_CREATE_PROPERTIES_AND_LINKS.html">Properties + Links</a>',
    ]
    path_table = """
<table class="field-table"><thead><tr><th>Order</th><th>Chapter</th><th>Parts</th><th>Start anchor</th></tr></thead><tbody>
<tr><td>1</td><td><a href="01_DEVELOPMENT.html">01 Development</a></td><td>15+</td><td><a href="01_DEVELOPMENT.html#part-1-application">Part 1 Application</a></td></tr>
<tr><td>2</td><td><a href="02_ADMINISTRATION.html">02 Administration</a></td><td>6</td><td><a href="02_ADMINISTRATION.html#part-1-roles">Part 1 Roles</a></td></tr>
<tr><td>3</td><td><a href="03_SERVICE_CATALOG.html">03 Service Catalog</a></td><td>5</td><td><a href="03_SERVICE_CATALOG.html#part-1-category">Part 1 Category</a></td></tr>
<tr><td>4</td><td><a href="06_NOTIFICATIONS_EVENTS_JOBS.html">06 Notifications</a></td><td>3</td><td><a href="06_NOTIFICATIONS_EVENTS_JOBS.html#part-1-events">Part 1 Events</a></td></tr>
<tr><td>5</td><td><a href="09_MODULES_AND_INTEGRATION.html">09 Modules</a></td><td>4</td><td><a href="09_MODULES_AND_INTEGRATION.html#part-1-menu">Part 1 Menu</a></td></tr>
<tr><td>6</td><td><a href="04_SERVICE_PORTAL.html">04 Portal</a></td><td>3</td><td><a href="04_SERVICE_PORTAL.html#part-1-widget-my-leaves">Part 1 Widget</a></td></tr>
<tr><td>7</td><td><a href="05_WORKSPACE_UIBUILDER.html">05 Workspace</a></td><td>4</td><td><a href="05_WORKSPACE_UIBUILDER.html#part-1-workspace">Part 1 Experience</a></td></tr>
<tr><td>8</td><td><a href="07_REPORTS_DASHBOARDS_PA.html">07 Reports</a></td><td>2</td><td><a href="07_REPORTS_DASHBOARDS_PA.html#part-1-report">Part 1 Report</a></td></tr>
<tr><td>9</td><td><a href="08_ATF_TESTING.html">08 ATF</a></td><td>4</td><td><a href="08_ATF_TESTING.html#part-1-suite">Part 1 Suite</a></td></tr>
<tr><td>10</td><td><a href="12_INTEGRATION_FULL_GUIDE.html">12 Integration</a></td><td>4</td><td><a href="12_INTEGRATION_FULL_GUIDE.html#part-1-integration-si">Part 1 SI</a></td></tr>
<tr><td>11</td><td><a href="10_IMPLEMENTATION_AND_CONFIG.html">10 Implementation</a></td><td>4</td><td><a href="10_IMPLEMENTATION_AND_CONFIG.html#part-1-seed-data">Part 1 Seed</a></td></tr>
<tr><td>12</td><td><a href="13_2HOUR_MASTER_SUMMARY.html">13 Summary</a></td><td>3</td><td><a href="13_2HOUR_MASTER_SUMMARY.html#part-1-quick-checklist">Part 1 Checklist</a></td></tr>
<tr><td>13</td><td><a href="11_SDK_CURSOR_CLAUDE.html">11 Practice</a></td><td>3</td><td><a href="11_SDK_CURSOR_CLAUDE.html#part-1-daily-workflow">Part 1 Workflow</a></td></tr>
<tr><td>14</td><td><a href="15_CLAUDE_CLI_CODE_SERVICENOW.html">15 Scripts</a></td><td>2</td><td><a href="15_CLAUDE_CLI_CODE_SERVICENOW.html#part-1-paste-studio">Part 1 Paste</a></td></tr>
<tr><td>15</td><td><a href="14_AI_SERVICENOW_AGENTS.html">14 AI</a> (optional)</td><td>—</td><td>After core E2E gate</td></tr>
</tbody></table>"""
    body = fix_links(intro_ok(
        "Ordered master path linking chapters 01–15. Each chapter is self-contained; this page is the index.",
        "15_CLAUDE_CLI_CODE_SERVICENOW.html", "15 Scripts",
    ) + """
<h2 id="how-objects-relate">Master path overview</h2>
<div class="ok">
<p>Complete walkthrough with every script embedded: <a href="STUDIO_CREATE_ALL_OBJECTS_01_16.html">Studio Create All Objects</a></p>
<p>Every form property + suggested values: <a href="PROFESSIONAL_HR_CREATE_PROPERTIES_AND_LINKS.html">Properties + Links</a></p>
</div>
<hr />
""" + RULE0 + """
<hr />
""" + part_header(1, "ordered-path", "Ordered Path Table (01→15)") + """
<h3>Purpose</h3>
<p>Recommended build order with Part anchors — follow sequentially on a fresh PDI.</p>
<h3>Verify checklist</h3>
""" + path_table + """
<hr />
""" + part_header(2, "master-links", "Master Links") + """
<h3>Purpose</h3>
<p>One-click entry points for the three master reference pages.</p>
<ul>
<li><a href="STUDIO_CREATE_ALL_OBJECTS_01_16.html">Studio Create All Objects 01–16</a> — every Part with Full script</li>
<li><a href="PROFESSIONAL_HR_CREATE_PROPERTIES_AND_LINKS.html">Professional Properties + Direct Links</a> — all 9 properties + URLs</li>
<li><a href="SCHEMA_AND_DATA.html">Schema and Data</a> — u_* columns and seed values</li>
<li><a href="scripts/index.html">Scripts portal</a> — mirror of src/ on disk</li>
<li><a href="index.html">Portal index</a> — all chapters 01–16</li>
</ul>
<h3>Verify checklist</h3>
<ul><li>All five links open from this page.</li></ul>
<hr />
""" + part_header(3, "e2e-gate", "E2E Gate") + """
<h3>Purpose</h3>
<p>Do not proceed to optional chapters (14 AI, advanced gaps) until this gate passes.</p>
<h3>Prerequisites</h3>
<ul><li>Ordered path rows 1–11 complete (through 10 Implementation seed + export).</li></ul>
<h3>Verify checklist</h3>
<div class="ok"><p>Run <a href="10_IMPLEMENTATION_AND_CONFIG.html#part-2-e2e-checklist">10 Part 2 E2E Checklist</a> — all items green.</p></div>
""" + fix_links(E2E_CHECKLIST) + """
<h3>Demo / test</h3>
<div class="demo-box"><p>employee1 submit → manager1 approve → balance + audit + notification → portal home → optional REST 201.</p></div>
<h2 id="master-verify">Master path verify checklist</h2>
<ol>
<li>Followed ordered path table through Implementation.</li>
<li>Master links bookmarked.</li>
<li>E2E gate passed.</li>
</ol>
""")
    return write_chapter(16, "16 — Studio From Scratch Master Path", hero, ql, body, 3)


if __name__ == "__main__":
    counts = {}
    builders = [
        build_ch03, build_ch04, build_ch05, build_ch06, build_ch07, build_ch08,
        build_ch09, build_ch10, build_ch11, build_ch12, build_ch13, build_ch14,
        build_ch15, build_ch16,
    ]
    for fn in builders:
        n = int(fn.__name__.replace("build_ch", ""))
        counts[n] = fn()
        print(f"{CHAPTER_FILES[n]} — {counts[n]} Parts")
