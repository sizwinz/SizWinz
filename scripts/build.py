#!/usr/bin/env python3
"""Rebuild SizWinz's README visual assets using HANCORE's original MIT card/route SVG geometry.
Origin: https://github.com/HANCORE-linux/HANCORE-linux/tree/main/folio
Licensed under HANCORE's MIT License (copyright (c) 2025 HANCORE); see LICENSE-HANCORE.
The base card mounts, paths, shadows and connectors are adapted from HANCORE's SVG source assets.
All preview panels, project names and links are specific to SizWinz.
"""
from pathlib import Path
from xml.sax.saxutils import escape
import io, re
import cairosvg
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
DEST=ROOT/'assets'; DEST.mkdir(exist_ok=True)
SRC=ROOT/'source'; SRC.mkdir(exist_ok=True)
COLORS={
    'dark':{'panel':'#191c1e','border':'#353a3d','pic':'#101213','white':'#e8e3d9','soft':'#bfc4c9','wire':'#48525b','orange':'#df6124','ui':'#0c1011','glass':'#202627','muted':'#869195'},
    'light':{'panel':'#f3f2ef','border':'#b9c0c1','pic':'#ecece9','white':'#242b31','soft':'#55616a','wire':'#8d969b','orange':'#c34f1b','ui':'#eff0ed','glass':'#e5e8e5','muted':'#68737b'}
}
FONT='IBM Plex Sans, DejaVu Sans, Arial, sans-serif'
MONO='DejaVu Sans Mono, monospace'
SVGHEAD='<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {vw} {vh}" role="img" aria-label="{label}">'
DEF='''<defs><filter id="float" x="-15%" y="-15%" width="130%" height="150%" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="8"/><feOffset dy="10"/></filter></defs>'''

def open_svg(w,h,desc,upscale=2):
    return SVGHEAD.format(w=int(w*upscale),h=int(h*upscale),vw=w,vh=h,label=escape(desc,{'"':'&quot;'}))

def txt(x,y,s,size,color,weight=500,anchor='start',font=None,letter=0):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{color}" font-family="{font or FONT}" font-size="{size}" font-weight="{weight}" letter-spacing="{letter}">{escape(s)}</text>'

def rect(x,y,w,h,fill,rx=0,stroke=None,sw=1):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="{sw}"' if stroke else '')+'/>'

def path(d,stroke,sw=2.5):
    return f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}" />'

def line(x1,y1,x2,y2,col,sw=2.5):
    return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{col}" stroke-width="{sw}" fill="none"/>'

def svgimg(name,w,h,body,desc):
    src=open_svg(w,h,desc)+body+'</svg>'
    (SRC/(name+'.svg')).write_text(src,encoding='utf-8')
    cairosvg.svg2png(bytestring=src.encode(),write_to=str(DEST/(name+'.png')))
    return Image.open(DEST/(name+'.png')).convert('RGBA')

def frame(W,H,variant,inner=None):
    c=COLORS[variant]
    # exact frame path and floating-shadow geometry reused from folio/shibumi-dark.svg / folio/info-waybar-dark.svg
    return DEF+f'<path d="M24 16H{W-24}V{H-54}L{W-46} {H-32}H24Z" fill="#000000" opacity="0.48" filter="url(#float)" />'+f'<path d="M24 16H{W-24}V{H-54}L{W-46} {H-32}H24Z" fill="{c["panel"]}" stroke="{c["border"]}" stroke-width="1.5" />'+(inner or '')

def shadowless_frame(W,H,variant):
    c=COLORS[variant];return f'<path d="M24 16H{W-24}V{H-54}L{W-46} {H-32}H24Z" fill="{c["panel"]}" stroke="{c["border"]}" stroke-width="1.5" />'

def save_simple(name,w,h,body,variant,desc):
    return svgimg(f'{name}-{variant}',w,h,body,desc)

