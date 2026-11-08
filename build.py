#!/usr/bin/env python3
"""Build the dependency-free Arabic website. Run: python3 build.py."""
import html
import hashlib
import json
import pathlib
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).parent
D = json.loads((ROOT / 'site-data.json').read_text())
BASE = D['url'].rstrip('/')
ASSET_VERSION = hashlib.sha256(b''.join((ROOT/name).read_bytes() for name in ['assets/site.css','assets/studio.css','assets/site.js','assets/brand-mark.svg'])).hexdigest()[:10]
SERVICES = D['services']
PHOTOS = {p['id']: p for p in D['photos']}
SIZES = {'01': (1600,2688), '03': (1600,2842), '04': (1600,2133), '05': (1600,2133), '06': (1080,1350), '07': (900,1600), '09': (1600,2133), '10': (1600,2133)}
MAPS = D['maps']
WA = 'https://wa.me/966546562621'
e = lambda v: html.escape(str(v), quote=True)

ICONS = {
 'arrow': '<path d="M19 12H5m0 0 6-6m-6 6 6 6"/>',
 'external': '<path d="M14 4h6v6m0-6L10 14M9 4H5a1 1 0 0 0-1 1v14a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-4"/>',
 'phone': '<path d="M20.5 16.5v2.7a1.5 1.5 0 0 1-1.7 1.5A18.4 18.4 0 0 1 3.3 5.2 1.5 1.5 0 0 1 4.8 3.5h2.7l1.4 5-2 1.8a15 15 0 0 0 6.8 6.8l1.8-2 5 1.4Z"/>',
 'whatsapp': '<path d="M20.5 11.6a8.6 8.6 0 0 1-12.7 7.5L3 20.5l1.4-4.7a8.6 8.6 0 1 1 16.1-4.2Z"/><path d="M8 7.5c-.9.4-.6 2.4.7 4.3 1.2 1.8 3.2 3.3 5.2 3.8 1.5.4 2.6-.5 2.6-1.4l-2.8-1.4-1.1 1c-1.8-.7-3.1-2-3.8-3.5l.9-1.1-1.2-2.3-.5.6Z"/>',
 'grid': '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
 'bath': '<path d="M3 11h18v3a6 6 0 0 1-6 6H9a6 6 0 0 1-6-6v-3Zm2 0V5a2 2 0 0 1 4 0M7 20v1m10-1v1"/>',
 'layers': '<path d="m12 3 10 5-10 5L2 8l10-5ZM2 12l10 5 10-5M2 16l10 5 10-5"/>',
 'stone': '<path d="m5 3 14 0 3 18H2L5 3Zm1 6 5 2 3-5m-3 5-2 7m2-7 7 5"/>',
 'home': '<path d="m2 11 10-8 10 8M5 9v12h14V9m-10 12v-8h6v8"/>',
 'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5"/>',
 'pin': '<path d="M20 10c0 5-8 12-8 12S4 15 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/>',
 'check': '<path d="m5 12 4 4L19 6"/>',
 'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 'zoom': '<circle cx="10" cy="10" r="6"/><path d="m15 15 6 6M10 7v6m-3-3h6"/>',
 'close': '<path d="m6 6 12 12M6 18 18 6"/>',
 'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>',
 'spark': '<path d="m12 2 2.7 7.3L22 12l-7.3 2.7L12 22l-2.7-7.3L2 12l7.3-2.7L12 2Z"/>'
}

def icon(name):
    return f'<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-{name}"/></svg>'

def sprite():
    return '<svg class="sprite" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">' + ''.join(f'<symbol id="i-{k}" viewBox="0 0 24 24">{v}</symbol>' for k,v in ICONS.items()) + '</svg>'

def prefix(path):
    return '../' * len([v for v in path.strip('/').split('/') if v])

def img(n, pre='', cls='', eager=False, sizes='(max-width: 680px) 100vw, 50vw'):
    w,h = SIZES[n]
    # Do not repeat width descriptors for photographs smaller than an output size.
    variants = {min(s,w): s for s in [480,960,1440]}
    ss = ', '.join(f'{pre}assets/photos/owner-{n}-{s}.webp {width}w' for width,s in variants.items())
    attrs = 'fetchpriority="high" loading="eager"' if eager else 'loading="lazy"'
    return f'<img class="{cls}" src="{pre}assets/photos/owner-{n}-960.webp" srcset="{ss}" sizes="{sizes}" width="{w}" height="{h}" alt="{e(PHOTOS[n]["alt"])}" {attrs} decoding="async">'

def button(text, url=WA, style='primary', which='arrow', external=False):
    return f'<a class="btn btn-{style}" href="{e(url)}"'+ (' target="_blank" rel="noopener noreferrer"' if external else '') + f'>{e(text)}{icon(which)}</a>'

