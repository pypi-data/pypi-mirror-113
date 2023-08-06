import os
import sys
import ujson
from clickhouse_driver import Client
from graph_op import CHGraph
from db_op import DBoperator
import psycopg2

'''

graph_dir = "./config/tcpflow_flow.cfg.json"

#graph = CHGraph(graph_dir, client)

'''


def load_config():
    print("服务所有配置开始加载")
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = os.path.split(curPath)
    sys.path.append(rootPath[0])
    sys.path.append(rootPath[0] + "/" + rootPath[1])

    clickhouse_config_dir = rootPath[0] + "/" + rootPath[1] + "/config/" + "graph_config.json"

    with open(clickhouse_config_dir, 'r') as f:
        clickhouse_config = ujson.load(f)

    clickhouse_ip = clickhouse_config["ip"]
    clickhouse_port = clickhouse_config["port"]
    clickhouse_user = clickhouse_config["user"]
    clickhouse_pwd = clickhouse_config["password"]

    db_ip = clickhouse_config["dbip"]
    db_port = clickhouse_config["dbport"]
    db_user = clickhouse_config["dbuser"]
    db_table = clickhouse_config["dbtable"]


    # host = '10.202.255.93', port = '9090', user = 'default', password = 'root'
    print(clickhouse_ip, clickhouse_port, clickhouse_user, clickhouse_pwd)
    # graphClient = Client(host=clickhouse_ip, port=clickhouse_port, user=clickhouse_user, password=clickhouse_pwd)
    clickhouse_connect = {}
    clickhouse_connect["ip"] = clickhouse_ip

    graphClient = Client(host=clickhouse_ip)
    # res = graphClient.execute('show databases')  # 显示所有的数据库
    # print("show databases:", res)
    graph = CHGraph(graphClient)
    url = 'postgresql://'+db_user+'@'+db_ip+':'+db_port+'/'+db_table+'?sslmode=disable'
    # conn = psycopg2.connect(url)
    db = DBoperator(url)
    print("服务所有配置加载结束")
    config_params = {
        "graph": graph,
        "db": db,
        "graphClient": graphClient,
        "clickhouse_connect": clickhouse_connect
    }
    # config_params = {
    #
    # }
    return config_params
