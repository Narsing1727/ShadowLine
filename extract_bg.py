import zipfile
import re

with zipfile.ZipFile('UpStream_ShadowLine.pptx', 'r') as z:
    slide_xml = z.read('ppt/slides/slide1.xml').decode('utf-8')
    bg = re.findall(r'<p:bg>.*?</p:bg>', slide_xml, re.DOTALL)
    print("Background XML:", bg)
