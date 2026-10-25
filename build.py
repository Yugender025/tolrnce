"""Build the TolRnce website: src/page.html -> docs/index.html (what GitHub Pages serves at tolrnce.com).

src/page.html is the page itself (styles, content and scripts). It is also what gets published as the
claude.ai preview, which adds its own document skeleton. This wraps it in a complete HTML document and adds
the head tags a real website needs: canonical address, favicon and the link preview for social media.

    python3 build.py
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://tolrnce.com/'
DESC = ('TolRnce is an AI design engineer for CAD. Describe a part, or drop in a drawing or a supplier’s STEP '
        'file, and get a parametric 3D model with its tolerances, drawing, cost and the steps to build it in your CAD program.')

src = open(os.path.join(HERE, 'src', 'page.html'), encoding='utf-8').read()
cut = src.index('<canvas')                      # everything before the first body element belongs in <head>
head, body = src[:cut].strip(), src[cut:].strip()
head = '\n'.join(l for l in head.split('\n') if not l.startswith('<meta name="description"'))
extra = f'''<meta name="description" content="{DESC}">
<link rel="canonical" href="{SITE}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#F8F9F8" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#14181B" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:site_name" content="TolRnce">
<meta property="og:url" content="{SITE}">
<meta property="og:title" content="TolRnce: the AI design engineer that works to tolerance">
<meta property="og:description" content="{DESC}">
<meta property="og:image" content="{SITE}og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="The TolRnce fit-cube logo and the line: The AI design engineer that works to tolerance.">
<meta name="twitter:card" content="summary_large_image">'''
doc = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
       '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
       'img{max-width:100%}[hidden]{display:none!important}</style>\n'
       + head + '\n' + extra + '\n</head>\n<body>\n' + body + '\n</body>\n</html>\n')
out = os.path.join(HERE, 'docs', 'index.html')
open(out, 'w', encoding='utf-8').write(doc)
print('wrote docs/index.html,', len(doc), 'bytes')
