"""Build the BIRP partner-discussion brief. Run from any directory with ReportLab installed."""
from pathlib import Path
import math, sys, shutil
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=Path(sys.argv[1]) if len(sys.argv)>1 else HERE/'BIRP-Invention-Brief-v1.0.pdf'
OUT.parent.mkdir(parents=True,exist_ok=True)
FONTDIR=Path('/usr/share/fonts/truetype/dejavu')
if (FONTDIR/'DejaVuSans.ttf').exists():
    for name,file in [('Body','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf'),('Serif','DejaVuSerif.ttf')]:
        pdfmetrics.registerFont(TTFont(name,str(FONTDIR/file)))
    pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Body',boldItalic='Bold')
else:
    for name,base in [('Body','Helvetica'),('Bold','Helvetica-Bold'),('Serif','Times-Roman')]:
        pdfmetrics.registerFont(pdfmetrics.Font(name,base,'WinAnsiEncoding'))
INK=HexColor('#173F39');MUTED=HexColor('#5F7067');GOLD=HexColor('#DDB345');PALE=HexColor('#F2F4EC');LINE=HexColor('#DCE3D7')
W,H=612,792;M=48;CW=516
c=canvas.Canvas(str(OUT),pagesize=(W,H),pageCompression=1)
c.setTitle('BIRP - The Home Canary | Invention Brief v1.0')
c.setAuthor('Prepared for Michael Gee')
c.setSubject('Recreated product concept and partner-discussion brief')

def para(text,x,y,w=CW,size=10,leading=None,color=INK,font='Body'):
    st=ParagraphStyle('p',fontName=font,fontSize=size,leading=leading or size*1.45,textColor=color,spaceAfter=0)
    p=Paragraph(text,st);pw,ph=p.wrap(w,1000)
    assert y-ph>=48,('Text below content area',text[:100],y,ph)
    p.drawOn(c,x,y-ph)
    return y-ph

def line(x,y,w=CW,color=LINE):
    c.setStrokeColor(color);c.setLineWidth(.65);c.line(x,y,x+w,y)

def header(page,kicker):
    c.setFillColor(white);c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(INK);c.setFont('Bold',11);c.drawString(M,750,'BIRP')
    c.setFont('Body',8);c.setFillColor(MUTED);c.drawString(87,750,'THE HOME CANARY')
    c.setFont('Body',7.5);c.drawRightString(W-M,750,kicker)
    line(M,735)
    c.setFillColor(MUTED);c.setFont('Body',7)
    c.drawString(M,30,'BIRP | Invention brief 1.0 | October 20, 2026')
    c.drawRightString(W-M,30,f'{page} / 4')

def title(text,y=702,size=25):
    return para(text,M,y,size=size,leading=size*1.18,font='Bold')

def box(x,y,w,h,fill=PALE):
    c.setFillColor(fill);c.roundRect(x,y,w,h,10,fill=1,stroke=0)

def label(text,x,y,color=MUTED):
    c.setFillColor(color);c.setFont('Bold',7.7);c.drawString(x,y,text)

def link(text,url,x,y,size=8.5):
    c.setFont('Body',size);c.setFillColor(INK);c.drawString(x,y,text)
    tw=pdfmetrics.stringWidth(text,'Body',size)
    c.linkURL(url,(x,y-2,x+tw,y+size+2),relative=0,thickness=0)
    c.setStrokeColor(LINE);c.line(x,y-3,x+tw,y-3)

# 1 / The concept
header(1,'PRODUCT CONCEPT / PARTNER DISCUSSION')
label('INVENTION BRIEF / RECREATED EDITION',M,711)
label('PREPARED FOR MICHAEL GEE',M,696)
para('Room conditions,<br/>made visible.',M,684,w=345,size=30,leading=36,font='Bold')
c.drawImage(str(ROOT/'website/assets/birp-original-logo.jpg'),416,585,width=148,height=148,preserveAspectRatio=True,mask='auto')
para('BIRP is a proposed wall-mounted environmental monitor with a round display and a physical bird that travels around its perimeter. Better conditions place the bird toward the top; worsening conditions move it toward the bottom. A light halo and readable measurements explain the signal.',M,584,size=10.5)
box(M,478,CW,31)
label('CURRENT STAGE: DOCUMENTED CONCEPT + BROWSER DEMONSTRATION',M+14,490,INK)
features=[
('01 / THE SIGNATURE INTERFACE','A physical perimeter bird makes the room-condition signal visible at a glance. The founder specified a 5-inch round display; final enclosure dimensions and the motion mechanism remain open.'),
('02 / STANDALONE BY DESIGN','Core room sensing and local feedback are intended to work without an app or subscription, after required sensor startup. The display provides the reason for a state change.'),
('03 / OPTIONAL CONNECTED SERVICES','The broader vision adds app history, remote monitoring, smart-home integration, video intercom, and multiple room units with a master-unit role. These features are not implemented.')]
y=443
for heading,body in features:
    label(heading,M,y,INK);para(body,M,y-13,size=9.7,leading=14.1);y-=87
