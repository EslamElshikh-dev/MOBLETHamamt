# Website design and development

This website was designed, programmed and developed by **Eng. Eslam Elshikh (المهندس إسلام الشيخ)**.

- Official profile: https://www.eslam-elshikh.com/
- Developer profile: https://github.com/EslamElshikh-dev
- Website: https://eslamelshikh-dev.github.io/
- Credit reviewed: 2026-11-03

The footer uses the approved ES signature with this website’s own colors. Website creator metadata describes the design and software implementation. Editorial authorship, business publishing identity, original contributor acknowledgements, and client copyright are retained. This credit does not relicense the repository or transfer the client’s rights.

Git history records the exact files and implementation revisions. Structured data describes the visible credit; it does not guarantee a Google rich result or constitute legal registration of authorship.

## November 8, 2026 redesign

- Canonical production origin: `https://moblet-hamamat.vercel.app`.
- Business identity verified from the user-supplied Maps listing: https://maps.app.goo.gl/ACpRdXij8ujAnbGP6?g_st=ac . Exact name: `مبلط حمامات`; telephone: `+966546562621`; address: طريق ابي بكر الصديق، المصيف، الرياض 12466; coordinates: 24.7644144, 46.6927084.
- Observed hours: Sunday 09:00–20:00, Monday through Saturday 05:30–22:00. The website mirrors those observations; it does not change the Business Profile.
- The Business Profile still links to `moblet-hamamat.com`. Ownership and DNS were not changed. This domain returned HTTP 503 during this review. The earlier GitHub Pages origin redirects visitors to the new canonical origin in the client, with canonical markup as the non-JavaScript fallback.
- Eight photographs came from the listing's **من المالك** gallery, with exact asset URLs recorded in `assets/photo-sources.json`. Original JPEG downloads are local working files, excluded from Git; responsive WebP files are deployed. Photographs were resized and compressed without generative edits.
- Six distinct service pages cover bathroom renovation, ceramic, porcelain, marble, villa interiors and exterior tiling. Content explains decisions, scope and preparation; prices, guarantees, completion times and project measurements are not invented.
- Schema uses a shared business ID, `WebSite`, `WebPage`/`CollectionPage`, `Service`, `BreadcrumbList` and image lists. No self-serving rating markup or unsupported FAQ rich-result claims are included. Official references: https://developers.google.com/search/docs/appearance/structured-data/local-business and https://developers.google.com/search/docs/appearance/structured-data/review-snippet .
- Self-hosted IBM Plex Sans Arabic is licensed under `assets/fonts/OFL.txt`.

### Build and checks

The deployed files are plain HTML, CSS and JavaScript. No application runtime, secrets or package installation is required. `site-data.json` is the editorial source; run `python3 build.py` to regenerate all HTML, sitemap, robots and the manifest, then `python3 validate.py` and `node --check assets/site.js`.

Browser QA used Chromium with embedded viewport widths of 320, 360, 390, 680, 768, 1024 and 1440 px. No horizontal document overflow was observed on the homepage or the bathroom service page at 360 px. The mobile menu, photo modal and FAQ disclosures were exercised. These checks do not substitute for physical-device Safari or Firefox testing. Reduced motion, safe-area insets, native forms and semantic elements are supported.

The contact form prepares a WhatsApp URL locally and does not submit data to a website backend. Browser testing reached WhatsApp's external application navigation, which the cloud browser blocked at the protocol boundary; no message was sent.
