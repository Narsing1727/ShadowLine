import zipfile
import xml.etree.ElementTree as ET

def extract_text(xml_content):
    root = ET.fromstring(xml_content)
    texts = []
    # a:t tags contain the text
    for elem in root.iter():
        if elem.tag.endswith('}t'):
            if elem.text:
                texts.append(elem.text)
    return ' '.join(texts)

try:
    with zipfile.ZipFile('UpStream_ShadowLine.pptx', 'r') as z:
        for i in range(1, 4):
            try:
                slide_xml = z.read(f'ppt/slides/slide{i}.xml').decode('utf-8')
                print(f"--- Slide {i} ---")
                print(extract_text(slide_xml))
            except KeyError:
                break
except Exception as e:
    print(e)