box(M,77,CW,96)
label('COLLABORATION GOAL',M+16,153,INK)
para('Make the interaction understandable, review the design with suitable engineering and industrial-design partners, and define an achievable first physical proof. The initial pitch focuses on home-room air awareness; customer demand is still to be tested.',M+16,140,w=CW-32,size=10,leading=14.5)
c.showPage()

# 2 / The interaction
header(2,'INTERACTION AND PROPOSED CONTROL FLOW')
title('How the room becomes a signal.')
para('The bird\'s location around the display is the primary indicator. Body tilt is a separate possible gesture; it must not replace or obscure perimeter position.',M,654,size=10.2)

def bird(cx,cy):
    c.setFillColor(GOLD);c.ellipse(cx-14,cy-9,cx+12,cy+9,fill=1,stroke=0)
    c.circle(cx+9,cy+8,7,fill=1,stroke=0)
    p=c.beginPath();p.moveTo(cx-12,cy+2);p.lineTo(cx-25,cy-2);p.lineTo(cx-11,cy-7);p.close();c.drawPath(p,fill=1,stroke=0)
    c.setFillColor(INK);c.circle(cx+11,cy+10,1.2,fill=1,stroke=0)
    c.setStrokeColor(GOLD);c.setLineWidth(1);c.line(cx-2,cy-8,cx-2,cy-14);c.line(cx+5,cy-8,cx+5,cy-14)

cy=474
for cx,angle,color,heading,sub in [(126,0,HexColor('#7CAC9B'),'TOP','Better conditions'),(306,90,HexColor('#D8B353'),'SIDE','Attention preset'),(486,180,HexColor('#CE7D68'),'BOTTOM','Worse conditions')]:
    c.setFillColor(PALE);c.circle(cx,cy,58,fill=1,stroke=0)
    c.setStrokeColor(color);c.setLineWidth(4);c.circle(cx,cy,58,fill=0,stroke=1)
    c.setFillColor(MUTED);c.setFont('Body',7);c.drawCentredString(cx,cy+4,'ROOM STATUS');c.drawCentredString(cx,cy-10,'CAUSE + READINGS')
    a=math.radians(angle);bird(cx+math.sin(a)*61,cy+math.cos(a)*61)
    c.setFillColor(INK);c.setFont('Bold',8);c.drawCentredString(cx,365,heading)
    c.setFont('Body',8);c.setFillColor(MUTED);c.drawCentredString(cx,350,sub)
para('Illustrative positions only. The founder specified top/bottom meaning; the side position is a prototype preset. No measured thresholds are assigned to these drawings.',M,327,size=8.7,color=MUTED)
box(M,220,CW,76)
label('WHEN A READING IS MISSING',M+14,278,INK)
para('Show an explicit unknown status and a violet halo. Retain the last referenced bird position where safe, clearly identified as historical. Missing data must never produce a reassuring all-clear signal.',M+14,267,w=CW-28,size=9.2,leading=13)
label('PROPOSED FIRST-BENCH SIGNAL FLOW',M,211,INK)
for x,head,body in [(48,'MEASURE','CO2 / PM2.5<br/>Temperature / humidity'),(232,'INTERPRET','Validate freshness<br/>Classify channels separately'),(416,'EXPRESS','Perimeter bird<br/>Halo + cause on display')]:
    box(x,126,148,67)
    para(head,x+12,181,w=124,size=8.5,font='Bold')
    para(body,x+12,165,w=124,size=8.2,leading=12)
for x in [202,386]:
    c.setStrokeColor(INK);c.setLineWidth(1);c.line(x,158,x+23,158);c.line(x+23,158,x+18,162);c.line(x+23,158,x+18,154)
para('Sensor-specific readiness, classification policy, position referencing, physical travel limits, and fault behavior must be selected and tested before hardware performance can be claimed.',M,106,size=8.6,color=MUTED)
c.showPage()

