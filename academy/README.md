# Zero²Hero Academy

**Brand:** Zero²Hero Academy  
**Promise (AR):** تعلّم كل شيء في ServiceNow من الصفر إلى الاحتراف · الفصول 00→16 · كل الموديولات  
**Promise (EN):** Learn everything in ServiceNow from Zero to Hero · chapters 00→16 · all modules  

**Domain:** https://snzero2hero.com  
**Pages project:** `snzero2hero`  
**Live (Pages):** https://snzero2hero.pages.dev/academy/  
**Local:** open `index.html`

## Redeploy

```powershell
cd c:\SVCProject\HR_Leave_App
.\scripts\deploy-cloudflare-pages.ps1
```

Or:

```powershell
npx wrangler@4 pages deploy .\html --project-name=snzero2hero --commit-dirty=true
```
