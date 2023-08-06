import pandas as pd
from gtls import gtls
from sqlalchemy import create_engine
from sqlalchemy import types
import pymysql
import psycopg2


def import_data(filename,filetype='csv', isFillNaN=False, fillMethod=None, header_number=None, db_type='pg', db_ip='localhost', db_port='5432', db_username='postgres', db_userpasswd='postgres',db_name='postgres', db_tbname=None,db_tbname_exists='replace', db_tbname_columnname_list=None, rid=None):
    """A tool for  load csv/excel file data into postgresql/mysql.
    """
    DB_TYPE_PREFFIX = {'pg': 'postgresql+psycopg2', 'mysql': 'mysql+pymysql'}
    if filetype.upper() == "CSV":
        dataframe =  pd.read_csv(filename, header=header_number, dtype=str).dropna(how='all',inplace=False,axis='index')
    elif filetype.upper() == "EXCEL":
        dataframe =  pd.read_excel(filename, header=header_number, dtype=str).dropna(how='all',inplace=False,axis='index')
    if isFillNaN:
        if fillMethod == 'ffill':
            dataframe.fillna(method='ffill', inplace=True,axis='index')
        elif fillMethod == 'bfill':
            dataframe.fillna(method='bfill', inplace=True, axis='index')
        else:
            gtls.logUtils(level='ERROR', Msg="not have this method")

    if fillMethod is None:
        dataframe.fillna(value='', inplace=True)

    if db_tbname_columnname_list:
        dataframe.columns = db_tbname_columnname_list

    if rid:
        dataframe['rid'] = rid
    db_conn = create_engine('{}://{}:{}@{}:{}/{}'.format(DB_TYPE_PREFFIX[db_type],db_username, db_userpasswd,db_ip,db_port,db_name), echo=False, client_encoding='utf8')
    dataframe.to_sql(db_tbname, db_conn,if_exists=db_tbname_exists,index=False,method='multi')
