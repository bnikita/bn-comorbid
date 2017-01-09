import xml.etree.ElementTree as ET
import numpy as np
import nltk, string
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from bs4 import BeautifulSoup
from time import time

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import f1_score
from sklearn.grid_search import GridSearchCV


def words_extract(tree):
    # функция для объединение полей xml
    # и лингвистического препроцессинга

    root = tree.getroot()

    vacs = []
    stop_words = stopwords.words('russian')
    russian_stemmer = SnowballStemmer('russian')

    for vacancy in root:

        # совмещаем все поля, кроме отраслей и даты обновления
        vac = ""
        for child in vacancy.iter():
            if not child.tag in ('industries', 'industry', 'update-date'):
                vac = vac + " " + child.text

        text = BeautifulSoup(vac, "html.parser").get_text()

        # альтернативный/упрощенный метод
        # дающий, однако, близкий F-score
        # оставлен для нужд тестирования
        # tokens = text.lower().split()

        tokens = nltk.word_tokenize(text)
        tokens = [i for i in tokens if (i not in string.punctuation)]
        tokens = [i for i in tokens if (i not in stop_words)]
        tokens = [russian_stemmer.stem(i) for i in tokens]

        vacs.append(" ".join(tokens))

    return vacs


def label_extract(tree, inds):
    # функция загрузки отраслей и составления словаря

    root = tree.getroot()

    L = []

    for vacancy in root:

        L_vac = []
        for industry in vacancy.find('industries'):
            if industry.text in inds:
                L_vac.append(inds.index(industry.text))
            else:
                inds.append(industry.text)
                L_vac.append(inds.index(industry.text))

        L.append(L_vac)

    return L


def save_xml(tree, inds, T):
    # функция сохранения предсказаний в xml

    root = tree.getroot()

    vac = 0
    for vacancy in root:
        for child in list(vacancy):
            # для визуального сопоставления
            # if not child.tag in ('job-name'):
            vacancy.remove(child)

        industries = ET.SubElement(vacancy, 'industries')

        for ind in T[vac]:
            industry = ET.SubElement(industries, 'industry')
            industry.text = inds[ind]

        vac += 1

    tree.write('pred.xml')


train_tree = ET.parse('train.xml')
test_tree = ET.parse('test.xml')

W_train = words_extract(train_tree)
print 'Train items stored'

W_test = words_extract(test_tree)
print 'Test items stored'

save_xml(test_tree, inds_dict, Y_test)
print 'Output file is saved'
