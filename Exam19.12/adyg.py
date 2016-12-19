import re
import os
f = open('polit.html', 'r', encoding = 'utf-8')
file = f.read()
res = re.findall('<p>(.*?)</p>', file, flags = re.DOTALL)
text = ' '.join(res)
text = text.replace('/xad', '')
text = text.replace('.', '')
text = text.replace(',', '')
text = text.replace(':', '')

text = text.replace('«', '')
text = text.replace('»', '')
text = text.replace(' — ', ' ')
text = text.replace(' -', ' ')

arr = text.split(' ')
for el in arr:
    el = el.replace('/xad', '')

f2 = open('adyghe-unparsed-words.txt', 'r', encoding = 'utf-8')
file2 = f2.read()
f2.close()

arr2 = file2.split('\n')

mnojad = set(arr2)
mnojad2 = set(arr)
a = mnojad & mnojad2
f3 = open('wordlist.txt', 'w', encoding = 'utf-8') #файл с пересечениями множеств из html-текста и из файла

for am in a:
    if am == '':
        continue
    else:
        f3.write(am + '\n')

f3.close()

os.system(r"C:\Users\student\Desktop\mystem " + '-ni -e utf8 ' + r"C:\Users\student\Desktop\adyghe-unparsed-words.txt" + r" C:\Users\student\Desktop\adyghe-parsed-words.txt")

f4 = open('adyghe-parsed-words.txt', 'r', encoding = 'utf-8') #файл из майстема с грам характеристиками всего
reg = f4.read()
f4.close()
f5 = open('rus_nouns.txt', 'w', encoding = 'utf-8') #файл со словами, которые майстем называет s, ед им
mas = reg.split('\n')
d = {}
for el in mas:
    if '?' not in el:
        resv2 = re.search('^(\w.+)\{.+?=S.+?[^|]=им,ед(\||\}|,)', el)
        if resv2 != None:
            bi = resv2.group(1)
            if bi in d:
                continue
            else:
                d[bi] = 1

for word in d:
    f5.write(word + '\n')

f5.close()
os.system(r"C:\Users\student\Desktop\mystem " + '-n -e utf8 ' + r"C:\Users\student\Desktop\probbb.txt" + r" C:\Users\student\Desktop\wordslemmas.txt")
f6 = open('wordslemmas.txt', 'r', encoding = 'utf-8') #вспомогательный файл с майстемом найденных слов, только словоформы и леммы
lines = f6.read()
f6.close()
myst = re.findall('(.+?)\{(.+?)(\|.+?)?(\|.+?)?\}\\n', lines, flags = re.DOTALL)
f7 = open('sql.txt', 'a', encoding = 'utf-8') #собственно файл с инсертами
for el in myst:
    rep1 = el[0]
    rep2 = el[1]
    rep3 = el[2]
    rep4 = el[3]
    rep3 = rep3.replace('|', '')
    rep4 = rep4.replace('|', '')
    
    f7.write('INSERT INTO rus_words (wordform, lemma) VALUES ("' + rep1 + '", "' + rep2 +'");\n')
    if rep3 != '' :
        f7.write('INSERT INTO rus_words (wordform, lemma) VALUES ("' + rep1 + '", "' + rep3 +'");\n')
    if rep4 != '' :
        f7.write('INSERT INTO rus_words (wordform, lemma) VALUES ("' + rep1 + '", "' + rep4 +'");\n')
        
f7.close()
