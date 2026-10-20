from pathlib import Path
import os
from reportlab.pdfgen import canvas
root=Path(os.environ['BIRP_WORKSPACE'])
c=canvas.Canvas(str(root/'output/presentation/BIRP-Partner-Pitch-v1.0.pdf'),pagesize=(960,540))
c.setTitle('BIRP Partner Pitch v1.0');c.setAuthor('Michael Gee / BIRP')
for n in range(1,9):
 c.drawImage(str(root/f'.pitch-build/slide-{n}.png'),0,0,width=960,height=540)
 if n==8:c.linkURL('https://birp-home-canary.oolongee.chatgpt.site',(54,40,920,75),relative=0)
 c.showPage()
c.save()
