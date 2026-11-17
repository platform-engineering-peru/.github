"""Build portable profile illustrations using approved assets and outlined type.

Requires fonttools==4.60.1. Run from any directory; output paths are repo-relative.
The source raster artwork is embedded byte-for-byte, never redrawn or recolored.
"""
from pathlib import Path
from base64 import b64encode
from html import escape
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'profile/assets'
FONTS = {}
for weight in (400, 500, 600, 700):
    font = instantiateVariableFont(TTFont(ROOT / 'design/fonts/epilogue-variable.ttf'), {'wght': weight})
    FONTS[weight] = (font, font.getGlyphSet(), font.getBestCmap())
VIOLET, GREEN, LAVENDER, NAVY = '#5B2EFF', '#00D96E', '#C4B5FD', '#090C20'
PAPER, WHITE = '#F0ECFF', '#FFFFFF'

def text(label, x, y, size=24, color=NAVY, weight=400, tracking=0):
    font, glyphs, cmap = FONTS[weight]
    scale = size / font['head'].unitsPerEm
    pieces = []
    cursor = x
    for char in label:
        name = cmap.get(ord(char), '.notdef')
        pen = SVGPathPen(glyphs)
        glyphs[name].draw(pen)
        if pen.getCommands():
            pieces.append(f'<path d="{pen.getCommands()}" transform="translate({cursor:.2f} {y}) scale({scale:.5f} {-scale:.5f})"/>')
        cursor += glyphs[name].width * scale + tracking
    return f'<g fill="{color}" aria-label="{escape(label)}">'+''.join(pieces)+'</g>'

def rect(x, y, w, h, fill, rx=0, stroke='none'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>'

def path(d, stroke, width=1, opacity=1):
    return f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{width}" opacity="{opacity}" stroke-linecap="round" stroke-linejoin="round"/>'

def circle(x,y,r,fill,stroke='none'):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}"/>'

def arrow(x,y,color=NAVY):
    return path(f'M{x} {y+20} l24 -24 M{x+2} {y-4} h22 v22',color,3)

def embed(name,x,y,w,h):
    mime='image/png' if name.endswith('.png') else 'image/webp'
    data=b64encode((OUT/name).read_bytes()).decode()
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="data:{mime};base64,{data}"/>'