def composed(name,variant,base,w,h,x,y,wires,desc):
    """Render HANCORE's originally independent card-and-connector assembly to static PNG.
    The upstream source used <image href=> in an SVG. We flatten it to PNG for reliable GitHub display.
    """
    canvas=Image.new('RGBA',(2*w,2*h),(0,0,0,0))
    canvas.alpha_composite(base,(2*x,2*y))
    overlay=open_svg(w,h,desc)+wires+'</svg>'
    (SRC/(f'{name}-{variant}.svg')).write_text(overlay,encoding='utf8')
    render=Image.open(io.BytesIO(cairosvg.svg2png(bytestring=overlay.encode()))).convert('RGBA')
    canvas.alpha_composite(render)
    canvas.save(DEST/f'{name}-{variant}.png',optimize=True)

def wire_feature(position,variant):
    c=COLORS[variant]; d='#e8e3d9' if variant=='dark' else '#55616a'
    # Exact paths from folio/connected-{shibumi,omaq,marketplace}-dark.svg
    if position==0:return path('M624 48H312V136M312 788V900',c['wire'])+path('M468 48H524',d,3.5)+path('M301 136H323M301 788H323',d,3)
    if position==1:return path('M0 48H624M312 8V136M312 788V900',c['wire'])+path('M312 76V112',d,3.5)+path('M301 136H323M301 788H323',d,3)+rect(308,4,8,8,c['orange'])
    return path('M0 48H312V136M312 788V900',c['wire'])+path('M100 48H156',d,3.5)+path('M301 136H323M301 788H323',d,3)

def wire_gallery(pos,variant,row):
    c=COLORS[variant];d='#e8e3d9' if variant=='dark' else '#55616a'
    if row==0:
        if pos==0:return path('M624 48H312V136M312 596V680',c['wire'])+path('M468 48H524',d,3.5)+path('M301 136H323M301 596H323',d,3)
        if pos==1:return path('M0 48H624M312 8V136M312 596V680',c['wire'])+path('M312 76V112',d,3.5)+path('M301 136H323M301 596H323',d,3)+rect(308,4,8,8,c['orange'])
        return path('M0 48H312V136M312 596V680',c['wire'])+path('M100 48H156',d,3.5)+path('M301 136H323M301 596H323',d,3)
    if pos==0:return path('M312 0V56M312 524V584H624',c['wire'])+path('M312 12V32M468 584H524',d,3.5)+path('M301 56H323M301 524H323',d,3)
    if pos==1:return path('M312 0V56M312 524V612',c['wire'])+path('M312 12V32',d,3.5)+path('M301 56H323M301 524H323',d,3)
    return path('M312 0V56M312 524V584H0',c['wire'])+path('M312 12V32M100 584H156',d,3.5)+path('M301 56H323M301 524H323',d,3)

# 01. HEADER (upstream wordmark dimensions/typographic colors; mark is an original SZ signet).
for variant in COLORS:
    c=COLORS[variant]
    mark='<g transform="translate(173 11)" fill="#df6124"><path d="M8 0H75V14H21L14 21V31H61L77 47V64L61 80H0V66H55L63 58V48H17L0 31V16Z"/><path d="M83 0H91V14H83Z"/></g>'
    # Name centered under reused wordmark spacing
    body=mark+txt(220,154,'SIZWINZ',40,c['orange'],700,'middle',letter=2)
    save_simple('wordmark',440,176,body,variant,'SizWinz logo')
    # Reuse same compact bio-wide frame, dimensions, and double-line typography.
    bio=frame(1872,192,variant)+txt(936,72,'Computer Engineering student. Builder of practical software.',46,c['white'],600,'middle')+txt(936,126,'Desktop apps, developer tools and privacy-minded systems.',46,c['soft'],500,'middle')
    save_simple('bio-wide',1872,192,bio,variant,'Sahaj Italiya: building practical desktop and developer tools')
    nbio=frame(704,406,variant)
    for y,t,weight,col in [(73,'Computer Engineering',600,c['white']),(127,'student & software builder.',600,c['white']),(198,'Desktop apps, tools,',500,c['soft']),(252,'and practical AI.',500,c['soft']),(323,'Built with care.',500,c['soft'])]:nbio+=txt(352,y,t,44,col,weight,'middle')
    save_simple('bio-narrow',704,406,nbio,variant,'Computer Engineering student and software builder')
    for name,label in [('label-main','Desktop apps & systems.'),('label-gallery','More things I build.'),('label-about','How I like to build.')]:
        save_simple(name,248,28,txt(124,20,label,16,c['white'],600,'middle'),variant,label)

