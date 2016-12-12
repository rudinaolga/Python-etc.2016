import re
import json
from flask import Flask
from flask import url_for, render_template, request, redirect

app = Flask(__name__)

def open_files(name):
    f = open('udm_lexemes_'+name+'.txt', 'r', encoding = 'utf-8')
    lines = f.read()
    return lines


adj = open_files('ADJ')
imit = open_files('IMIT')
n = open_files('N')
d = {} #словарь, где ключи - удмуртские слова, значения - части речи и русские переводы
druskeys = {} #словарь, где ключи - русские переводы, значения - части речи и удмуртские слова
def res_texts(var):
    mas = re.findall('lex: (.+?)\\n.+?gramm: (.+?)\\n.+?trans_ru: (.+?)\\n', var, flags = re.DOTALL)
    return mas
dfor = {} #специальный словарь для перевода во фласке
resadj = res_texts(adj)
resimit = res_texts(imit)
resn = res_texts(n)
for i in resadj:
    for f in i:
        if i[2] == '':
            continue
        else:
            dfor[i[0]] = i[2]
            transladj = i[2]
            transladj = re.sub('\d\.|\)', ',', transladj)
            arradj = transladj.split(', ')
            
                
            d[i[0]] = (i[1], arradj) #беру из кортежа элементы (0 - удм слово, 1 - часть речи, 2 - перевод на русский)
            for j in arradj:
                if j == '':
                    del j
                else:
                    druskeys[j] = (i[0], i[1])
            
        
for i in resimit:
    for f in i:
        if i[2] == '':
            continue
        else:
            dfor[i[0]] = i[2]
            translimit = i[2]
            translimit = re.sub('\d\.|\)', ',', translimit)
            arrimit = translimit.split(', ')
            d[i[0]] = (i[1], arrimit) #беру из кортежа элементы (0 - удм слово, 1 - часть речи, 2 - перевод на русский)
            for j in arrimit:
                if j == '':
                    del j
                else:
                    druskeys[j] = (i[0], i[1])
            
        

for i in resn:
    for f in i:
        if i[2] == '':
            continue
        else:
            dfor[i[0]] = i[2]
            transln = i[2]
            transln = re.sub('\d\.|\)', ',', transln)
            arrn = transln.split(', ')
            d[i[0]] = (i[1], arrn) #беру из кортежа элементы (0 - удм слово, 1 - часть речи, 2 - перевод на русский)
            for j in arrn:
                if j == '':
                    del j
                else:
                    druskeys[j] = (i[0], i[1])


        
        
        
drusjs = json.dumps(druskeys, sort_keys = True, indent = 4, ensure_ascii = False)
djs = json.dumps(d, sort_keys = True, indent = 4, ensure_ascii = False)
f1 = open('dictionary.json', 'w', encoding = 'utf-8')
f1.write(djs)
f2 = open('russianudm.json', 'w', encoding = 'utf-8')
f2.write(drusjs)
f1.close()
f2.close()
@app.route('/')
def index():
    global names, dfor
    if request.args:
        names = request.args['keys']
        return render_template ('results.html', keys = names)
    return render_template ('search.html')

@app.route('/results')
def results():
    
    global names, dfor
    if request.args:
        names = request.args['keys']
        
        if names in dfor:
            povt = dfor[names]
        else:
            povt = 'Перевод отсутствует'
        return render_template('results.html', keys = names, povt = povt)
    return render_template('results.html')

if __name__ == '__main__':
    app.run()



