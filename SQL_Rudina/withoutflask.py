import os
import re

def write_ms_file(fileaddress): #требует полного адреса файла
    fr = open(fileaddress, 'r', encoding = 'utf-8')
    fr.read()
    os.system(r"C:\mystem " + '-cd -e utf8 ' + fileaddress + ' C:\\output\\result.txt')
    fms = open('C:\\output\\result.txt', 'r', encoding = 'utf-8') #открываем созданный в майстеме файл
    strwrd = fms.read()
    mas = re.findall('(\W?)\W?(.+?)\{(.+?)\}(.*?)( (\d+?.*?\d+?.?|\d+?.*?)?|\\n)', strwrd, flags = re.DOTALL)
    return (mas)

def dicts_ind_dbs(arr):
    sqlfile = open('C:\\output\\sqlfile.txt', 'a', encoding = 'utf-8') #файл дл записи sql
    lems = {}
    n = 1
    m = 1
    for el in arr:
        if el[2] in lems:
            continue
        else:
            lems[el[2]] = n
            n += 1
        wfwf = el[1].lower() #индексы кортежей - словоформы и леммы, в словаре присваиваем номер лемме без повторений
        sqlfile.write('INSERT INTO tab1 (id, wf, lem) VALUES ("' + str(lems[el[2]]) + '", "' + wfwf + '", "' + el[2] +'");\n')
    wfr = {}
    for el in arr:     
        wfr[m] = el[1]
        rep1 = el[0]
        rep2 = el[3] #берем правую и левую пунктуацию помимо прочего и не исключаем повторения
        rep1 = rep1.replace('"', '«')#т.к. берем не словоформы, а вхождения; они же могут повторяться
        rep2 = rep2.replace('"', '»') #sql ругается на обычные кавычки
        sqlfile.write('INSERT INTO tab2 (id, left_punct, words, right_punct, id_lem) VALUES ("' + str(m) + '", "' + rep1 +'", "' + el[1] + '", "' + rep2 + '", "' + str(lems[el[2]]) +'");\n')
        m += 1
    sqlfile.close()

def main():
    full_filead = 'C:\\input\\juststo.txt'
    res_arr = write_ms_file(full_filead)
    dicts_ind_dbs(res_arr)
    
 
if __name__ == '__main__':
    main()
