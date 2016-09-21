
import sqlite3
import json
from os import path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

ROOT = path.dirname(path.realpath(__file__))

def create_database():
    conn = sqlite3.connect(path.join(ROOT,'ckc00.sqlite'))
    conn.execute(''' CREATE TABLE ckc00 
        (id INTEGER NOT NULL PRIMARY KEY, \
        bbs_id TEXT,  \
        name TEXT NOT NULL, \
        sex TEXT NOT NULL, \
        city TEXT, \
        state TEXT, \
        class_type TEXT NOTE NULL, \
        class_id TEXT NOT NULL, \
        latitude REAL, \
        longitude REAL);''')

    # add entries
    with open('ckc00.json') as fin:
        ckc00 = json.load(fin)
    for a in ckc00:
        conn.execute('''INSERT INTO ckc00
            (id, bbs_id, name, sex, city, state, class_type, class_id, 
                    latitude, longitude)
            VALUES (?,?,?,?,?,?,?,?,?,?)''',
            (a['id'], a['88id'], a['name'],a['sex'], a['city'], 
             a['state'], a['class_type'], a['class_id'], 
             a['latitude'], a['longitude']))
    conn.commit()
    conn.close()

def do_name_query(name):
    basecmd = '''SELECT id, bbs_id, city, state, latitude, longitude 
                FROM ckc00 '''
    conn = sqlite3.connect(path.join(ROOT,'ckc00.sqlite'))
    c = conn.execute(basecmd+'WHERE name=?', (name,))
    results = c.fetchall()
    conn.close()
    str_rows = [','.join(map(str, row)) for row in results]
    return '\n'.join(str_rows)

def do_query(sex, class_type):
    ''' mimics csv output '''
    basecmd = '''SELECT id, bbs_id, city, state, latitude, longitude 
                FROM ckc00 '''

    conn = sqlite3.connect(path.join(ROOT,'ckc00.sqlite'))
    if sex=='all' and class_type=='all':
        c = conn.execute(basecmd)
    elif sex=='all' and class_type!='all':
        c = conn.execute(basecmd+'WHERE class_type=?',(class_type,))
    elif sex!='all' and class_type=='all':
        c = conn.execute(basecmd+'WHERE sex=?',(sex,))
    else:
        c = conn.execute(basecmd+'WHERE sex=? AND class_type=?',
                        (sex, class_type))

    results = c.fetchall()
    conn.close()
    str_rows = [','.join(map(str, row)) for row in results]
    return '\n'.join(str_rows)
    


