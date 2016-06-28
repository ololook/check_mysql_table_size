#!/usr/bin/env python
#coding=utf-8
import time
from prettytable import PrettyTable
from optparse import OptionParser
import sys
import os
import MySQLdb
import MySQLdb.cursors
def get_cli_options():
    parser = OptionParser(usage="usage: python %prog [options]",
                          description="""This script prints some basic table  about the size of the table and their indexes.""")

    parser.add_option("-H", "--host",
                      dest="host",
                      default="localhost",
                      metavar="HOST",
                      help="mysql host")
    parser.add_option("-p", "--port",
                      dest="port",
                      default=3306,
                      metavar="PORT",
                      help="mysql port")
    (options, args) = parser.parse_args()

    return options

def get_client(host, port):

    try:
      conn = MySQLdb.connect(host=host,port=int(port),user='username',
                             passwd='passwd', charset='utf8' )
    except  MySQLdb.Error,e:
      print "Error %d:%s"%(e.args[0],e.args[1])
      exit(1)
    return conn

def main() :
    options = get_cli_options()
    cursor=get_client(options.host,options.port).cursor()
    table = PrettyTable()
    #cursor=conn.cursor() 
    sql = """SELECT
               TABLE_SCHEMA,
               table_name AS "Table",
               TABLE_ROWS,
               AVG_ROW_LENGTH,
               round((data_length / 1024 / 1024), 0 ) "Data (MiB)" ,
               round((index_length / 1024 / 1024), 0 ) "Index (MiB)"
               FROM information_schema.TABLES  where TABLE_SCHEMA not in ("information_schema","performance_schema","mysql")
               and DATA_LENGTH is not  null and INDEX_LENGTH is not null   
               ORDER BY TABLE_SCHEMA,data_length DESC;"""
    try :
          cursor.execute(sql)
          table.field_names=[col[0] for col in cursor.description]
          for column in table.field_names:
              table.align[column]='l'
          for row in cursor.fetchall():
              table.add_row(row)
          print table
    
    except KeyboardInterrupt :
          print "exit .."
          sys.exit()
  
    cursor.close()
if __name__ == '__main__':
   main()