def header(pre, section):
    section = 'services' if section == 'service' else section
    links = [('الرئيسية', pre or './', 'home'), ('خدماتنا', pre+'services/', 'services'), ('من أعمالنا', pre+'projects/', 'projects'), ('تواصل معنا', pre+'contact/', 'contact')]
    nav=''.join(f'<a href="{url}"'+(' aria-current="page"' if section==key else '')+f'>{title}</a>' for title,url,key in links)
    return f'''<a class="skip" href="#main">انتقل إلى المحتوى</a>
    <div class="topbar"><div class="container topbar-inner"><span>من تفاصيل البلاط… إلى جمال المكان</span><a href="{e(MAPS)}" target="_blank" rel="noopener noreferrer">{icon('pin')}الرياض · حي المصيف</a></div></div>
    <header class="header"><div class="container header-inner"><a href="{pre or './'}" class="brand" aria-label="مبلط حمامات، الرئيسية"><img src="{pre}assets/brand-mark.svg?v={ASSET_VERSION}" alt="" width="54" height="54"><span>مبلط حمامات<small>تبليط وترميم في الرياض</small></span></a><nav class="desktop-nav" aria-label="التنقل الرئيسي">{nav}</nav><a class="header-phone" href="tel:{D['phone']}">{icon('phone')}<bdi>{D['phoneDisplay']}</bdi></a><details class="mobile-nav"><summary aria-label="فتح قائمة التنقل">{icon('menu')}</summary><nav aria-label="تنقل الجوال">{nav}<a href="tel:{D['phone']}">اتصل بنا <bdi>{D['phoneDisplay']}</bdi></a></nav></details></div></header>'''

def footer(pre):
    service_links=''.join(f'<a href="{pre}services/{s["slug"]}/">{s["name"]}</a>' for s in SERVICES)
    return f'''<footer class="footer"><div class="container"><div class="footer-slogan"><span>مبلط حمامات · الرياض</span><p>تفاصيل <em>تَفرق.</em></p><a href="{pre}contact/" class="footer-start" aria-label="ابدأ مشروعك، تواصل معنا">{icon('arrow')}</a></div><div class="footer-grid"><div class="footer-about"><a class="brand" href="{pre or './'}"><img src="{pre}assets/brand-mark.svg?v={ASSET_VERSION}" alt="" width="54" height="54"><span>مبلط حمامات<small>سيراميك · بورسلان · رخام</small></span></a><p>ترميم حمامات وأعمال تبليط للمساحات الداخلية والخارجية في الرياض. تفاصيل مرتبة، من بداية الفكرة إلى تنسيق التنفيذ.</p><a class="footer-map" href="{e(MAPS)}" target="_blank" rel="noopener noreferrer">{icon('pin')}{D['address']}</a></div><div><h2>الخدمات</h2><div class="footer-links">{service_links}</div></div><div><h2>خلّنا نناقش مشروعك</h2><a class="footer-number" href="tel:{D['phone']}"><bdi>{D['phoneDisplay']}</bdi></a><a class="footer-wa" href="{WA}" target="_blank" rel="noopener noreferrer">{icon('whatsapp')}التواصل على واتساب</a><p class="footer-hours">الأحد: ٩ ص – ٨ م<br>الاثنين إلى السبت: ٥:٣٠ ص – ١٠ م</p></div></div><div class="footer-bottom"><p>© 2026 مبلط حمامات. جميع الحقوق محفوظة. <a href="{pre}privacy/">الخصوصية</a></p><a class="developer" data-eslam-signature="v1" href="https://www.eslam-elshikh.com/" target="_blank" rel="noopener noreferrer" aria-label="تصميم وتطوير المهندس إسلام الشيخ، يفتح في تبويب جديد"><img src="{pre}assets/developer.webp" width="32" height="32" alt="" loading="lazy"><span><small>تصميم وتطوير</small><strong>المهندس إسلام الشيخ</strong></span>{icon('external')}</a></div></div></footer><div class="floating-contact" role="group" aria-label="التواصل السريع"><a class="float-wa" href="{WA}" target="_blank" rel="noopener noreferrer" aria-label="تواصل عبر واتساب">{icon('whatsapp')}</a><a class="float-phone" href="tel:{D['phone']}" aria-label="اتصل على 0546562621">{icon('phone')}</a></div><dialog class="lightbox" aria-label="عرض صورة من أعمال النشاط"><button class="lightbox-close" type="button" aria-label="إغلاق الصورة">{icon('close')}</button><figure><img width="960" height="1280" alt=""><figcaption></figcaption></figure></dialog>'''

def business():
    return {'@type':'HomeAndConstructionBusiness','@id':BASE+'/#business','name':D['name'],'url':BASE+'/','telephone':D['phone'],'description':'ترميم حمامات وتركيب سيراميك وبورسلان ورخام وتبليط مساحات داخلية وخارجية في الرياض.','image':[BASE+'/assets/photos/owner-04.webp',BASE+'/assets/photos/owner-06.webp',BASE+'/assets/photos/owner-07.webp'],'logo':BASE+'/assets/brand-mark.svg?v='+ASSET_VERSION,'address':{'@type':'PostalAddress','streetAddress':'طريق ابي بكر الصديق، المصيف','addressLocality':'الرياض','addressRegion':'منطقة الرياض','postalCode':'12466','addressCountry':'SA'},'geo':{'@type':'GeoCoordinates','latitude':D['latitude'],'longitude':D['longitude']},'hasMap':MAPS,'sameAs':[MAPS],'areaServed':{'@type':'City','name':'الرياض'},'openingHoursSpecification':[{'@type':'OpeningHoursSpecification','dayOfWeek':['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'],'opens':'05:30','closes':'22:00'},{'@type':'OpeningHoursSpecification','dayOfWeek':'Sunday','opens':'09:00','closes':'20:00'}],'hasOfferCatalog':{'@type':'OfferCatalog','name':'خدمات مبلط حمامات في الرياض','itemListElement':[{'@type':'Offer','itemOffered':{'@type':'Service','@id':BASE+'/services/'+s['slug']+'/#service','name':s['title'],'url':BASE+'/services/'+s['slug']+'/'}} for s in SERVICES]}}