FEATURES=[
 ('pocketmc','PocketMC','Windows Minecraft server management','C#  /  .NET 8  /  WPF', 'PocketMC dashboard'),
 ('msm','MSM','Minecraft servers from your phone','PYTHON  /  TERMUX  /  SQLITE', 'MSM terminal'),
 ('studysage','StudySage','Offline-first study companion','PYTHON  /  NLP  /  OCR', 'StudySage note summary'),
]

def feature_art(name,variant):
    c=COLORS[variant]
    cream=c['white'];mut=c['soft'];orange=c['orange'];border=c['border']
    # The content below depicts stylized interfaces, NOT captured screenshots.
    win=rect(32,35,560,548,c['pic'])+rect(32,35,560,36,c['glass'])+''.join(f'<circle cx="{xx}" cy="53" r="5" fill="{clr}" />' for xx,clr in [(50,'#c65b47'),(67,'#bd9e47'),(84,'#57816d')])
    if name=='pocketmc':
        b=win+txt(112,58,'PocketMC / Server Dashboard',18,cream,500)
        b+=rect(50,91,119,468,c['glass'],6)+txt(68,129,'POCKETMC',17,orange,700)
        b+=line(65,148,152,148,border,2)
        for yy,label in [(189,'Overview'),(232,'Servers'),(275,'Backups'),(318,'Plugins'),(361,'Settings')]:
            b+=rect(60,yy-26,99,35,'#31383a' if yy==189 and variant=='dark' else c['panel'],4)+txt(70,yy,label,15,cream if yy==189 else mut)
        b+=txt(191,129,'SURVIVAL WORLD',23,cream,700)+rect(481,102,80,33,'#275039' if variant=='dark' else '#c4e7ce',5)+txt(521,124,'ONLINE',13,'#8ddea1' if variant=='dark' else '#27633f',600,'middle')
        b+=rect(191,156,175,88,c['glass'],5)+rect(378,156,184,88,c['glass'],5)
        b+=txt(205,183,'CPU USAGE',15,mut)+txt(205,223,'18.4%',29,cream,700)
        b+=txt(393,183,'MEMORY',15,mut)+txt(393,223,'2.3 GB',29,cream,700)
        b+=rect(191,262,371,248,c['glass'],5)+txt(208,295,'Console',17,cream,600)+line(208,313,540,313,border,2)
        for yy,label,co in [(346,'[14:05] Preparing spawn region',mut),(381,'[14:05] Done! Server started', '#8fc69d'),(416,'[14:06] Player joined the game',mut),(451,'[14:07] Autosave complete','#8fc69d')]:b+=txt(207,yy,label,14,co,500,font=MONO)
    elif name=='msm':
        b=win+txt(110,58,'Termux / Minecraft Server Manager',17,cream,500,font=MONO)
        b+=txt(58,109,'$ msm',21,orange,600,font=MONO)+txt(58,157,'MINECRAFT SERVER MANAGER',24,cream,700,font=MONO)
        b+=line(58,174,552,174,border,2)
        for yy,a,v,co in [(214,'SERVER','survival',cream),(247,'STATUS','RUNNING','#91bd96'),(280,'PLAYERS','3 / 20',cream),(313,'MEMORY','1.8 GB',cream)]:
            b+=txt(59,yy,a,17,mut,500,font=MONO)+txt(289,yy,v,17,co,600,font=MONO)
        b+=rect(57,341,492,121,c['glass'],4)
        for yy,t in [(374,'[1] Start server      [2] Stop server'),(409,'[3] Backups          [4] View logs'),(444,'[5] Settings         [6] Exit')]:b+=txt(72,yy,t,16,mut,500,font=MONO)
        b+=txt(60,505,'> choose an action _',17,orange,500,font=MONO)
    else:
        b=win+txt(112,58,'StudySage / Workspace',18,cream,500)
        b+=rect(50,91,209,450,c['glass'],4)+txt(70,120,'Notes / Lecture 04',17,cream,600)
        for yy,ww in [(153,158),(182,142),(211,172),(240,132),(269,171),(298,152)]:b+=rect(70,yy,ww,8,mut,2)
        b+=rect(70,349,170,72,c['pic'],4)+txt(88,381,'OCR Complete',16,orange,600)+txt(88,404,'12 pages',14,mut)
        b+=rect(275,91,292,450,c['glass'],4)+txt(298,125,'AI Summary',22,cream,700)
        for yy,ww in [(160,240),(188,218),(216,248),(244,206)]:b+=rect(296,yy,ww,8,mut,2)
        b+=line(296,281,542,281,border,2)+txt(298,320,'Quick Quiz',19,cream,700)
        for yy,s in [(359,'1. Key takeaway?'),(397,'2. Explain the model.'),(435,'3. Define the concept.')]:b+=txt(299,yy,s,16,mut)
        b+=rect(299,465,241,46,'#472a1c' if variant=='dark' else '#f3d9c7',6)+txt(419,494,'Generate quiz  →',17,orange,600,'middle')
    return b

