#!/usr/bin/env python3
"""Check deployable HTML, local resources, metadata and the verified business entity."""
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parent
BASE='https://moblet-hamamat.vercel.app'

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.h1=0; self.ids=[]; self.resources=[]; self.links=[]; self.meta={}; self.canonical=[]; self.data=[]; self.in_data=False; self.buf=''
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='h1': self.h1+=1
        if 'id' in a: self.ids.append(a['id'])
        if tag=='meta': self.meta[a.get('name') or a.get('property')]=a.get('content')
        if tag=='a' and 'href' in a: self.links.append(a['href'])
        if tag=='link':
            if a.get('rel')=='canonical': self.canonical.append(a['href'])
            elif a.get('rel') in ['stylesheet','icon','apple-touch-icon','manifest','preload']: self.resources.append(a['href'])
        if tag=='img':
            assert 'alt' in a, 'Image has no alt'
            assert 'width' in a and 'height' in a, 'Image has no dimensions'
            if a.get('src'): self.resources.append(a['src'])
            for entry in a.get('srcset','').split(','):
                if entry.strip(): self.resources.append(entry.strip().split()[0])
        if tag=='script' and a.get('src'): self.resources.append(a['src'])
        if tag=='script' and a.get('type')=='application/ld+json': self.in_data=True; self.buf=''
    def handle_data(self,data):
        if self.in_data: self.buf+=data
    def handle_endtag(self,tag):
        if tag=='script' and self.in_data:
            self.data.append(json.loads(self.buf));self.in_data=False

def resolve(file,url):
    p=unquote(urlsplit(url).path)
    return ROOT/p.lstrip('/') if p.startswith('/') else (file.parent/p).resolve()

files=[ROOT/'index.html',ROOT/'404.html']+sorted(ROOT.glob('services/**/index.html'))+[ROOT/p/'index.html' for p in ['projects','contact','privacy']]
for f in files:
    p=Page();p.feed(f.read_text())
    assert p.h1==1,(f,'H1 count',p.h1)
    assert len(set(p.ids))==len(p.ids),(f,'Duplicate ids')
    assert len(p.canonical)==1 and p.canonical[0].startswith(BASE+'/'),(f,'Canonical')
    assert p.meta.get('description') and p.meta.get('og:image'),(f,'Metadata')
    for u in p.links+p.resources:
        if u.startswith(('#','http:','https:','tel:','mailto:')): continue
        assert resolve(f,u).exists(),(f,'Missing resource',u)
    assert len(p.data)==1,(f,'Schema graph')
    nodes=p.data[0]['@graph'];b=next(n for n in nodes if n['@type']=='HomeAndConstructionBusiness')
    assert b['name']=='مبلط حمامات' and b['telephone']=='+966546562621'
    assert b['address']['postalCode']=='12466' and b['geo']=={'@type':'GeoCoordinates','latitude':24.7644144,'longitude':46.6927084}
    assert b['openingHoursSpecification'][1]['dayOfWeek']=='Sunday'
    assert b['openingHoursSpecification'][1]['opens']=='09:00'
    assert 'aggregateRating' not in b and 'review' not in b
    if f.parent.parent.name=='services': assert any(n['@type']=='Service' for n in nodes),(f,'Service schema')
    if f.parent.name=='privacy': assert p.meta['robots']=='noindex,follow'

urls=[n.find('{*}loc').text for n in ET.parse(ROOT/'sitemap.xml').getroot()]
assert len(urls)==10 and len(set(urls))==10
for u in urls:
    assert u.startswith(BASE+'/')
    assert (ROOT/u.removeprefix(BASE).strip('/')/'index.html').exists(),u
assert BASE+'/sitemap.xml' in (ROOT/'robots.txt').read_text()
print(f'PASS: {len(files)} HTML pages; 10 indexable URLs; internal links, responsive assets, metadata, and business/service schema.')
