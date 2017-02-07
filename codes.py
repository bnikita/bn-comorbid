# -*- coding: utf-8 -*-
from lxml import etree
import os, sys
import glob
import pandas as pd

folder = sys.argv[1]
output = sys.argv[2]
vocab_file = sys.argv[3]

diagnoses = pd.read_csv(vocab_file, sep=';', names  = ['code', 'variants'], encoding="cp1251")
diagnoses.variants = diagnoses.variants.map(lambda x: [s.strip() for s in x.split("|")])
 
cases = []
# find all .xml files and iterate them
parser = etree.XMLParser(ns_clean=True, encoding='cp1251')
for case_file_name in glob.glob(folder + r"/Прием кардиолога*.xml"):
    with open(case_file_name, 'r', encoding="cp1251") as case_file:
        tree = etree.parse(case_file, parser)
        root = tree.getroot()
        
        for case in root.findall(r'OXy'):
            ID = case.find('Zs0c1').text
            diag_text = etree.tostring(case.find('Zs0c15'), encoding='cp1251').decode('cp1251')
            
            if diag_text == '<Zs0c15>-</Zs0c15>':
                continue
            
            diag_codes = []
            for row in diagnoses.itertuples(index=False):
                for v in row.variants:
                    if v in diag_text:
                        diag_codes.append(row.code)
                        break
                    
            codes = "|".join(diag_codes)
            cases.append((ID, codes if codes else None))
            
    dd = pd.DataFrame(cases)
    dd.columns = ["case", "codes"]

    dd.to_csv(output)