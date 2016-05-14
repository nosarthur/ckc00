
import sqlite3
import json
from os import path

ROOT = path.dirname(path.realpath(__file__))

def create_database():
    conn = sqlite3.connect(path.join(ROOT,'ckc00.sqlite'))
    conn.execute(''' CREATE TABLE ckc00 
        (id TEXT NOT NULL PRIMARY KEY,  \
        name TEXT NOT NULL, \
        sex TEXT NOT NULL, \
        city TEXT NOT NULL, \
        state TEXT NOT NULL, \
        class TEXT NOT NULL, \
        classId TEXT NOT NULL, \
        latitude REAL NOT NULL, \
        longitude REAL NOT NULL);''')

    # add entries
    with open('ckc00.json') as fin:
        ckc00 = json.load(fin)
    for a in ckc00:
        conn.execute('''INSERT INTO ckc00
            (id, name, sex, city, state, class, classId, 
                    latitude, longitude)
            VALUES (?,?,?,?,?,?,?,?,?)''',
            (a['88id'], a['name'],a['sex'], a['city'], 
             a['state'], a['class'], a['classId'], 
             a['latitude'], a['longitude']))
    conn.commit()
    conn.close()

def do_name_query(name):
    basecmd = '''SELECT id, city, state, latitude, longitude 
                FROM ckc00 '''
    conn = sqlite3.connect(path.join(ROOT,'ckc00.sqlite'))
    c = conn.execute(basecmd+'WHERE name=?', (name,))
    results = c.fetchall()
    conn.close()
    str_rows = [','.join(map(str, row)) for row in results]
    return '\n'.join(str_rows)

def do_query(sex, clss):
    ''' mimics csv output '''
    basecmd = '''SELECT id, city, state, latitude, longitude 
                FROM ckc00 '''

    conn = sqlite3.connect(path.join(ROOT,'ckc00.sqlite'))
    if sex=='all' and clss=='all':
        c = conn.execute(basecmd)
    elif sex=='all' and clss!='all':
        c = conn.execute(basecmd+'WHERE class=?',(clss,))
    elif sex!='all' and clss=='all':
        c = conn.execute(basecmd+'WHERE sex=?',(sex,))
    else:
        c = conn.execute(basecmd+'WHERE sex=? AND class=?',
                        (sex, clss))

    results = c.fetchall()
    conn.close()
    str_rows = [','.join(map(str, row)) for row in results]
    return '\n'.join(str_rows)
    


