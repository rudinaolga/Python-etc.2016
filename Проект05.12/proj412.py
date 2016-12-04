import urllib.request as ur
import re
import html

#статьи лежат в переменных
a = 'https://regnum.ru/news/innovatio/2211264.html'
b = 'http://www.newsler.ru/science/2016/11/29/planetologi-zametili-na-marse-zagadochnyij-labirint'
c = 'https://lenta.ru/news/2016/11/29/mars/'
d = 'https://rg.ru/2016/11/29/na-marse-obnaruzhen-labirint.html'

dictator = {}

#функция для создания 
def make_content_arr (mas):
    mas1 = re.sub('\.|\,|\—|\"|\«|\»|\xa0|\(|\)|/|\:', '', mas)
    mas1 = mas1.replace('\n', '')
    mas1 = mas1.replace('\r', '')
    mas1 = mas1.lower()
    arr = mas1.split(' ')
    mas1 = ''.join(arr)

    i = 0
    while i < len(arr):
            if arr[i] == '':
		
                    del arr[i]
            else:
                    i += 1
    return (arr)
#функция для создания словаря с частотностью слов
#поскольку в симметричной разности будут лишь уникальные слова, нет смысла создавать отдельный словарь: частотность уникального слова
#не изменится от присутствия там слов из других массивов
def make_freq (ddd, array):
    for j in array:
            if j in ddd:
                ddd[j] += 1
            else:
                ddd[j] = 1
    return ddd
#читаем статью а, парсим, создаем множество, забиваем в частотный словарь
page = ur.urlopen(a)
text = page.read().decode('utf-8')
res = re.search('REGNUM</b></span>(.+?)\n', text, flags=re.DOTALL)
if res != None:
    art = res.group(1)
    art1 = html.unescape(art)
    art2 = re.sub('</p><p>|</p>', ' ', art1)
    #итоговая статья без закорючек - art2
    array0 = make_content_arr (art2)
    mnoj1 = set(array0)
    dictator = make_freq (dictator, array0)
    
    
#читаем статью d, парсим, создаем множество, забиваем в частотный словарь
page2 = ur.urlopen(d)
text2 = page2.read().decode('utf-8')

res1 = re.search('articleBody">(.*?)<!--incut b-read-more_width-->', text2, flags=re.DOTALL)
if res1 != None:
    art3 = res1.group(1)
    art4 = html.unescape(art3)
    art5 = re.sub('</p>|<p>', ' ', art4)
    art6 = re.sub('<?a? href=.+?>|</a>|<img class.+?>|</?div.*?>|<!--incut b-read-more_large-->|<!--/?noindex-->|<h3.+?</h3>|<a.*-->', '', art5)
    #итоговая статья без закорючек - art6
    array1 = make_content_arr (art6)
    dictator = make_freq (dictator, array1)
    
    mnoj2 = set(array1)

#читаем статью c, парсим, создаем множество, забиваем в частотный словарь
page3 = ur.urlopen(c)
text3 = page3.read().decode('utf-8')
res2 = re.search('articleBody">(.*?)</div></div><section', text3)
if res2 != None:
    art7 = res2.group(1)
    art8 = re.sub('</?p>', ' ', art7)
    art9 = re.sub('</?a.*?>|</?div.*?>|<h2>.*?</h4>|<img.*?>|</?use.*?>|</?svg.*?>|{.+?}', '', art8)
    #итоговая статья без закорючек - art9
    array2 = make_content_arr(art9)
    dictator = make_freq (dictator, array2)
    mnoj3 = set(array2)

#читаем статью b, парсим, создаем множество, забиваем в частотный словарь
page4 = ur.urlopen(b)
text4 = page4.read().decode('utf-8')
res3 = re.search('<div class="materialIntrotext">(.*?)</div>', text4)
res4 = re.search('<div class="materialContent">(.*\n.*\n.*\n.*)', text4)
if res3 != None:
    art10 = res3.group(1)
    art11 = re.sub('</?p>', ' ', art10)
    
if res4 != None:
    art12 = res4.group(1)
    art13 = re.sub('</?p>', ' ', art12)
    art14 = re.sub('</?div.*?>', '', art13)
    art15 = art11 + art14 #итоговая статья без закорючек
    array3 = make_content_arr (art15)
    dictator = make_freq (dictator, array3)
    
    mnoj4 = set(array3)
#решаем задачу: пересечение множеств и симметрическая разность 
ex1 = mnoj1 & mnoj2 & mnoj3 & mnoj4
ex2 = mnoj1 ^ mnoj2 ^ mnoj3 ^ mnoj4

#функция для создания отсортированных по алфавиту массивов из множеств
def sorted_array_from(mnoj):
    array = list(mnoj)
    array.sort()
    return (array)
        


mas1 = sorted_array_from(ex1)
mas2 = sorted_array_from(ex2)
ex10 = []
def write_file(name, array):
    fw = open('mnojfreqarticles.txt', 'a')
    fw.write(name + '\n')
    for i in array:
        fw.write(i + '\n')
        
write_file('Пересечение множеств:', mas1)
write_file('Симметрическая разность множеств:', mas2)

        
#проверяем слова из симметрической разности на частотность, бОльшую единицы
for el in ex2:
    if el in dictator:
        if dictator[el] != 1:
            ex10.append(el)
        else:
            continue

ex10.sort()
write_file('Симметрическая разность множеств (freq > 1):', ex10)

     
