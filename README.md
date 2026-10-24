# tolrnce.com

The TolRnce website. It's one page: a scroll-driven 3D story built with three.js. In order:
- the fit-cube logo pulls apart and closes to tolerance;
- a drawing extrudes into a solid, and its features light up;
- a shaft-and-bore fit you can try (ISO 286, ⌀20 H7);
- brackets bolt to a plate;
- tube routes across a panel;
- then the export files, test results and early access.

The studio itself (the CAD app) lives in [Yugender025/design-agent](https://github.com/Yugender025/design-agent).

## What's here

| Path | What it is |
|---|---|
| `src/page.html` | The page: styles, content and scripts. Edit this. |
| `build.py` | Builds `docs/index.html` from it, adding the head tags a website needs (canonical address, favicon, link preview). Run `python3 build.py` after every edit. |
| `docs/` | What GitHub Pages serves at tolrnce.com: `index.html`, `favicon.svg`, `og-image.png` (the picture shown when the link is shared), `CNAME` (the domain) and `.nojekyll` |

The page loads three.js 0.160.0 from jsDelivr and its fonts (Archivo, IBM Plex Sans and Mono) from Google Fonts. Nothing else is needed: no build tools, no server code.

## How it's hosted

GitHub Pages serves the `docs/` folder of the `main` branch, for free, with HTTPS. The domain tolrnce.com is registered at Squarespace and points to GitHub Pages through DNS records. Squarespace's own website builder isn't used.

### 1. Turn on GitHub Pages (once)

GitHub Pages works on a public repository on the free plan. A private repository needs GitHub Pro. The website's code is public anyway once it's live, so a public repository is the usual choice.

1. **Settings › General › Danger Zone › Change visibility › Public** (skip this if you have GitHub Pro).
2. **Settings › Pages**. Under **Build and deployment**, set **Source** to **Deploy from a branch**, then choose **Branch: main** and the **/docs** folder. Click **Save**.
3. On the same page, **Custom domain** should show `tolrnce.com` (read from `docs/CNAME`). If it's empty, type `tolrnce.com` and click **Save**.

### 2. Point tolrnce.com at GitHub Pages (Squarespace)

1. Open the [Squarespace domains dashboard](https://account.squarespace.com/domains), click **tolrnce.com**, then **DNS** (or **DNS Settings**).
2. Delete the existing records that point the domain at Squarespace: the **Squarespace Defaults** A records for `@` and the `www` CNAME. Leave anything for email alone.
3. Add these **custom records**:

| Type | Host | Data |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| AAAA | @ | 2606:50c0:8000::153 |
| AAAA | @ | 2606:50c0:8001::153 |
| AAAA | @ | 2606:50c0:8002::153 |
| AAAA | @ | 2606:50c0:8003::153 |
| CNAME | www | yugender025.github.io |

4. Wait. DNS changes take from a few minutes up to 24 to 48 hours. Then go back to **Settings › Pages** on GitHub. When the domain check passes, tick **Enforce HTTPS**. The tick box can take up to a day to become available.

### 3. Email: hello@tolrnce.com

The page asks visitors to write to hello@tolrnce.com. Squarespace includes free email forwarding with domains it sells. In the domains dashboard, open **tolrnce.com**, find **Email forwarding**, add `hello` and forward it to your own inbox. Turning it on adds the email (MX) records it needs; don't delete those when you change the website records.

## Editing

1. Edit `src/page.html`.
2. Run `python3 build.py`.
3. Commit and push. GitHub Pages updates the live site within a minute or two.

Keep the NIST acknowledgement and the trademark note in the footer. The numbers in "Checked against public test data" come from the studio's benchmarks (`datasets/README.md` and `ml/README.md` in design-agent); update them when those change.
