#!/usr/bin/env python3
"""Export the authored SVG identity; requires Inkscape, Pillow and the Noto fonts."""
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET
from PIL import Image

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'assets'
SYMBOL = (ASSETS / 'brand-symbol.svg').read_text()
ART = SYMBOL[SYMBOL.index('<defs>'):SYMBOL.rindex('</svg>')]

def inkscape(source, *arguments):
    subprocess.run(['inkscape', str(source), *arguments], cwd=ROOT, check=True, capture_output=True)

for name, ink, muted in [('brand-lockup', '#172f46', '#62768a'), ('brand-lockup-inverse', '#ffffff', '#afc7da')]:
    plate = ''
    source = f'''<svg xmlns="http://www.w3.org/2000/svg" width="340" height="106" viewBox="0 0 340 106">
{plate}<g transform="translate(245 8) scale(.36)">{ART}</g>
<path d="M244 25v55" fill="none" stroke="{muted}" stroke-opacity=".25"/>
<text x="229" y="53" direction="rtl" text-anchor="start" font-family="Noto Kufi Arabic" font-size="32" font-weight="700" fill="{ink}">مبلط حمامات</text>
<text x="229" y="78" direction="rtl" text-anchor="start" font-family="Noto Sans Arabic" font-size="12" fill="{muted}">تبليط وترميم · الرياض</text>
</svg>'''
    path = ASSETS / (name + '-source.svg')
    path.write_text(source)
    inkscape(path, '--export-plain-svg', '--actions=select-all:all;object-to-path;export-filename:assets/' + name + '.svg;export-do')
    assert not ET.parse(ASSETS / (name + '.svg')).findall('.//{http://www.w3.org/2000/svg}text'), 'Wordmark must use outlined text.'

(ROOT / 'favicon.svg').write_text(SYMBOL)
inkscape(ASSETS / 'brand-symbol.svg', '--export-filename=assets/brand-emblem.png', '--export-width=512')
master = Image.open(ASSETS / 'brand-emblem.png').convert('RGBA')
master.resize((384, 384), Image.Resampling.LANCZOS).save(ASSETS / 'brand-emblem.webp', quality=95, method=6)
for size, filename in [(48, 'favicon.png'), (180, 'apple-touch-icon.png'), (192, 'icon-192.png'), (512, 'icon-512.png')]:
    image = Image.new('RGBA', (size, size), '#ffffff')
    image.alpha_composite(master.resize((size, size), Image.Resampling.LANCZOS))
    image.convert('RGB').save(ASSETS / filename, optimize=True)
(ASSETS / 'app-icon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512"><rect width="512" height="512" rx="64" fill="#fff"/><image href="brand-symbol.svg" width="512" height="512"/></svg>\n')

logo = ET.parse(ASSETS / 'brand-lockup-inverse.svg').getroot()
logo.attrib.update({'x': '570', 'y': '100', 'width': '565', 'height': '176'})
lockup = ET.tostring(logo, encoding='unicode')
cover = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
<defs><clipPath id="work-photo"><rect x="35" y="35" width="365" height="560" rx="24"/></clipPath></defs>
<rect width="1200" height="630" fill="#142a3e"/>
<rect x="15" y="15" width="1170" height="600" rx="30" fill="none" stroke="#87b1ce" stroke-opacity=".25"/>
<image href="photos/owner-06-social.jpg" x="35" y="35" width="365" height="560" preserveAspectRatio="xMidYMid slice" clip-path="url(#work-photo)"/>
{lockup}
<g direction="rtl" text-anchor="start">
<text x="1115" y="365" font-family="Noto Kufi Arabic" font-size="31" font-weight="700" fill="#b9d9ef">جمال المكان يبدأ من البلاط.</text>
<text x="1115" y="437" font-family="Noto Sans Arabic" font-size="26" fill="#c4d6e3">ترميم حمامات · سيراميك · بورسلان · رخام</text>
<text x="1115" y="545" font-family="Noto Sans Arabic" font-size="23" fill="#afc7da">الرياض · المصيف</text>
</g>
<path d="M450 488h675" stroke="#b8d6eb" stroke-opacity=".25"/>
<text x="460" y="545" font-family="sans-serif" font-size="26" fill="#ffffff">054 656 2621</text>
</svg>'''
(ASSETS / 'social-cover-identity.svg').write_text(cover)
inkscape(ASSETS / 'social-cover-identity.svg', '--export-filename=assets/social-cover-identity.png', '--export-width=1200', '--export-height=630')
temporary = ASSETS / 'social-cover-identity.png'
Image.open(temporary).convert('RGB').save(ASSETS / 'social-cover-identity.jpg', quality=92, optimize=True)
temporary.unlink()
print('Exported vector wordmarks, application icons and 1200 × 630 sharing artwork.')