for v in COLORS:
    c=COLORS[v]
    for i,(slug,title,tagline,tech,desc) in enumerate(FEATURES):
        body=frame(624,700,v)
        body+=feature_art(slug,v)
        body+=txt(312,636,title,34,c['white'],600,'middle')
        base=save_simple('feature-'+slug,624,700,body,v,desc)
        composed('connected-feature-'+slug,v,base,624,900,0,120,wire_feature(i,v),desc+' with original HANCORE connector pattern')

# Original neutral cut-corner info cards: adapted from folio/info-waybar-dark.svg.
def info_body(variant,title,detail):
    c=COLORS[variant]
    return frame(624,192,variant)+txt(312,72,title,40,c['white'],600,'middle')+txt(312,126,detail,31,c['soft'],500,'middle')

for v in COLORS:
    c=COLORS[v];d=c['white']
    infos=[('DS Labs','Products made to be used.'),('Open source','Built in the open.')]
    for i,(title,desc) in enumerate(infos):
        b=save_simple('info-'+str(i),624,192,info_body(v,title,desc),v,title)
        # 936x272: first card on x312, second card on x0, same independent upstream route technique
        x=312 if i==0 else 0
        paths=(path('M312 0V272M936 0V272M312 120H336',c['wire'])+path('M336 113V127',d,3)) if i==0 else (path('M624 0V272M0 0V272M600 120H624',c['wire'])+path('M600 113V127',d,3))
        composed('connected-info-'+str(i),v,b,936,272,x,40,paths,title)

    extras=[('WatchMark','Local-first media tracker.'),('SchemeSetu','Smarter scheme matching.'),('PocketMC on Linux','Cross-platform server tools.')]
    for i,(title,detail) in enumerate(extras):
        b=save_simple('info-small-'+str(i),624,192,info_body(v,title,detail),v,title)
        w=path('M312 0V56',c['wire'])+path('M312 12V32',d,3.5)+path('M301 56H323',d,3)
        composed('connected-info-small-'+str(i),v,b,624,232,0,40,w,title)

GALLERY=[
 ('gitfetch','GitFetch','TypeScript  ·  React', 'Developer profile analyzer'),
 ('skillwise','SkillWise','Python  ·  Streamlit','Learning roadmap generator'),
 ('serverpulse','ServerPulse','Discord  ·  Python','Community analytics bot'),
 ('releasewave','ReleaseWave','Python  ·  automation','Diff-powered changelogs'),
 ('campus','Campus Assistant','FastAPI  ·  Next.js','Multilingual education AI'),
 ('saas','SaaS Inspector','TypeScript  ·  research','Evidence-based idea research'),
]

