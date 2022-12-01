import json
from xml.etree.ElementTree import fromstring
from xmljson import badgerfish as bf

a = open('DFD.xml', encoding='UTF-8').read()
bf.dict = dict
res = bf.data(fromstring(a))

list_of_elems = res['mxGraphModel']['root']['mxCell']
for elem in list_of_elems:
    if elem.get('@style'):
        temp_style = elem['@style'].split(";")
        for i, style in enumerate(temp_style):
            temp = style.split("=")
            if len(temp) == 2:
                temp_style[i] = {temp[0]: temp[1]}
        elem['@style'] = temp_style
print(list_of_elems)
with open('data.json', 'w') as outfile:
    json.dump(list_of_elems, outfile)
