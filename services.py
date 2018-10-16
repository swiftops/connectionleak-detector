from flask import Flask, request
from com.swiftops.connleak import ConnectionLeakCatcher as ConLeak
from com.swiftops.connleak import Connleak_Mongo_Connector as ConMong
import connexion

app = Flask(__name__)
app = connexion.App(__name__)
#app.add_api('swagger.yaml')

@app.route('/api/connectionleak/v1/findConnectionLeak', methods=['POST'])
def find_conn_leaks():
    """
           This api will run jar file to find database connection leak in given repository.
           :return: database connection-leak list with filename and api.
           :limitation: if any api in repository retuning database resultset it raise false alarm for it. add this api in
           ignore list only if resultset is closed in calling api.
    """
    if request.method == 'POST':
        connleaks = ConLeak.find_conn_leaks()
    return connleaks

@app.route('/get_nightly_conndata', methods=['POST'])
def insert_nightlybuild_data():
    """ This api parse captured connection leak data and insert data in mongo db
    """
    conn_data = request.data
    rel_no = request.headers['REL_NO']
    build_no = request.headers['BUILD_NO']
    #branch_name = request.headers['Branch_Name']
    return ConMong.put_nightlybuild_data(conn_data, rel_no, build_no)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)