def save(name,w,h,content,title):
    (OUT/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{escape(title)}</title><defs><clipPath id="bounds"><rect width="{w}" height="{h}" rx="28"/></clipPath></defs><g clip-path="url(#bounds)">{content}</g></svg>\n')

def contours(x,y,color,count=7):
    return ''.join(path(f'M{x-150} {y+i*17} C{x+80} {y-210+i*17} {x+150} {y+280+i*17} {x+370} {y+20+i*17} S{x+700} {y-90+i*17} {x+800} {y+90+i*17}',color,1,0.24) for i in range(count))

# The welcome artwork is self-contained, with a separately composed mobile cover.
for mobile in (False, True):
    w,h=(720,820) if mobile else (1200,560)
    c=rect(0,0,w,h,PAPER,28)
    c+=text('PLATFORM ENGINEERING',44,58,20,VIOLET,600,1.1)
    c+=text('PERÚ',44,86,17,NAVY,500,2)
    c+=rect(121,73,7,12,'#E61530')+rect(128,73,7,12,WHITE)+rect(135,73,7,12,'#E61530')
    if mobile:
        c+=contours(100,530,VIOLET)
        c+=text('Better platforms.',44,175,60,NAVY,700)
        c+=text('Built together.',44,248,60,VIOLET,700)
        c+=text('A community for the people',44,300,25,NAVY,400)
        c+=text('behind the platforms.',44,335,25,NAVY,400)
        c+=embed('official-mark.png',200,370,320,320)
        c+=circle(53,745,5,GREEN)+text('ROOTED IN PERU. OPEN TO EVERYONE.',72,752,18,NAVY,500)
        c+=text('LEARN / CONNECT / CONTRIBUTE',44,790,14,VIOLET,500,1)
    else:
        c+=contours(750,210,VIOLET)
        c+=text('Better platforms.',44,210,74,NAVY,700)
        c+=text('Built together.',44,300,74,VIOLET,700)
        c+=text('A community for the people',47,358,26,NAVY,400)
        c+=text('behind the platforms.',47,394,26,NAVY,400)
        c+=embed('official-mark.png',807,95,365,365)
        c+=path('M44 464 H1156',VIOLET,1,0.23)
        c+=circle(51,508,5,GREEN)+text('ROOTED IN PERU. OPEN TO EVERYONE.',70,515,17,NAVY,500)
        c+=text('LEARN / CONNECT / CONTRIBUTE',790,515,15,VIOLET,500,0.4)
    save('cover-mobile.svg' if mobile else 'cover.svg',w,h,c,'Platform Engineering Perú. Better platforms. Built together.')

# Each card is a complete 400 px component that can wrap naturally on mobile.
for kind in ('gatherings','resources','memories','community'):
    bg,fg,accent = {'gatherings':(VIOLET,WHITE,LAVENDER),'resources':(PAPER,NAVY,VIOLET),'memories':(NAVY,WHITE,GREEN),'community':(GREEN,NAVY,NAVY)}[kind]
    c=rect(0,0,800,480,bg,28)
    number={'gatherings':'01','resources':'02','memories':'03','community':'04'}[kind]
    c+=text(number+' / '+kind.upper(),40,52,19,fg,500,1)
    c+=circle(735,50,25,'none',fg)+arrow(723,46,fg)
    if kind=='gatherings':
        # A conversational constellation, deliberately irregular rather than a logo.
        for x,y,r in [(612,180,22),(716,233,14),(584,289,14),(718,343,22),(644,388,8)]:
            c+=path(f'M612 180 L{x} {y} L718 343',LAVENDER,2,0.45)+circle(x,y,r,'none',LAVENDER)
        c+=circle(612,180,7,GREEN)+circle(718,343,7,WHITE)
        lines=['Good conversations.','Better connections.']
        c+=text(lines[0],40,204,43,fg,600)+text(lines[1],40,258,43,fg,600)
        desc='Real people. Shared experiences.'
        c+=text(desc,40,356,24,fg,400)
        c+=text('FIND A GATHERING',40,432,18,fg,500,1)
    elif kind=='resources':
        for i,col in enumerate([VIOLET,GREEN,LAVENDER]):
            c+=rect(568+i*55,159-i*8,48,185+i*8,col,5)
            c+=path(f'M{578+i*55} 188 h25 M{578+i*55} 198 h25',NAVY,2,0.35)
        c+=text('Ideas worth',40,204,53,fg,600)+text('building on.',40,266,53,fg,600)
        c+=text('A little curiosity goes a long way.',40,356,24,fg,400)
        c+=text('OPEN THE KNOWLEDGE ARCHIVE',40,432,18,fg,500,1)
    elif kind=='memories':
        c+=contours(440,188,LAVENDER,5)
        for x,y in [(610,170),(650,235),(700,290)]:
            c+=rect(x,y,70,54,'none',5,LAVENDER)
            c+=circle(x+19,y+18,6,GREEN)+path(f'M{x+10} {y+42} l15 -12 l12 8 l15 -15 l12 19',LAVENDER,2)
        c+=text('More than',40,204,53,fg,600)+text('a meetup.',40,266,53,fg,600)
        c+=text('The moments that make us, us.',40,356,24,LAVENDER,400)
        c+=text('EXPLORE OUR MEMORIES',40,432,18,GREEN,500,1)
    else:
        for x,y,r in [(630,207,63),(694,270,63),(630,333,63)]:
            c+=circle(x,y,r,'none',NAVY)
        c+=circle(630,207,7,NAVY)+circle(694,270,7,NAVY)+circle(630,333,7,NAVY)
        c+=text('Your people.',40,204,53,fg,600)+text('Your place.',40,266,53,fg,600)
        c+=text('Every level. Every perspective.',40,356,24,fg,400)
        c+=text('MEET THE COMMUNITY',40,432,18,fg,500,1)
    save(kind+'.svg',800,480,c,{'gatherings':'Gatherings — Good conversations. Better connections.','resources':'Resources — Ideas worth building on.','memories':'Memories — More than a meetup.','community':'Community — Your people. Your place.'}[kind])

# A small typographic ribbon supplies the brand palette without making a table.
c=rect(0,0,1200,12,VIOLET)+rect(400,0,400,12,GREEN)+rect(800,0,400,12,LAVENDER)
save('spectrum.svg',1200,12,c,'')

for mobile in (False,True):
    w,h=(720,730) if mobile else (1200,410)
    c=rect(0,0,w,h,NAVY,28)
    c+=contours(730,270,LAVENDER)
    c+=text('THE BEST PART OF A PLATFORM? ITS PEOPLE.',40,57,17,LAVENDER,500,0.5)
    c+=text('Make room',40,150,65,WHITE,600)
    c+=text('for others.',40,229,65,LAVENDER,600)
    c+=text('A question. A first talk. A helping hand.',43,283,23,WHITE,400)
    if mobile:
        c+=embed('ukuku.webp',210,325,300,315)
        c+=text('YOU BELONG HERE.',40,688,20,GREEN,500,1)
    else:
        c+=embed('ukuku.webp',826,43,320,340)
        c+=text('YOU BELONG HERE.',43,365,18,GREEN,500,1.5)
    save('welcome-mobile.svg' if mobile else 'welcome.svg',w,h,c,'Make room for others. A question. A first talk. A helping hand. You belong here.')
print('Rendered 9 SVG compositions.')
