# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET

# Надо будет еще добавить пакетную обработку файлов
EHR_tree = ET.parse('10_2015.xml')
root = EHR_tree.getroot()

fout = open ("from_xml.txt", "w")
skipi = 1

for record in root:
    if skipi > 25: # Пропускаем первые 25 незначащих тегов
    
        for field in record.find('Zs0c15'): # В этом поле - диагноз
            # Хитрая обработка, учитывающая наличие html-тегов
            fout.write(ET.tostring(field, encoding="utf-8"))
            fout.write('\n')
        
            #Таким образом в файле исходные данные для извлечения кодов заболеваний        
        
    skipi += 1

fout.close()
