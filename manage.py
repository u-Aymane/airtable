from pyairtable import PyAirtable
from flask import Flask, request

app = Flask(__name__)


@app.route('/airtable', methods=['POST'])
def run():
    if request.method == 'POST':
        req = request.get_json()
        print(f'REQUEST: {req}')
        if req['action'] == "create":
            agent.createRecord(req)
            print('CREATE OLD!')
        elif req['action'] == "update":
            message = agent.updateRecord(req)
            print('UPDATING RECORD!')
            print(f'return value: {message}')
            if message is not None:
                print('AFTER NOT FOUND - UPDATING RECORD!')
                agent.createRecord(req, fromUpdate=True)

        else:
            return {'status': 'error - action not recognized'}

        return {'status': 'success'}


if __name__ == '__main__':
    agent = PyAirtable("Planning d'interventions")
    # agent.updateRecord()
    app.run(host="0.0.0.0", debug=True, port=1506)
    # main()
