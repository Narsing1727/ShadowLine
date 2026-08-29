import zipfile
import re

try:
    with zipfile.ZipFile('UpStream_ShadowLine.pptx', 'r') as z:
        theme_xml = z.read('ppt/theme/theme1.xml').decode('utf-8')
        sys_clr = re.findall(r'<a:sysClr val="([^"]+)" lastClr="([^"]+)"', theme_xml)
        srgb = re.findall(r'<a:srgbClr val="([^"]+)"', theme_xml)
        print('SysColors:', sys_clr)
        print('SRGB:', srgb)
        
        fonts = re.findall(r'typeface="([^"]+)"', theme_xml)
        print('Fonts:', set(fonts))
except Exception as e:
    print("Error:", e)
