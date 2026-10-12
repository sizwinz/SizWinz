from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
R=Path(__file__).resolve().parents[1];A=R/'assets'
W=900
for mode in ('dark','light'):
    bg=(12,16,20) if mode=='dark' else (253,253,251)
    fg=(223,223,218) if mode=='dark' else (45,50,54)
    # collect section rows with logical (browser CSS pixel) sizes, retain HANCORE's exact visual margins.
    rows=[('wordmark',220,88,14),('bio-wide',744,76,30),('label-main',248,28,27),
        ('FEATURES',744,358,5),('INFOS',744,108,0),('SMALL',744,92,0),
        ('label-gallery',248,28,28),('GALLERY1',744,270,11),('GALLERY2',744,306,0),('connected-archive',248,92,4),('closing',248,61,21)]
    # gallery 2: original connected art render 612 high =306px
    H=60+sum(r[2]+r[3] for r in rows)+210
    out=Image.new('RGB',(W,H),bg)
    d=ImageDraw.Draw(out)
    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
    y=28
    def paste_img(name,x,y,w,h):
        im=Image.open(A/f'{name}-{mode}.png').convert('RGBA')
        im=im.resize((w,h),Image.Resampling.LANCZOS)
        out.paste(im,(int(x),int(y)),im)
    for key,w,h,gap in rows:
        y+=gap
        left=(W-w)//2
        if key=='FEATURES':
            for i,name in enumerate(['pocketmc','msm','studysage']):paste_img('connected-feature-'+name,left+i*248,y,248,358)
        elif key=='INFOS':
            for i in range(2):paste_img('connected-info-'+str(i),left+i*372,y,372,108)
        elif key=='SMALL':
            for i in range(3):paste_img('connected-info-small-'+str(i),left+i*248,y,248,92)
        elif key=='GALLERY1':
            for i,name in enumerate(['gitfetch','skillwise','serverpulse']):paste_img('connected-gallery-'+name,left+i*248,y,248,270)
        elif key=='GALLERY2':
            for i,name in enumerate(['releasewave','campus','saas']):paste_img('connected-gallery-'+name,left+i*248,y,248,306)
        else:paste_img(key,left,y,w,h)
        y+=h
    d.text((W//2, y+20),'sahaj33.me     •     PocketMC     •     DS Labs',fill=fg,font=font,anchor='mt')
    d.text((W//2,y+79),'Discord     Credits',fill=fg,font=font,anchor='mt')
    d.text((W//2,y+125),'Profile layout inspired by HANCORE · MIT licensed artwork',fill=fg,font=font,anchor='mt')
    out=out.crop((0,0,W,y+170))
    out.save(R/f'preview-{mode}.png',optimize=True)
    print(R/f'preview-{mode}.png',out.size)