# 3 / Visual reference and scope
header(3,'DESIGN REFERENCE AND PRODUCT SCOPE')
title('The device, in context.')
para('The original exploded illustration records the visual direction and optional modules. It is concept art: component labels, dimensions, fit, and internal layer details are not validated engineering specifications.',M,660,size=9.4,leading=13.4)
c.drawImage(str(ROOT/'website/assets/birp-exploded-concept.jpg'),M,285,width=CW,height=344,preserveAspectRatio=True,mask='auto')
para('Original project artwork supplied by the founder. The perimeter-motion requirement in the written product vision remains authoritative where the illustration is ambiguous.',M,272,size=8,color=MUTED,leading=11)
style=ParagraphStyle('cell',fontName='Body',fontSize=8.4,leading=11.8,textColor=INK)
def cell(s):return Paragraph(s,style)
rows=[['AREA','PROPOSED FIRST EXPERIMENT','BROADER INTENDED PRODUCT'],
['Display and bird','Round display, perimeter bird, halo, and cause-aware feedback.','5-inch display target; final enclosure and mechanism remain unselected.'],
['Sensing','CO2, PM2.5, temperature, and humidity.','Final sensor suite and product policy remain open.'],
['Connectivity','Core sensing and local output independent of app setup.','Optional app/services, smart-home integration, video intercom, and multi-room/master-unit roles.']]
t=Table([[cell(x) for x in row] for row in rows],colWidths=[95,195,226])
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LINEBELOW',(0,0),(-1,-1),.5,LINE)]))
tw,th=t.wrap(CW,300);assert 239-th>=54;t.drawOn(c,M,239-th)
c.showPage()

# 4 / The next practical proof
header(4,'EVIDENCE, COLLABORATION AND NEXT STEPS')
title('The path to first physical proof.')
steps=[
('1','Test the need and the interaction.','Complete the concept packet, then ask prospective users to explain the bird signal and the problem they would use it to solve. Record actual feedback for one initial audience.'),
('2','Review a buildable architecture.','With suitable resources or a partner, review display and sensor candidates, full orbital travel, gravity loading, position reference, power, heat, and noise. The same-hardware goal needs a separate feasibility review.'),
('3','Demonstrate the complete loop.','Show sensor readings, independent channel classification, cause text, halo, perimeter movement, missing-reading status, and qualified recovery. Record the build configuration and measured results.'),
('4','Choose the product-development path.','Use the evidence to assess partner-led development, a licensing discussion, or another resource-appropriate prototype step. Camera/audio, app services, and multi-room roles require further architecture work.')]
y=649
for num,head,body in steps:
    c.setFillColor(GOLD);c.circle(59,y-8,11,fill=1,stroke=0)
    c.setFillColor(INK);c.setFont('Bold',9);c.drawCentredString(59,y-11,num)
    para(head,81,y,w=483,size=10.3,font='Bold',leading=14)
    end=para(body,81,y-21,w=483,size=9.3,leading=13.4)
    y=end-24
box(M,248,CW,66)
label('WHAT A PARTNER CAN HELP EVALUATE',M+14,296,INK)
para('Mechanical feasibility, sensor integration, industrial design, user understanding, and a costed prototype plan. No purchase, funding commitment, production price, or partnership is represented by this brief.',M+14,284,w=CW-28,size=9.2,leading=13.2)
label('SOURCE MATERIAL AND CURRENT PROJECT',M,222,INK)
link('Original design conversation - supplied by the founder','https://chatgpt.com/share/6ad73285-01e0-83ea-b09e-83f61921a494?ogimg=plain',M,202)
link('Minimal founder plan - supplied by the founder','https://chatgpt.com/share/6ad73293-6efc-83e9-b179-55be44093599?ogimg=plain',M,183)
link('Current product vision','https://github.com/GEEKProtocol0110/birp-home-canary/blob/main/docs/PRODUCT_VISION.md',M,164)
link('Control draft 0.2','https://github.com/GEEKProtocol0110/birp-home-canary/blob/main/docs/control-spec-v0.2.md',M+260,164)
link('BIRP website','https://birp-home-canary.oolongee.chatgpt.site',M,145)
link('GitHub repository','https://github.com/GEEKProtocol0110/birp-home-canary',M+124,145)
line(M,127)
para('This is a newly recreated brief, not the missing original PDF. Current evidence consists of project documents, two original visual references, and a browser demonstration. A physical device, customer demand, manufacturing cost, and operating performance have not been validated. Smoke/CO integration remains outside the proposed bench scope.',M,113,size=8.2,leading=11.6,color=MUTED)
c.save()
print(OUT)
