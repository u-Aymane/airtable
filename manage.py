from pyairtable import PyAirtable
from flask import Flask, request

app = Flask(__name__)


@app.route('/airtable', methods=['POST'])
def run():
    if request.method == 'POST':
        print(request.data)
        req = request.get_json()
        if req['action'] == "create":
            agent.createRecord(req)
            print('Creating Record! from create')
        elif req['action'] == "update" or req['action'] == "create/update":
            message = agent.updateRecord(req)
            print('Updating Record!')
            if message is not None:
                agent.createRecord(req, fromUpdate=True)
                print('Creating Record!')
        else:
            return {'status': 'error - action not recognized'}

        return {'status': 'success'}


if __name__ == '__main__':
    agent = PyAirtable("Planning d'interventions")
    # agent.updateRecord()
    app.run(host="0.0.0.0", debug=True, port=1506)
    # main()
