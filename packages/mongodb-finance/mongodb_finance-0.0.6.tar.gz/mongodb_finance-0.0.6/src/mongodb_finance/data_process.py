import pymongo
import pandas as pd
from datetime import datetime

# 连接数据库
def connect_mongodb(host='127.0.0.1', port=27017):
    """
    连接mongodb服务器

    参数
    -------
    host: str
        服务器ip地址，默认是本地('127.0.0.1')
    port: int 
        端口号，默认是27017
    
    返回值
    -------
    pymongo.MongoClient

    示例
    -------
    client = mongodb_finance.connect_mongodb(host='127.0.0.1', port=27017)
    """

    mongo_uri = f'mongodb://{host}:{port}/'
    visitor = pymongo.MongoClient(mongo_uri)
    return visitor

# 从mongodb中读取数据库
def query_data(client, database, factors, stocks=None, start_time=None, end_time=None):
    """
    获取因子数据

    参数
    -------
    client: pymongo.MongoClient
        已连接mongodb对象
    databse: str 
        数据库名字
    factors: list
        因子名列表
    stocks: list
        公司名列表，默认是None，即读取所有公司
    start_time: str
        开始时间(>=)，默认是None，即不限制开始时间
    end_time: str
        结束时间(<=)，默认是None，即不限制结束时间
    
    返回值
    -------
    dict
        一个大字典，key对应factor名字，value对应dataframe

    示例
    -------
    client = mongodb_finance.connect_mongodb(host='10.16.7.69', port=27017)
    df_dict = mongodb_finance.query_data(client=client, database='stock_daily', factors=['open', 'close'], start_time='20100101', end_time='20150101')
    open = df_dict['open']
    close = df_dict['close']
    """

    if stocks is None:  # all stocks
        col_dict = {}
    else:
        col_dict = {stock: 1 for stock in stocks}
        col_dict['cal_date'] = 1
    col_dict['_id'] = 0
    if start_time is None and end_time is None:  # all time
        row_dict = {}
    elif start_time is not None and end_time is None:
        start_time = datetime.strptime(start_time, '%Y%m%d')
        row_dict = {'cal_date':{'$gte': start_time}}
    elif start_time is None and end_time is not None:
        end_time = datetime.strptime(end_time, '%Y%m%d')
        row_dict = {'cal_date':{'$lte': end_time}}
    elif start_time is not None and end_time is not None:
        start_time = datetime.strptime(start_time, '%Y%m%d')
        end_time = datetime.strptime(end_time, '%Y%m%d')
        row_dict = {'cal_date':{'$gte': start_time, '$lte': end_time}}
    db = client[database]
    df_dict = {}
    for factor in factors:
        cursor = db[factor].find(row_dict, col_dict)
        df_dict[factor] = pd.DataFrame(list(cursor))
    return df_dict
