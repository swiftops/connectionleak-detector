import configparser
import json
import subprocess
import re

config = configparser.ConfigParser()
config.read("com/swiftops/connleak/connleak.ini")


def find_conn_leaks():
    """
       This api will run jar file to find database connection leak in given repository.
       :return: database connection-leak list with filename and api.
       :limitation: if any api in repository returning database resultset it raise false alarm for it. add this api in
       ignore list only if resultset is closed in calling api.
       :Note: in ignore list same classs api are seprated using #. fing in example.
    """
    error_data = {}
    try:
        pattern_file_name = config.get("FILENAME", "pattern_file")
        ignore_file_list = config.get("FILENAME", "ignore_list_file")
    except Exception as e:
        error_data["status_code"] = 404
        error_data["error_msg"] = "exception occurred while reading config file. Exception is " + e.__str__()
        return build_error_response(error_data)
    try:
        connleaks = subprocess.Popen(['java','-jar', 'jars/ConnectionLeakCatcher.jar',ignore_file_list,pattern_file_name],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = connleaks.stdout.read()
        exception_str = ''.join(chr(x) for x in output)
        java_error = connleaks.stderr.read()
        err_str = ''.join(chr(x) for x in java_error)
        if 'JAVA :' in exception_str:
            exceptions = exception_str.split('\n')
            exceptions.remove(exceptions[0])
            err_str1 = re.findall(r"Total [0-9]+ connection leak found in current run",err_str)
            exceptions.insert(0, err_str1[0])
            return get_success_response(exceptions)
        else:
            return get_success_response("No connection-leak found in any API")
    except Exception as ex:
        error_data["status_code"] = 404
        error_data["error_msg"] = "exception occurred while running ConnectionLeakCatcher jar file. Exception is " + ex.__str__()
        return build_error_response(error_data)


def get_success_response(data):
    """
    this api forms response for success
    :return: success response in jason format
    """
    return_data={}
    return_data["success"] = "true"
    return_data["conn_leak"] = data
    return_data["error"] = {}
    return json.dumps(return_data)


def build_error_response(data):
    """
        This api forms response for failure
        :return: failure response in jason format
    """
    return_data = {}
    return_data["success"] = "false"
    return_data["data"] = {}
    return_data["error"] = data
    return json.dumps(return_data)

