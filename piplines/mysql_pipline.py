
import pymysql
from dbutils.pooled_db import PooledDB
from settings import MYSQL_CONFIG,logger


class MysqlPipeline:
    def __init__(self,db):
        MYSQL_CONFIG['db'] = db
        self.pool = PooledDB(pymysql, **MYSQL_CONFIG,
                        setsession=['SET AUTOCOMMIT = 1'])
        self.connector,self.cursor = self.connect()

    def connect(self):
        try:
            connector = self.pool.connection()
            cursor = connector.cursor()
            return connector,cursor
        except:
            logger.error('mysql connect failed')

    def select(self,sql):
        try:
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            return res
        except Exception as e:
            logger.error(f'mysql select error {e}')

    def insert(self,table,item):
        sql_insert = f"""insert into {table}({",".join(item.keys())}) values({",".join([f'"{value}"' for value in item.values()])});"""
        try:
            self.cursor.execute(sql_insert)
            self.connector.commit()
            logger.debug(f'{item} - insert success')
        except pymysql.err.IntegrityError:
            self.connector.rollback()
            logger.warning('repeat insert')
        except Exception as e:
            logger.error(f'mysql insert error - {e}')

    def close(self):
        self.cursor.close()
        self.connector.close()