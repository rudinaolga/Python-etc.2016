import urllib.request as ur
import re
import time
import os
f = 'C:\\'

os.makedirs(f + 'kluch')
os.makedirs(f + 'kluch'+ '\\plain')
os.makedirs(f + 'kluch' + '\\mystemxml')
os.makedirs(f + 'kluch' + '\\mystemplain')
fw1 = open(f+'kluch\\'+'metadata.tsv', 'w', encoding='utf-8')
fw1.write('path\tauthor\tsex\tbirthday\theader\tcreated\tsphere\tgenre_fi\ttype\ttopic\tchronotop\tstyle\taudience_age\taudience_level\taudience_size\tsource\tpublication\tpublisher\tpubl_year\tmedium\tcountry\tregion\tlanguage\n')
fw1.close()
commonUrl = 'http://yaskluch.ru/?module=articles&action=view&id='

for i in range(93, 417):
    pageUrl = commonUrl + str(i)
    page = ur.urlopen(pageUrl)
    text = page.read().decode('utf-8')
    res = re.search('<h1>(.*?)</h1>.*?<span class=\'date_start\'>(.*?)</span>', text)
    regex = re.search('<span class=\'intro\'>(.+?)</span><span class=\'text\'>', text)
    if res != None:
        title = res.group(1)
        dataa = res.group(2)
    
    regs = re.search('rubrics=.+?&id=0\'\S(.*?)</a>', text)
    if regs != None:
        rubr = regs.group(1)
        
    else:
        rubr = 'None'
    if regex != None:
        article = regex.group(1)
        name = dataa[0:4]
        name2 = dataa[5:7]
        path = f + 'kluch\\plain\\'+name+'\\'+ name2 +'\\'+dataa+'.txt'
        
        row = path+'\tNoAuthor\t\t\t'+title+'\t'+dataa+'\tпублицистика\t\t\t'+rubr+'\t\tнейтральный\tн-возраст\tн-уровень\tобластная\t'+pageUrl+'\tЯсный ключ\t\t'+name+'\tгазета\tРоссия\tБелгородская область\tru\n'
        fw1 = open(f+'kluch\\'+'metadata.tsv', 'a', encoding='utf-8')

        fw1.write(row)
        fw1.close()
        if not os.path.exists(f + 'kluch'+ '\\plain\\' + name):
            os.makedirs(f + 'kluch'+ '\\plain\\' + name)
            
        if not os.path.exists(f + 'kluch'+ '\\plain\\' + name + '\\' +name2):
            os.makedirs(f + 'kluch'+ '\\plain\\' + name + '\\' +name2)
        fw = open(f + 'kluch' + '\\plain\\' +name + '\\' + name2 +'\\'+ dataa + '.txt', 'w')
        fw.write('@au Noname\n@ti ' + title +'\n@da ' + dataa + '\n@topic ' + rubr +'\n@url ' + pageUrl + '\n' + article)
        fw.close()

        if not os.path.exists(f + 'kluch'+ '\\mystemplain\\' + name):
            os.makedirs(f + 'kluch'+ '\\mystemplain\\' + name)
        if not os.path.exists(f + 'kluch'+ '\\mystemplain\\' + name + '\\' +name2):
            os.makedirs(f + 'kluch'+ '\\mystemplain\\' + name + '\\' +name2)

        if not os.path.exists(f + 'kluch'+ '\\mystemxml\\' + name):
            os.makedirs(f + 'kluch'+ '\\mystemxml\\' + name)    
        if not os.path.exists(f + 'kluch'+ '\\mystemxml\\' + name + '\\' +name2):
            os.makedirs(f + 'kluch'+ '\\mystemxml\\' + name + '\\' +name2)   
   
    time.sleep(2)
    




