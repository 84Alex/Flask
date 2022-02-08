import pymysql


# function para conectar a la bd
def connect():
    return pymysql.connect(host='localhost', user='root', password='', db='flask')