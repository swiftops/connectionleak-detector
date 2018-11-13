from pymongo import MongoClient
from com.swiftops.connleak import ConnectionLeakCatcher as ConLeak
import configparser

config = configparser.ConfigParser()
config.read("com/swiftops/connleak/connleak.ini")


def _get_db_collection():
    """ This api read db details from ini file and connect to mongo db.
        :return mongo collection db collection.
    """

    error_data = {}
    try:
        db_ip = config.get("db_properties", "DB_IP")
        db_port = int(config.get("db_properties", "DB_PORT"), 10)
        db_user = config.get("db_properties", "DB_USERNAME")
        db_name = config.get("db_properties", "DB_NAME")
        db_pwd = config.get("db_properties", "DB_PASSWORD")
    except Exception as e:
        error_data["status_code"] = 404
        error_data["error_msg"] = "exception occurred while reading config file. Exception is " + e.__str__()
        return ConLeak.build_error_response(error_data)

    client = MongoClient(host=db_ip, port=db_port)
    mong_perf_db = client[db_name]
    print(mong_perf_db)
    mong_perf_db.authenticate(db_user, db_pwd)
    mong_perf_col = mong_perf_db.connleak_nightly_build
    return mong_perf_col


def _parse_connleak_data(conn_data):
    """ Parse connection leak raw data in  tabular format
     :return connleak data in jason format
    """
    jsondata = {}
    list_files = []
    conn_leaks = ''.join(chr(x) for x in conn_data)
    if 'JAVA :' in conn_leaks:
        total_number = conn_leaks[conn_leaks.find('Total ') + 6: conn_leaks.find(' connection')]
        conn_leaks = conn_leaks[conn_leaks.find('JAVA :'): conn_leaks.find(' Exception')]
        conn_leaks = conn_leaks.replace('\\t', '')
        conn_leaks = conn_leaks.split('JAVA :')
        conn_leaks.remove(conn_leaks[0])
        num = 1
        str_connleak = ''
        jsondata["tabulardata"] = [["File Name"]]
        jsondata["total"] = total_number
        for leak in conn_leaks:
            leak_list = [str(num) + '. ' + leak]
            list_files.append(leak_list)
            num += 1
        jsondata["tabulardata"].append(list_files)
        print(jsondata)
    return jsondata


def put_nightlybuild_data(conn_data, rel_no, build_no):
    error_data = {}
    """ This api parse captured connection leak data and insert data in mongo db
    """
    try:
        jsondata = _parse_connleak_data(conn_data)
        jsondata["Release No"] = rel_no
        jsondata["Build No"] = build_no
        mong_perf_coll = _get_db_collection()
        response=jsondata
        mong_perf_coll.insert_one(jsondata)
        return ConLeak.get_success_response(str(response))

    except Exception as ex:
        error_data["status_code"] = 404
        error_data["error_msg"] = "exception occurred while inserting document to collection" + ex.__str__()
        return ConLeak.build_error_response(error_data)

