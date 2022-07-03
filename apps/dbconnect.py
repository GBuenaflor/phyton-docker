import psycopg2
from psycopg2 import pool
import pandas as pd
import os


def getdblocation():

    db = psycopg2.connect(
        user="postgres",
        password="password",
        host="localhost",
        port=5432,
        database="hrdo_localdb_schemaonly_test2",
        # # # #    sslmode='require'

    )
    #DATABASE_URL = os.environ['DATABASE_URL']
    #db = psycopg2.connect(DATABASE_URL, sslmode='require')
    return db


def querydatafromdatabase(sql):
    #    print(sql)
    db = getdblocation()
    cur = db.cursor()
    cur.execute(sql)
    rows = pd.read_sql(sql, db)
    db.close()
    return rows


def securequerydatafromdatabase(sql, values, dfcolumns):
    # print(sql)
    # print(values)
    # print(dfcolumns)
    db = getdblocation()
    cur = db.cursor()
    cur.execute(sql, values)
    #print(cur.mogrify(sql, values))
    rows = pd.DataFrame(cur.fetchall(), columns=dfcolumns)
    db.close()
    return rows


def modifydatabase(sqlcommand, values):
    # print(sqlcommand)
    db = getdblocation()
    cursor = db.cursor()
    cursor.execute(sqlcommand, values)
    db.commit()
    db.close()


def modifydatabasereturnid(sqlcommand, values):
    # print(sqlcommand)
    db = getdblocation()
    cursor = db.cursor()
    cursor.execute(sqlcommand, values)
    key = cursor.fetchone()[0]
    db.commit()
    db.close()
    return key


def bulkmodifydatabase(sqlcommand, valuelist):
    # print(sqlcommand)
    db = getdblocation()
    cursor = db.cursor()
    cursor.executemany(sqlcommand, valuelist)
    db.commit()
    db.close()


def singularcommandupdatedatabase(sqlcommand):
    # print(sqlcommand)
    db = getdblocation()
    cursor = db.cursor()
    cursor.execute(sqlcommand)
    db.commit()
    db.close()
