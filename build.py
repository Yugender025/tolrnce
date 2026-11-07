"""Build the TolRnce website: src/page.html -> docs/ (what GitHub Pages serves at tolrnce.com).

src/page.html is the page itself (styles, content and scripts). It is also what gets published as the
claude.ai preview, which adds its own document skeleton. This wraps it in a complete HTML document and adds
what a real website needs:

  - the search result: title, description, canonical address and robots rules
  - structured data (JSON-LD) that tells search engines TolRnce is a company and a CAD application
  - favicon, home-screen icon and the link preview for social media
  - docs/robots.txt and docs/sitemap.xml

    python3 build.py

To prove to Google Search Console or Bing Webmaster Tools that you own the site with the "HTML tag" method,
put the code they give you in GOOGLE_VERIFY or BING_VERIFY and rebuild. (The DNS method needs no change here.)
"""
import datetime
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://tolrnce.com/'

# What shows in search results. Keep the title under about 60 characters and the description under about
# 160: search engines cut anything longer. Lead with the words people type: 2D drawing, 3D CAD, tolerances.
TITLE = 'TolRnce: AI for 2D drawing to 3D CAD, with tolerances'
DESC = ('Turn a 2D drawing, a STEP file or a few sentences into an editable 3D CAD model with ISO fits and '
        'tolerances. Rebuilds it in SOLIDWORKS, Fusion and FreeCAD.')

# Link previews on LinkedIn, X, Slack and the like keep the brand line.
SOCIAL_TITLE = 'TolRnce: the AI design engineer that works to tolerance'
SOCIAL_DESC = ('Give TolRnce a 2D drawing, a supplier’s STEP file or a few sentences. It builds the parametric '
               '3D model with its fits and tolerances, the manufacturing drawing and a cost estimate, ready to '
               'edit in your CAD program.')

GOOGLE_VERIFY = ''   # content="..." from Google Search Console, HTML tag method
BING_VERIFY = ''     # content="..." from Bing Webmaster Tools, HTML meta tag method

FEATURES = [
    '2D drawing to parametric 3D CAD model (DWG, DXF, photos of drawings, or a description in words)',
    'STEP AP203, AP214 and AP242 import with automatic feature recognition',
    'ISO 286 hole and shaft fits and ISO 2768 general tolerances',
    'Tolerance stack-up calculator',
    'Assemblies with mates, bolted joints, clash checks and a bill of materials',
    'Tube routing for panels and skids, with cut lists',
    'Manufacturing drawing with dimensions, hole table and general tolerances',
    'Cost estimate with design-for-manufacturing checks',
    'Exports STEP and STL, and rebuilds the feature tree in SOLIDWORKS, Fusion and FreeCAD',
]
STRUCTURED = {
    '@context': 'https://schema.org',
    '@graph': [
        {
            '@type': 'Organization',
            '@id': SITE + '#organization',
            'name': 'TolRnce',
            'url': SITE,
            'logo': SITE + 'logo-512.png',
            'email': 'hello@tolrnce.com',
        },
        {
            '@type': 'WebSite',
            '@id': SITE + '#website',
            'name': 'TolRnce',
            'url': SITE,
            'publisher': {'@id': SITE + '#organization'},
        },
        {
            '@type': 'SoftwareApplication',
            '@id': SITE + '#app',
            'name': 'TolRnce',
            'alternateName': 'TolRnce AI design engineer',
            'url': SITE,
            'description': SOCIAL_DESC,
            'applicationCategory': 'DesignApplication',
            'applicationSubCategory': 'CAD',
            'operatingSystem': 'Web browser, Windows, macOS',
            'image': SITE + 'og-image.png',
            'featureList': FEATURES,
            'publisher': {'@id': SITE + '#organization'},
        },
    ],
}


def attr(s):
    return html.escape(s, quote=True)


src = open(os.path.join(HERE, 'src', 'page.html'), encoding='utf-8').read()
cut = src.index('<canvas')                      # everything before the first body element belongs in <head>
head, body = src[:cut].strip(), src[cut:].strip()
head = '\n'.join(l for l in head.split('\n')
                 if not l.startswith('<meta name="description"') and not l.startswith('<title>'))
verify = ''.join(f'\n<meta name="{n}" content="{attr(v)}">'
                 for n, v in (('google-site-verification', GOOGLE_VERIFY), ('msvalidate.01', BING_VERIFY)) if v)
ld = json.dumps(STRUCTURED, ensure_ascii=False, indent=1).replace('</', '<\\/')
extra = f'''<meta name="description" content="{attr(DESC)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{SITE}">{verify}
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="theme-color" content="#F8F9F8" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#14181B" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:site_name" content="TolRnce">
<meta property="og:locale" content="en_US">
<meta property="og:url" content="{SITE}">
<meta property="og:title" content="{attr(SOCIAL_TITLE)}">
<meta property="og:description" content="{attr(SOCIAL_DESC)}">
<meta property="og:image" content="{SITE}og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="The TolRnce fit-cube logo and the line: The AI design engineer that works to tolerance.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{attr(SOCIAL_TITLE)}">
<meta name="twitter:description" content="{attr(SOCIAL_DESC)}">
<meta name="twitter:image" content="{SITE}og-image.png">
<script type="application/ld+json">
{ld}
</script>'''
doc = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
       f'<title>{html.escape(TITLE)}</title>\n'
       '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
       'img{max-width:100%}[hidden]{display:none!important}</style>\n'
       + head + '\n' + extra + '\n</head>\n<body>\n' + body + '\n</body>\n</html>\n')

docs = os.path.join(HERE, 'docs')
open(os.path.join(docs, 'index.html'), 'w', encoding='utf-8').write(doc)

# Every page that should be found goes in PAGES (path from the site root). One page for now.
PAGES = ['']
today = datetime.date.today().isoformat()
sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + ''.join(f'  <url><loc>{SITE}{p}</loc><lastmod>{today}</lastmod></url>\n' for p in PAGES)
           + '</urlset>\n')
open(os.path.join(docs, 'sitemap.xml'), 'w', encoding='utf-8').write(sitemap)
open(os.path.join(docs, 'robots.txt'), 'w', encoding='utf-8').write(
    f'User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n')

print('wrote docs/index.html,', len(doc), 'bytes; docs/sitemap.xml; docs/robots.txt')
