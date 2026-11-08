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

### Material Studio visual refresh — November 8, 2026

The existing Vercel site and GitHub repository now use a coordinated forest, limestone and copper palette. The refresh includes an architectural hero, illustrated material links, service cards using the existing owner photographs, a craft feature, a staggered work gallery, styled FAQs, a darker contact form and a shared footer. Shared styles cover the homepage and all service, gallery and contact pages. No business details, ratings, guarantees or project statistics were added.

The work gallery includes accessible filter buttons for bathroom finishes, installation stages and outdoor details, with pressed states and announced result counts. All eight photographs remain available when JavaScript is disabled. Native image enlargement and contact links are retained. CSS and JavaScript URLs include a build-generated content hash so visitors receive the current release.

Checks for this refresh: regenerated all twelve HTML pages; `python3 validate.py`, `node --check assets/site.js` and `git diff --check` passed. Production Chromium review covered the homepage, bathroom service and contact page. Gallery filters returned 2, 4, 2 and 8 photographs respectively; the image modal opened and closed. No horizontal document overflow was observed at the available desktop viewport. Inputs and service selection were exercised without sending a message. The responsive CSS was reviewed, but visual verification of the new theme at mobile viewport sizes could not be completed in this session; earlier viewport checks above apply to the preceding design.

### Porcelain identity revision — November 8, 2026

The owner rejected the forest/copper palette and the previous four-tile logo. The replacement uses a white opening, cool porcelain surfaces, graphite typography and restrained mineral-blue accents. The mark is a new native SVG: a single rotated tile with a white water drop and two grout lines. The header wordmark is bolder. The revised identity is applied to the favicon, Apple/PWA icons, business logo metadata and a new sharing image. Vector originals are retained next to raster exports. Base styles, theme styles and logo URLs share a content-derived version so the previous cached colors and mark are replaced together.

### Architectural identity and opening — November 8, 2026

The current identity replaces the previous drop mark with an original generated architectural emblem: interlocking blue and graphite slabs with a curved negative space. `assets/brand-emblem.png` is the transparent raster master used for website delivery, and `assets/brand-emblem.webp` is its optimized display export. The app icons and favicon share this artwork; the emblem is raster artwork, not a vector logo. `assets/app-icon.svg` is a composition container. The superseded mark and sharing artwork have been removed.

Noto Kufi Arabic Bold provides the geometric Arabic wordmark and headings, with IBM Plex Sans Arabic retained for paragraphs and controls. The self-hosted font subset retains Arabic shaping features; its copyright and SIL OFL text are in `assets/fonts/Noto-Kufi-LICENSE.txt`.

The new opening uses two actual owner photographs, led by the tile and drain detail (owner-06), with owner-04 as a secondary finish image. No project photograph has been generated or retouched. Service icons now share a duotone line style, and cards, headings, inner pages and the footer follow the same visual system. The sharing composition source is `assets/social-cover-identity.svg`; the published JPEG is a 1200 × 630 export. `assets/photos/owner-06-social.jpg` is a resized export of the existing photograph for the SVG renderer.

Checks: `python3 build.py`, `python3 validate.py`, `node --check assets/site.js`, and `git diff --check`. Responsive styles cover narrow screens from 320 px, but a visual mobile-browser check remains outside the available desktop viewport in this session.

### Tile Studio refinement — November 8, 2026

The current revision uses a hand-authored SVG symbol and outlined Arabic wordmarks instead of the preceding raster emblem. The geometry retains the interlocking tile and meem-inspired negative space, with consistent stroke widths and clean edges at favicon size. The header, inverse footer lockup, favicon, PWA icons, business logo schema and sharing composition use the same source geometry. `python3 brand-assets.py` regenerates the wordmarks, raster exports and sharing card using Inkscape, Pillow and the installed Noto Kufi Arabic/Noto Sans Arabic fonts. The editable SVG wordmark sources are retained beside the outlined display assets.

The homepage now opens on a deep navy surface with pale blue accents. A manually controlled photograph feature switches among three actual owner photographs: finish details, installation and outdoor work. It updates the responsive image, caption, pressed button, announced status, image count and enlargement target together. There is no autoplay. A normal gallery link remains available without JavaScript. Service cards have two larger introductory entries and four compact entries on wide screens, with narrower-screen arrangements; the process section uses open numbered steps. Floating phone and WhatsApp circles include hover and keyboard-focus labels. Mobile form fields use 16 px text.

Preview QA used the supported managed preview. Temporary same-origin iframes displayed the homepage at nominal widths 320, 360, 390 and 768 px, and the bathroom service page at 360 px; Chromium's scrollbar reduces each content width by 15 px. No horizontal page overflow was observed. The 360 px mobile menu opened and closed, the photograph selector worked, and visual checks confirmed readable headings and unclipped branding. At the 1363 px desktop viewport, all three photograph choices updated their matching sources/captions/counts, enlargement opened the selected outdoor photograph, and the two-size service-card layout rendered correctly. These are embedded Chromium viewport checks, not physical-device Safari/Firefox tests. The responsive QA page is an untracked preview-only file inside ignored `dist/` and is excluded from deployment.

### Porcelain Atelier refinement — November 8, 2026

The hand-authored identity now uses four diagonally set ceramic tiles and contrasting grout in a navy tile-shaped frame. The same vector source regenerates the light and inverse wordmarks, browser and application icons, business logo, and sharing image. The refreshed opening uses a restrained navy-to-blue architectural grid, a clearer title hierarchy, a lighter treatment of the actual owner photograph, and refined photo selectors. Materials, services, inner-page details, the footer, and floating contact controls share the same palette and shape language. The original photographs and business information are preserved.

Verification covered `python3 build.py`, `python3 validate.py`, `node --check assets/site.js` and `git diff --check`. A managed Chromium preview displayed the home page at nominal iframe widths 320, 360 and 390 px and the bathroom service page at 360 px; each iframe's scrollbar reduces the content width by 15 px. No horizontal document overflow was found. The mobile menu, the opening photo selector, and image enlargement and close controls worked. This does not represent physical-device Safari or Firefox testing.
