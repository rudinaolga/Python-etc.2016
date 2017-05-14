import re
import os
from flask import Flask
from flask import url_for, render_template, request, redirect

app = Flask(__name__)

def write_ms_file(inputname, text):
    fw = open(inputname + 'ohnems.txt', 'w', encoding = 'utf-8')
    fw.write(text)
    fw.close()
    fr = open(inputname + 'ohnems.txt', 'r', encoding = 'utf-8')
    fr.read()
    os.system(r"C:\mystem " + '-cd -e utf8 ' + 'C:\\' + inputname + 'ohnems.txt C:\\' + inputname + 'parsed.txt')
    fms = open('C:\\' + inputname + 'parsed.txt', 'r', encoding = 'utf-8')
    strwrd = fms.read()
    mas = re.findall('(\W?)\W?(.+?)\{(.+?)\}(.*?)( (\d+?.*?\d+?.?|\d+?.*?)?|\\n)', strwrd, flags = re.DOTALL)
    return (mas)

def dicts_ind_dbs(arr, filename):
    sqlfile = open('C:\\output\\' + filename + '.txt', 'a', encoding = 'utf-8')
    wfr = {}
    lems = {}
    n = 1
    m = 1
    for el in arr:
        if el[2] in lems:
            continue
        else:
            lems[el[2]] = n
            n += 1
        wfwf = el[1].lower() 
        sqlfile.write('INSERT INTO tab1 (id, wf, lem) VALUES ("' + str(lems[el[2]]) + '", "' + wfwf + '", "' + el[2] +'");\n')
    
    for el in arr:     
        wfr[m] = el[1]
        rep1 = el[0]
        rep2 = el[3]
        rep1 = rep1.replace('"', '«')
        rep2 = rep2.replace('"', '»')
        sqlfile.write('INSERT INTO tab2 (id, left_punct, words, right_punct, id_lem) VALUES ("' + str(m) + '", "' + rep1 +'", "' + el[1] + '", "' + rep2 + '", "' + str(lems[el[2]]) +'");\n')
        m += 1
    sqlfile.close()
        
@app.route('/')
def index():
    global name
    if request.args:
        name = request.args['filename']
        text = request.args['keys']
        arr = write_ms_file(name, text)
        dicts_ind_bds(arr, name)
        return render_template ('vydacha.html', keys = text, filename = name )
    return render_template ('zapros.html')

@app.route('/results')
def results():
    return render_template('vydacha.html')

if __name__ == '__main__':
    app.run()