def schema(path,title,description,crumbs=None,service=None):
    url=BASE+path
    nodes=[business(),{'@type':'WebSite','@id':BASE+'/#website','url':BASE+'/','name':D['name'],'inLanguage':'ar-SA','publisher':{'@id':BASE+'/#business'},'creator':{'@id':'https://www.eslam-elshikh.com/#person'}},{'@type':'Person','@id':'https://www.eslam-elshikh.com/#person','name':'إسلام الشيخ','url':'https://www.eslam-elshikh.com/'},{'@type':'WebPage','@id':url+'#webpage','url':url,'name':title,'description':description,'inLanguage':'ar-SA','isPartOf':{'@id':BASE+'/#website'},'about':{'@id':BASE+'/#business'},'primaryImageOfPage':{'@type':'ImageObject','url':BASE+'/assets/photos/owner-'+(service['image'] if service else '04')+'.webp'}}]
    if crumbs:
        nodes.append({'@type':'BreadcrumbList','@id':url+'#breadcrumbs','itemListElement':[{'@type':'ListItem','position':i+1,'name':name,'item':BASE+p} for i,(name,p) in enumerate(crumbs)]})
        nodes[3]['breadcrumb']={'@id':url+'#breadcrumbs'}
    if service:
        nodes.append({'@type':'Service','@id':url+'#service','name':service['title'],'serviceType':service['name'],'description':service['intro'],'url':url,'image':BASE+'/assets/photos/owner-'+service['image']+'.webp','provider':{'@id':BASE+'/#business'},'areaServed':{'@type':'City','name':'الرياض'},'mainEntityOfPage':{'@id':url+'#webpage'}})
        nodes[3]['mainEntity']={'@id':url+'#service'}
    if path == '/projects/':
        nodes[3]['@type'] = 'CollectionPage'
        nodes[3]['mainEntity'] = {'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'item':{'@type':'ImageObject','contentUrl':BASE+'/assets/photos/owner-'+p['id']+'.webp','name':p['title'],'description':p['alt']}} for i,p in enumerate(D['photos'])]}
    if path == '/services/':
        nodes[3]['@type'] = 'CollectionPage'
        nodes[3]['mainEntity'] = {'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'item':{'@type':'Service','@id':BASE+'/services/'+s['slug']+'/#service','name':s['title'],'url':BASE+'/services/'+s['slug']+'/'}} for i,s in enumerate(SERVICES)]}
    return json.dumps({'@context':'https://schema.org','@graph':nodes},ensure_ascii=False,separators=(',',':')).replace('</','<\\/')

def layout(path,title,description,body,section='home',crumbs=None,service=None,noindex=False):
    pre=prefix(path)
    current_img=service['image'] if service else '04'
    preload=f'<link rel="preload" as="image" href="{pre}assets/photos/owner-{current_img}-960.webp" imagesrcset="'+', '.join(f'{pre}assets/photos/owner-{current_img}-{s}.webp {width}w' for width,s in {min(s,SIZES[current_img][0]): s for s in [480,960,1440]}.items())+'" imagesizes="(max-width: 680px) 100vw, 50vw">' if section in ['home','service'] else ''
    return f'''<!doctype html>
<html lang="ar-SA" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#f7f9fb"><title>{e(title)}</title><meta name="description" content="{e(description)}"><meta name="robots" content="{'noindex,follow' if noindex else 'index,follow,max-image-preview:large'}"><link rel="canonical" href="{BASE+path}"><link rel="icon" href="{pre}favicon.svg?v={ASSET_VERSION}" type="image/svg+xml"><link rel="apple-touch-icon" href="{pre}assets/apple-touch-icon.png?v={ASSET_VERSION}"><link rel="manifest" href="{pre}site.webmanifest?v={ASSET_VERSION}"><link rel="preload" href="{pre}assets/fonts/plex-arabic-400.woff2" as="font" type="font/woff2" crossorigin>{preload}<link rel="stylesheet" href="{pre}assets/site.css?v={ASSET_VERSION}"><link rel="stylesheet" href="{pre}assets/studio.css?v={ASSET_VERSION}"><script src="{pre}assets/site.js?v={ASSET_VERSION}" defer></script><meta name="creator" content="المهندس إسلام الشيخ"><meta property="og:type" content="website"><meta property="og:locale" content="ar_SA"><meta property="og:site_name" content="{D['name']}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}"><meta property="og:url" content="{BASE+path}"><meta property="og:image" content="{BASE}/assets/social-cover-slate.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="هوية مبلط حمامات بالرياض: بلاطة زرقاء وقطرة ماء باللون الأبيض"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(description)}"><meta name="twitter:image" content="{BASE}/assets/social-cover-slate.png"><script type="application/ld+json">{schema(path,title,description,crumbs,service)}</script></head><body data-page="{section}">{sprite()}{header(pre,section)}<main id="main">{body}</main>{footer(pre)}</body></html>'''

def breadcrumbs(items,pre):
    return '<nav class="breadcrumbs" aria-label="مسار التنقل">'+'<span aria-hidden="true">/</span>'.join(f'<a href="{pre+p.lstrip("/")}">{n}</a>' if i<len(items)-1 else f'<span aria-current="page">{n}</span>' for i,(n,p) in enumerate(items))+'</nav>'

def service_cards(pre):
    return '<div class="service-grid">'+''.join(f'''<a class="service-card" href="{pre}services/{s['slug']}/"><div class="service-cover">{img(s['image'],pre,sizes='(max-width: 680px) 90vw, (max-width: 1000px) 45vw, 30vw')}<span class="service-photo-tag">من صور النشاط</span></div><div class="service-content"><div class="service-top">{icon(s['icon'])}<span>0{i+1}</span></div><h3>{s['name']}</h3><p>{s['short']}</p><span class="card-link">تفاصيل الخدمة <span class="card-arrow">{icon('arrow')}</span></span></div></a>''' for i,s in enumerate(SERVICES))+'</div>'

def gallery(pre,count=8):
    groups={'04':'bathrooms','06':'bathrooms','03':'installation','10':'installation','07':'outdoor','01':'outdoor','05':'installation','09':'installation'}
    return '<div class="photo-grid">'+''.join(f'''<a class="photo-card photo-{i}" href="{pre}assets/photos/owner-{p['id']}.webp" data-group="{groups[p['id']]}" data-lightbox data-caption="{e(p['title'])}">{img(p['id'],pre,sizes='(max-width: 680px) 90vw, (max-width: 1000px) 50vw, 33vw')}<span class="photo-caption"><span><small>تفاصيل من العمل</small>{p['title']}</span><span class="photo-zoom">{icon('zoom')}</span></span></a>''' for i,p in enumerate(D['photos'][:count]))+'</div>'

def faq(rows):
    return '<div class="faq-list">'+''.join(f'<details><summary>{e(q)}<span aria-hidden="true">+</span></summary><p>{e(a)}</p></details>' for q,a in rows)+'</div>'

def request_form():
    options=''.join(f'<option>{s["name"]}</option>' for s in SERVICES)
    return f'''<form id="request-form" class="request-form"><span class="form-kicker">نبدأ برسالة.</span><h2>وش تحتاج لمساحتك؟</h2><p>حدد الخدمة والحي وأهم التفاصيل، وجهّز رسالتك على واتساب.</p><div class="form-grid"><div class="field"><label for="service">الخدمة المطلوبة</label><select id="service" name="service" required><option value="">اختر الخدمة</option>{options}<option>خدمة أخرى</option></select></div><div class="field"><label for="district">الحي في الرياض</label><input id="district" name="district" maxlength="80" autocomplete="address-level3" placeholder="مثل: المصيف"></div><div class="field field-wide"><label for="project-details">تفاصيل العمل</label><textarea id="project-details" name="details" maxlength="1200" rows="4" placeholder="مساحة تقريبية، نوع البلاط، أو وصف ما يحتاج تغييرًا"></textarea></div></div><button class="btn btn-primary" type="submit">جهّز رسالتك على واتساب {icon('whatsapp')}</button><p class="form-hint">يفتح واتساب لمراجعة التفاصيل وإرسالها.</p><p class="form-status" role="status" aria-live="polite"></p></form>'''

def contact_strip(pre):
    return f'''<section class="cta-section"><div class="container cta-inner"><div><span class="eyebrow">الخطوة الجاية بسيطة</span><h2>فكرتك واضحة؟<br>خلّنا نرتّب تفاصيلها.</h2><p>صورة للمكان، مقاس تقريبي، ووصف لما تحتاجه. نبدأ من هنا.</p></div><div class="cta-actions">{button('ناقش مشروعك على واتساب',WA,'cream','whatsapp',True)}{button('تواصل معنا',pre+'contact/','outline-light')}</div></div></section>'''

def write(path,content):
    file=ROOT/('index.html' if path=='/' else path.strip('/')+'/index.html')
    file.parent.mkdir(parents=True,exist_ok=True)
    file.write_text(content)

home=f'''<section class="hero studio-hero"><div class="container hero-grid"><div class="hero-copy"><span class="eyebrow">مبلط حمامات · الرياض</span><div class="hero-kicker">مساحة جديدة. إحساس مختلف.</div><h1>مبلط حمامات<br><span class="hero-title-soft">حكاية خامة.</span><em>وجمال تفاصيل.</em></h1><p class="hero-lead">من حمامك إلى أرضيات بيتك؛ سيراميك، بورسلان ورخام. نرتّب معك الخامة والتوزيع والتشطيب، لتجتمع التفاصيل في مساحة تحبها.</p><div class="hero-actions">{button('خلّنا نرتّب فكرتك',WA,'primary','whatsapp',True)}{button('استكشف الأعمال','projects/','text')}</div><div class="hero-notes"><span>{icon('pin')}داخل مدينة الرياض</span><span>{icon('grid')}حمامات · أرضيات · مساحات خارجية</span></div></div><div class="hero-visual"><div class="image-index" aria-hidden="true"><span>تفاصيل المكان / 01</span><span>RIYADH</span></div>{img('04',cls='hero-image',eager=True)}<div class="hero-image-label"><span>من صور مبلط حمامات<br><strong>الخامة تتكلم.</strong></span>{icon('spark')}</div><a href="projects/" class="hero-detail">{img('06',sizes='140px')}<span><small>نظرة أقرب</small>الجمال في<br>التفاصيل {icon('arrow')}</span></a></div></div><div class="container hero-bottom"><span>ترميم الحمامات وأعمال التبليط</span><span class="hero-bottom-line" aria-hidden="true"></span><a href="#services">اكتشف ما يناسب مساحتك {icon('arrow')}</a></div></section>
<div class="material-band"><div class="container material-inner"><div class="material-intro"><span>خامات لها حضور.</span><strong>أيّ تفاصيل تشبه ذوقك؟</strong></div><div class="material-links"><a href="services/ceramic-installation-riyadh/"><i class="material-swatch swatch-ceramic" aria-hidden="true"></i><span>سيراميك<small>إيقاع الفواصل</small></span>{icon('arrow')}</a><a href="services/porcelain-installation-riyadh/"><i class="material-swatch swatch-porcelain" aria-hidden="true"></i><span>بورسلان<small>امتداد المساحة</small></span>{icon('arrow')}</a><a href="services/marble-installation-riyadh/"><i class="material-swatch swatch-marble" aria-hidden="true"></i><span>رخام<small>شخصية العروق</small></span>{icon('arrow')}</a></div></div></div>
<section class="section services-section" id="services"><div class="container"><div class="section-heading"><div><span class="eyebrow">01 / خدماتنا</span><h2>مساحتك هي البداية.<br><em>خلّنا نرتّب تفاصيلها.</em></h2></div><div><p>تجديد حمام، أرضية لبيت، أو تشطيب لمساحة خارجية؟ اكتشف الخدمة الأقرب لفكرتك، وتعرّف على تفاصيلها قبل أول خطوة.</p><a class="text-link" href="services/">استعرض كل الخدمات {icon('arrow')}</a></div></div>{service_cards('')}</div></section>
<section class="section detail-section"><div class="container detail-grid"><figure class="detail-photo">{img('03')}<figcaption><span>من صور النشاط</span><strong>الشغل يظهر في التفاصيل.</strong></figcaption></figure><div class="detail-copy"><span class="eyebrow">02 / الحرفة في التفاصيل</span><h2>المظهر الجميل<br>يبدأ <em>بترتيب صحيح.</em></h2><p>التبليط أكثر من اختيار لون. اتجاه الصفوف، مكان القص، التقاء الجدران، والتفاصيل حول الأبواب والمصارف، كلها تصنع إحساس المساحة.</p><div class="detail-points"><div><span>01</span><div><h3>نفهم حالة المكان</h3><p>ترميم قائم أو تأسيس جديد؟ صور المكان تختصر كثيرًا من الكلام.</p></div></div><div><span>02</span><div><h3>نناقش الخامة والتوزيع</h3><p>المقاسات والنقشة وحالة السطح، قبل اعتماد تفاصيل التركيب.</p></div></div><div><span>03</span><div><h3>نوضح نطاق العمل</h3><p>المواد والتجهيز والإزالة والبنود المطلوبة تُحسم قبل البدء.</p></div></div></div>{button('تفاصيل ترميم الحمامات','services/bathroom-renovation-riyadh/','text')}</div></div></section>
<section class="section projects-section" id="work"><div class="container"><div class="section-heading"><div><span class="eyebrow">03 / من أعمالنا</span><h2>شوف الخامات.<br><em>وقرّب على التفاصيل.</em></h2></div><div><p>صور نشرها المالك في ملف «مبلط حمامات» على Google، من مراحل التنفيذ إلى التشطيب.</p>{button('المعرض الكامل','projects/','text')}</div></div>{gallery('',5)}</div></section>
<section class="section process-section"><div class="container"><div class="section-heading"><div><span class="eyebrow">04 / من الفكرة إلى التنفيذ</span><h2>طلبك يبدأ<br><em>بخطوات واضحة.</em></h2></div><p>ما تحتاج تكون حاسم كل شيء. ابدأ بما عندك من معلومات، ونناقش معك ما يحتاج توضيحًا.</p></div><ol class="process-grid"><li><span>01</span><h3>أرسل صورة ووصفًا</h3><p>نوع الخدمة، الحي، ومقاس تقريبي إذا توفر. أظهر تفاصيل المكان اللي تهمك.</p></li><li><span>02</span><h3>نراجع المطلوب</h3><p>نتحدث عن حالة السطح والخامة والتوزيع والأعمال التي تحتاج ترتيبًا قبل التبليط.</p></li><li><span>03</span><h3>نتفق على التفاصيل</h3><p>يتحدد نطاق العمل والمواد والخطوة التالية حسب احتياج المشروع وظروف الموقع.</p></li></ol></div></section>
<section class="section faq-section"><div class="container faq-grid"><div><span class="eyebrow">05 / قبل ما تبدأ</span><h2>إجابات تساعدك<br><em>تاخذ قرارك.</em></h2><p>تفاصيل مختصرة عن طلب الخدمة واختيار الخامات.</p></div>{faq([('وين تقدمون خدمات التبليط؟','نقدم خدماتنا داخل مدينة الرياض. عنوان النشاط الظاهر في الملف التجاري: طريق ابي بكر الصديق، حي المصيف، الرياض 12466. أرسل حي المشروع عند التواصل لتنسيق المتابعة.'),('هل عندكم صور من الأعمال؟','نعم، المعرض هنا يستخدم صورًا من قسم «من المالك» في الملف التجاري. تقدر تكبّر الصور أو تفتح الملف على Google لمشاهدة المزيد.'),('كيف أحصل على تكلفة للمشروع؟','أرسل صورًا ومقاسات تقريبية ونوع الخامة، ووضح هل المطلوب تركيب فقط أو إزالة وتجديد. تتحدد التكلفة بحسب مساحة العمل والتجهيز والمواد والبنود المتفق عليها.'),('هل تختارون الخامة بدلًا عني؟','نناقش معك المقاس والتوزيع وموضع الاستخدام. مواصفات المنتج وملاءمته تؤخذ من المورد، والاختيار النهائي يرتبط بذوقك واحتياج المكان.'),('هل تشمل الأعمال السيراميك والبورسلان والرخام؟','نعم، هذه من الخدمات الموجودة في الموقع، إضافة إلى ترميم الحمامات وتبليط الفلل والأحواش والأسطح. التفاصيل والنطاق يحددان حسب المشروع.')])}</div></section>
<section class="section contact-section"><div class="container contact-grid"><div><span class="eyebrow">06 / خلّنا نبدأ</span><h2>حمام يحتاج تجديد؟<br><em>أو مساحة تنتظر فكرتك؟</em></h2><p>أرسل المطلوب بالطريقة اللي تناسبك. نبدأ بصورة واضحة لما تحتاجه، ثم نناقش التفاصيل.</p><a class="contact-number" href="tel:{D['phone']}">{icon('phone')}<bdi>{D['phoneDisplay']}</bdi></a><a class="address-link" href="{e(MAPS)}" target="_blank" rel="noopener noreferrer">{icon('pin')}<span>{D['address']}<small>افتح الملف التجاري على Google {icon('external')}</small></span></a></div>{request_form()}</div></section>'''
write('/',layout('/','مبلط حمامات بالرياض | ترميم وتركيب سيراميك وبورسلان ورخام','مبلط حمامات في الرياض: ترميم وتجديد الحمامات وتركيب السيراميك والبورسلان والرخام وتبليط الفلل والأحواش. شاهد صور النشاط وتواصل على 0546562621.',home))

for s in SERVICES:
    path='/services/'+s['slug']+'/'
    pre=prefix(path)
    crumbs=[('الرئيسية','/'),('الخدمات','/services/'),(s['name'],path)]
    content=''.join(f'<section class="article-section"><span class="article-no">0{i+1}</span><div><h2>{x["title"]}</h2><p>{x["text"]}</p></div></section>' for i,x in enumerate(s['sections']))
    other=''.join(f'<a href="{pre}services/{a["slug"]}/">{icon(a["icon"])}<span>{a["name"]}</span>{icon("arrow")}</a>' for a in SERVICES if a!=s)
    checks=''.join(f'<li>{icon("check")}{t}</li>' for t in s['checklist'])
    body=f'''<section class="service-hero"><div class="container">{breadcrumbs(crumbs,pre)}<div class="service-hero-grid"><div><span class="eyebrow">{s['tag']}</span><h1>{s['title']}</h1><p class="hero-lead">{s['intro']}</p><div class="hero-actions">{button('استفسر عن الخدمة',WA,'primary','whatsapp',True)}{button('اتصل بنا','tel:'+D['phone'],'text','phone')}</div><div class="service-micro">{icon('pin')}الرياض · صور من الملف التجاري</div></div><div class="service-image">{img(s['image'],pre,eager=True)}<span>{s['name']}<small>من صور مبلط حمامات</small></span></div></div></div></section><section class="section article-wrap"><div class="container article-grid"><article>{content}<section class="service-checklist"><h2>جهّز هذه التفاصيل قبل التواصل</h2><ul>{checks}</ul><p>ما عندك كل المعلومات؟ ابدأ بوصف بسيط وصور متاحة، ونناقش ما يحتاج توضيحًا.</p>{button('أرسل تفاصيل مشروعك',WA,'primary','whatsapp',True)}</section></article><aside class="service-sidebar"><div class="sidebar-card"><span class="eyebrow">خدماتنا في الرياض</span><h2>ابدأ من احتياجك.</h2><nav aria-label="خدمات مرتبطة">{other}</nav><a class="sidebar-call" href="tel:{D['phone']}">{icon('phone')}<bdi>{D['phoneDisplay']}</bdi></a></div><a class="sidebar-photo" href="{pre}projects/">{img('06',pre,sizes='320px')}<span>تفاصيل من صور النشاط {icon('arrow')}</span></a></aside></div></section><section class="section faq-section"><div class="container faq-grid"><div><span class="eyebrow">أسئلة عن الخدمة</span><h2>تفاصيل تستحق<br><em>تكون واضحة.</em></h2></div>{faq(s['faq'])}</div></section>{contact_strip(pre)}'''
    write(path,layout(path,s['title']+' | مبلط حمامات',s['meta'],body,'service',crumbs,s))

path='/services/';pre='../';crumbs=[('الرئيسية','/'),('الخدمات',path)]
body=f'''<section class="page-hero"><div class="container">{breadcrumbs(crumbs,pre)}<span class="eyebrow">خدمات التبليط والترميم</span><h1>تفاصيل مختلفة.<br><em>واحتياجك هو البداية.</em></h1><p>من حمام صغير إلى أرضيات فيلا، استكشف الخدمات واختر المساحة الأقرب لمشروعك. كل صفحة تجمع تفاصيل تساعدك على تحديد المطلوب قبل التواصل.</p></div></section><section class="section services-page"><div class="container">{service_cards(pre)}</div></section><section class="section material-guide"><div class="container"><div class="section-heading"><div><span class="eyebrow">قبل اختيار الخامة</span><h2>ابدأ من الاستخدام،<br><em>ثم اختر الشكل.</em></h2></div><p>نوع المساحة وطريقة استخدامها وحالة السطح، أهم من اسم الخامة وحده. راجع مواصفات المنتج مع المورد قبل الشراء.</p></div><div class="table-wrap"><table><caption>نقاط للمقارنة عند اختيار خامة التبليط</caption><thead><tr><th scope="col">الخامة</th><th scope="col">ما الذي تراجعه؟</th><th scope="col">تفصيل يؤثر في التنفيذ</th></tr></thead><tbody><tr><th scope="row">السيراميك</th><td>هل المنتج للأرضيات أم الجدران؟ وهل يلائم موضع الاستخدام؟</td><td>توزيع الصفوف والقص والفواصل.</td></tr><tr><th scope="row">البورسلان</th><td>المقاس والملمس واتجاه النقشة وبيانات المنتج.</td><td>استواء السطح ومادة التثبيت ومناولة القطع.</td></tr><tr><th scope="row">الرخام</th><td>نوع الحجر والعروق ومتطلبات العناية به.</td><td>ترتيب القطع والحواف ومواد ملائمة للخامة.</td></tr></tbody></table></div></div></section>{contact_strip(pre)}'''
write(path,layout(path,'خدمات التبليط وترميم الحمامات بالرياض | مبلط حمامات','تعرف على خدمات مبلط حمامات بالرياض: ترميم الحمامات والسيراميك والبورسلان والرخام وتبليط الفلل والأحواش والأسطح، مع تفاصيل اختيار الخامات ونطاق العمل.',body,'services',crumbs))

path='/projects/';pre='../';crumbs=[('الرئيسية','/'),('من أعمالنا',path)]
body=f'''<section class="page-hero"><div class="container">{breadcrumbs(crumbs,pre)}<span class="eyebrow">صور المالك من الملف التجاري</span><h1>من مراحل الشغل،<br><em>إلى شكل التفاصيل.</em></h1><p>صور من ملف «مبلط حمامات» على Google. استعرض تشطيبات الحمامات والأرضيات ومراحل التركيب، واضغط على أي صورة لمشاهدتها بحجم أكبر.</p><a class="text-link" href="{e(MAPS)}" target="_blank" rel="noopener noreferrer">شاهد الملف التجاري على Google {icon('external')}</a></div></section><section class="section full-gallery"><div class="container gallery-browser"><div class="gallery-toolbar"><div class="gallery-filters" role="group" aria-label="تصفية صور الأعمال" hidden><button type="button" data-gallery-filter="all" aria-pressed="true">كل الصور</button><button type="button" data-gallery-filter="bathrooms" aria-pressed="false">تشطيبات الحمامات</button><button type="button" data-gallery-filter="installation" aria-pressed="false">مراحل التركيب</button><button type="button" data-gallery-filter="outdoor" aria-pressed="false">المساحات الخارجية</button></div><p class="gallery-result" role="status" aria-live="polite"></p></div>{gallery(pre)}<div class="gallery-note">{icon('grid')}صور توضح مراحل مختلفة من العمل؛ تفاصيل الطلب ونطاقه تناقش بحسب موقعك والخامة المطلوبة.</div></div></section>{contact_strip(pre)}'''
write(path,layout(path,'صور أعمال التبليط وترميم الحمامات | مبلط حمامات بالرياض','شاهد صورًا من الملف التجاري لمبلط حمامات في الرياض: تشطيب حمامات وأرضيات ومراحل تركيب البلاط وتفاصيل المصارف والحواف، مع معرض قابل للتكبير.',body,'projects',crumbs))

path='/contact/';pre='../';crumbs=[('الرئيسية','/'),('تواصل معنا',path)]
body=f'''<section class="page-hero"><div class="container">{breadcrumbs(crumbs,pre)}<span class="eyebrow">نسمع فكرتك ونرتّب تفاصيلها</span><h1>خلّنا نبدأ<br><em>من مساحتك.</em></h1><p>لترميم الحمامات وأعمال السيراميك والبورسلان والرخام في الرياض، شاركنا نوع الخدمة وموقع المشروع وصورًا إذا توفرت.</p></div></section><section class="section contact-page"><div class="container contact-grid"><div><div class="contact-info-card"><span class="eyebrow">التواصل المباشر</span><a class="contact-number" href="tel:{D['phone']}">{icon('phone')}<bdi>{D['phoneDisplay']}</bdi></a>{button('تواصل عبر واتساب',WA,'primary','whatsapp',True)}<div class="contact-info-line">{icon('pin')}<div><h2>عنوان النشاط</h2><p>{D['address']}</p><a class="text-link" href="{e(MAPS)}" target="_blank" rel="noopener noreferrer">افتح الملف على Google {icon('external')}</a></div></div><div class="contact-info-line">{icon('clock')}<div><h2>ساعات العمل</h2><dl class="hours-list"><div><dt>الأحد</dt><dd>٩ ص – ٨ م</dd></div><div><dt>الاثنين إلى السبت</dt><dd>٥:٣٠ ص – ١٠ م</dd></div></dl></div></div><p>خدماتنا داخل مدينة الرياض. اذكر حي المشروع لتنسيق تفاصيل المتابعة.</p></div></div>{request_form()}</div></section>'''
write(path,layout(path,'تواصل مع مبلط حمامات بالرياض | 0546562621','تواصل مع مبلط حمامات على 0546562621 أو واتساب. طريق ابي بكر الصديق، المصيف، الرياض 12466. تعرف على ساعات العمل وأرسل تفاصيل مشروع التبليط أو الترميم.',body,'contact',crumbs))

path='/privacy/';pre='../';crumbs=[('الرئيسية','/'),('الخصوصية',path)]
body=f'''<section class="page-hero"><div class="container">{breadcrumbs(crumbs,pre)}<span class="eyebrow">وضوح في التعامل</span><h1>خصوصيتك.</h1><p>آخر تحديث: ٨ نوفمبر ٢٠٢٦</p></div></section><section class="section"><article class="container prose"><h2>المعلومات في نموذج التواصل</h2><p>يستخدم النموذج اسم الخدمة والحي وتفاصيل العمل التي تكتبها لتجهيز رسالة على جهازك وفتحها في واتساب. لا يوجد في الموقع خادم يستقبل هذه المدخلات أو قاعدة بيانات تحفظها. اختر المعلومات التي ترغب في إرسالها، وراجع الرسالة داخل واتساب قبل إرسالها.</p><h2>الخدمات الخارجية</h2><p>روابط واتساب وخرائط Google وموقع المطور تنقلك إلى خدمات مستقلة تخضع لسياسات الخصوصية الخاصة بها. صور الأعمال مستضافة ضمن ملفات الموقع، ولا تُحمّل مباشرة من خرائط Google أثناء تصفح المعرض.</p><h2>الاستضافة</h2><p>الموقع مستضاف على Vercel. قد تعالج منصة الاستضافة بيانات تقنية لازمة لتقديم الصفحات وحماية الخدمة، مثل عنوان الاتصال وطلب الصفحة. لا يضيف كود الموقع أدوات تحليلات أو ملفات تعريف ارتباط تسويقية.</p><h2>الاستفسارات</h2><p>للاستفسار عن التواصل مع النشاط، اتصل على <a class="text-link" href="tel:{D['phone']}"><bdi>{D['phoneDisplay']}</bdi></a>.</p></article></section>'''
write(path,layout(path,'سياسة الخصوصية | مبلط حمامات','معلومات عن خصوصية نموذج التواصل وروابط واتساب وخرائط Google واستضافة موقع مبلط حمامات.',body,'privacy',crumbs,noindex=True))

notfound=f'<section class="page-hero not-found"><div class="container"><span class="eyebrow">404</span><h1>الصفحة غير موجودة.</h1><p>تقدر ترجع للرئيسية أو تتصفح خدمات التبليط والترميم.</p>{button("العودة إلى الرئيسية","/","primary")}</div></section>'
(ROOT/'404.html').write_text(layout('/404.html','الصفحة غير موجودة | مبلط حمامات','الصفحة المطلوبة غير موجودة.',notfound,'404',noindex=True).replace('../','/'))

paths=['/','/services/','/projects/','/contact/']+['/services/'+s['slug']+'/' for s in SERVICES]
ns='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',ns)
root=ET.Element('{'+ns+'}urlset')
for p in paths:
    node=ET.SubElement(root,'{'+ns+'}url');ET.SubElement(node,'{'+ns+'}loc').text=BASE+p
    ET.SubElement(node,'{'+ns+'}lastmod').text='2026-11-08'
ET.ElementTree(root).write(ROOT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: '+BASE+'/sitemap.xml\n')
(ROOT/'site.webmanifest').write_text(json.dumps({'name':D['name'],'short_name':D['name'],'lang':'ar-SA','dir':'rtl','start_url':'./','display':'standalone','background_color':'#f7f9fb','theme_color':'#2468ab','icons':[{'src':'assets/icon-192.png?v='+ASSET_VERSION,'sizes':'192x192','type':'image/png'},{'src':'assets/icon-512.png?v='+ASSET_VERSION,'sizes':'512x512','type':'image/png'}]},ensure_ascii=False))
print('Built 10 indexable pages, privacy page, 404, sitemap and manifest.')
