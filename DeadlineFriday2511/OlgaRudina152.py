import json
from flask import Flask
from flask import url_for, render_template, request, redirect


app = Flask(__name__)

a = {}
b = {}
c = {}
d = {}
e = {}
aa = {}


@app.route('/')
def index():
    urls = {'Анкета': url_for('index'),
            'Все ответы': url_for('sonic'),
            'Статистика ответов': url_for('stats'),
            'Поиск': url_for('search'),}
    
    global a, b, c, d, e
    if request.args:
        
        vor = request.args['vor']
        tvo = request.args['tvo']
        bal = request.args['bal']
        zak = request.args['zak']
        disp = request.args['disp']
        if vor != '':
            a.setdefault('ВОРОТА', []).append(vor)
        if tvo != '':
            b.setdefault('ТВОРОГ', []).append(tvo)
        if bal != '':
            c.setdefault('БАЛОВАТЬ', []).append(bal)
        if zak != '':
            d.setdefault('ЗАКУПОРИТЬ', []).append(zak)
        if disp != '':
            e.setdefault('ДИСПАНСЕР', []).append(disp)
        
        
        
        
       
        global aa
        global aaa, bbb, ccc, ddd, eee
        aaa = json.dumps (a, sort_keys = True, indent = 4, ensure_ascii = False)
        bbb = json.dumps (b, sort_keys = True, indent = 4, ensure_ascii = False)
        ccc = json.dumps (c, sort_keys = True, indent = 4, ensure_ascii = False)
        ddd = json.dumps (d, sort_keys = True, indent = 4, ensure_ascii = False)
        eee = json.dumps (e, sort_keys = True, indent = 4, ensure_ascii = False)
        fa = open('vorota.json', 'w')
        fb = open('tvorog.json', 'w')
        fc = open('balovat.json', 'w')
        fd = open('zakuporit.json', 'w')
        fe = open('dispanser.json', 'w')
        fa.write(aaa)
        fb.write(bbb)
        fc.write(ccc)
        fd.write(ddd)
        fe.write(eee)
        fa.close()
        fb.close()
        fc.close()
        fd.close()
        fe.close()
        return render_template('anketa.html', urls = urls, tvo = tvo, vor = vor, bal = bal, zak = zak, disp = disp)
    return render_template('anketa.html', urls = urls)

@app.route('/stats')
def stats():
    urls = {'Анкета': url_for('index'),
            'Все ответы': url_for('sonic'),
            'Статистика ответов': url_for('stats'),
            'Поиск': url_for('search'),}
    
    global a, b, c, d, e
    global aa
    try:
        for i in a['ВОРОТА']:
            if i in aa:
                aa[i] += 1
                
            else:
                aa[i] = 1
        for j in b['ТВОРОГ']:
            if j in aa:
                aa[j] += 1
                
            else:
                aa[j] = 1
        for k in c['БАЛОВАТЬ']:
            if k in aa:
                aa[k] += 1
                
            else:
                aa[k] = 1
        for l in d['ЗАКУПОРИТЬ']:
            if l in aa:
                aa[l] += 1
                
            else:
                aa[l] = 1

        for m in e['ДИСПАНСЕР']:
            if m in aa:
                aa[m] += 1
                
            else:
                aa[m] = 1
    
    except:
        return redirect ('errorstat')
    return render_template ('statistics.html', votes = aa, urls = urls)

@app.route('/json')
def sonic():
    urls = {'Анкета': url_for('index'),
            'Все ответы': url_for('sonic'),
            'Статистика ответов': url_for('stats'),
            'Поиск': url_for('search'),}
    fila = open('vorota.json', 'r')
    linesa = fila.read()
    filb = open('tvorog.json', 'r')
    linesb = filb.read()
    filc = open('balovat.json', 'r')
    linesc = filc.read()
    fild = open('zakuporit.json', 'r')
    linesd = fild.read()
    file = open('dispanser.json', 'r')
    linese = file.read()
    
    
    return render_template ('xtmljson.html', ja = linesa, jb = linesb, jc = linesc, jd = linesd, je = linese, urls = urls)

@app.route('/search')
def search():
    urls = {'Анкета': url_for('index'),
            'Все ответы': url_for('sonic'),
            'Статистика ответов': url_for('stats'),
            'Поиск': url_for('search'),}
    global names
    if request.args:
        names = request.args['keys']
        return render_template ('results.html', keys = names, urls = urls )
    return render_template ('sesearch.html', urls = urls)

    

@app.route('/errorstat')
def errorstat():
     urls = {'Анкета': url_for('index'),
            'Все ответы': url_for('sonic'),
            'Статистика ответов': url_for('stats'),
            'Поиск': url_for('search'),}
     return render_template ('errorstat.html', urls = urls)
    
@app.route('/results')
def results():
    urls = {'Анкета': url_for('index'),
            'Все ответы': url_for('sonic'),
            'Статистика ответов': url_for('stats'),
            'Поиск': url_for('search'),}
    global names, aa
    if request.args:
        names = request.args['keys']
        #povt = request.args['povt']
        if names in aa:
            povt = aa[names]
        else:
            povt = 0
        return render_template('result.html', urls = urls, keys = names, povt = povt)
    return render_template('result.html', urls = urls)

if __name__ == '__main__':
    app.run(debug=True)