def gallery_art(slug,variant):
    c=COLORS[variant];cream=c['white'];mut=c['soft'];orange=c['orange'];bg=c['glass']
    b=rect(32,24,560,325,c['pic'])+rect(32,24,560,27,c['glass'])+txt(47,43,slug+' / preview',14,mut,500,font=MONO)
    if slug=='gitfetch':
        for xx,lab,num in [(55,'REPOS','39'),(235,'COMMITS','2.1K'),(416,'ACTIVITY','↗')]:
            b+=rect(xx,70,154,94,bg,4)+txt(xx+11,99,lab,15,mut,600)+txt(xx+11,146,num,34,cream,700)
        b+=txt(56,198,'CONTRIBUTION ACTIVITY',14,mut,500)
        for row in range(4):
            for col in range(19):
                color=['#243329','#344d38','#648969','#a7c2a0'][(col*7+row*3)%4] if variant=='dark' else ['#d3dfd1','#a7c4a6','#6d9d72','#477b50'][(col*7+row*3)%4]
                b+=rect(56+col*27,213+row*29,20,20,color,2)
    elif slug=='skillwise':
        b+=txt(58,93,'Your learning path',25,cream,700)
        b+=line(101,159,101,309,c['border'],4)
        for i,(t1,t2) in enumerate([('01','Foundation'),('02','Build projects'),('03','Go deeper')]):
            y=150+i*67;b+=f'<circle cx="101" cy="{y}" r="13" fill="{orange}" />'+txt(145,y+8,t1+'   '+t2,21,cream,500)
    elif slug=='serverpulse':
        b+=txt(57,89,'Community growth',24,cream,700)
        for x,y,h in [(70,236,80),(124,200,116),(178,214,102),(232,167,149),(286,191,125),(340,136,180),(394,165,151),(448,103,213),(502,124,192)]:
            b+=rect(x,y,35,h,'#d96c3a' if (x//54)%3==0 else '#678479',2)
    elif slug=='releasewave':
        b+=txt(57,91,'CHANGELOG  /  v2.4.0',22,cream,700,font=MONO)
        for yy,tag,detail in [(145,'+','New backup engine'),(192,'+','Faster startup'),(239,'~','Safer fallbacks'),(286,'-','Removed legacy flags')]:
            b+=txt(62,yy,tag,25,orange,700,font=MONO)+txt(104,yy,detail,20,mut,500,font=MONO)
    elif slug=='campus':
        b+=txt(56,88,'Ask your campus',23,cream,700)
        b+=rect(55,107,420,65,bg,6)+txt(73,132,'What is the exam timetable?',16,cream)+txt(73,156,'English / हिन्दी / ગુજરાતી',13,mut)
        b+=rect(116,189,422,95,bg,6)+txt(137,223,'I found the relevant notice.',16,cream)+txt(137,250,'View sources  →',15,orange,600)
    else:
        b+=txt(56,92,'Market opportunity score',22,cream,700)
        for i,(t,val) in enumerate([('Demand',78),('Competition',42),('Reach',63)]):
            y=134+i*64;b+=txt(56,y,t,19,mut)+rect(220,y-16,320,17,bg,8)+rect(220,y-16,val*3.15,17,orange if i==0 else '#779185',8)+txt(556,y,str(val),16,cream,600,'end')
    return b

for v in COLORS:
    c=COLORS[v]
    for i,(slug,title,tech,desc) in enumerate(GALLERY):
        # same independent theme-card proportions as HANCORE's 3x2 gallery, 624x492
        art=frame(624,492,v)+gallery_art(slug,v)
        art+=txt(50,402,title,32,c['white'],600)+txt(50,444,tech,23,c['soft'],500)
        standalone=save_simple('gallery-'+slug,624,492,art,v,desc)
        row=0 if i<3 else 1;pos=i%3
        y=120 if row==0 else 40
        h=680 if row==0 else 612
        composed('connected-gallery-'+slug,v,standalone,624,h,0,y,wire_gallery(pos,v,row),desc)

    # CTA from same compact card template.
    archive=save_simple('archive',624,192,info_body(v,'More repositories','Browse the full collection  →'),v,'Browse all GitHub projects')
    wires=path('M312 0V56',c['wire'])+path('M312 12V32',c['white'],3.5)+path('M301 56H323',c['white'],3)
    composed('connected-archive',v,archive,624,232,0,40,wires,'All repositories')
    # Slim stats/info panel, no fabricated metrics.
    base=frame(624,122,v)+txt(312,74,'DESIGN   ·   ENGINEER   ·   SHIP',26,c['orange'],600,'middle')
    save_simple('closing',624,122,base,v,'Design engineer ship')

print('Created',len(list(DEST.glob('*.png'))),'PNG assets; same card frame and connectors as HANCORE source.')
