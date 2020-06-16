import pymysql
from dbconfig import Dbconfig
from datetime import datetime
from datetime import timedelta

class DBModel :

    def DBConnect(self):
        dbstr = Dbconfig.connectionStr(self)
        conn =pymysql.connect(host=dbstr['host'], user=dbstr['user'], password=dbstr['password'], db=dbstr['database'], charset='utf8')
        return conn

    def InsertProduct(self,param):
        conn = DBModel().DBConnect()
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sqlstr = 'insert into HelloMarket(company, model, title, price, content) values(%s, %s, %s, %s, %s)'
        curs.execute(sqlstr, (param.company, param.model, param.title, param.price, param.content))
        conn.commit()
        conn.close()
        return 'InsertProduct_insertOK'


if __name__ == '__main__':
    conn = DBModel().DBConnect()
    conn.DBConnect()
    curs = conn.cursor(pymysql.cursors.DictCursor)
    
    curs.execute()