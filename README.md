# Airtable
Automate CRM and Airtable process
## Installation

```bash
pip install requests
pip install flask
```

## Usage

```python
from pyairtable import PyAirtable
from flask import Flask, request

app = Flask(__name__)


@app.route('/airtable', methods=['POST'])
def run():
    if request.method == 'POST':
        print(request.get_json())
        req = request.get_json()
        if req['action'] == "create":
            agent.createRecord(req)
        elif req['action'] == "update":
            message = agent.updateRecord(req)
            if message is not None:
                return {'status': f'error - {message}'}
        else:
            return {'status': 'error - action not recognized'}

        return {'status': 'success'}


if __name__ == '__main__':
    agent = PyAirtable("Planning d'interventions")
    app.run(host="0.0.0.0", debug=True)
```

## POST Example
Add rows at Airtable
```json
{
   "action":"create",
   "data":{
      "ticketId": 8520,
      "_id":"62ed37b1535ee60512a0b80f",
      "nomClient":"Adnane JABRI",
      "idClient":"610974fc102e0b0b54fd4cfd",
      "tele":"+212674469590",
      "email":"adnane.jabri@gmail.com",
      "creeA":"2022-08-05T15:30:57.000Z",
      "commentaire":"pko",
      "univers":[
         "Climatisation",
         "Bricolage"
      ],
      "typeIntervention":"Visite + prestation",
      "__v":0
   }
}
```

Update a row 

```json
{
   "action": "update",
   "key":{
      "creeA":"2022-08-05T08:14:39.000+00:00",
      "nomClient":"Aymane Benani"
      // any column filter could be added here
   },
   "data":{
      "nomClient":"SULZER MAROC",
      "tele":"+212660468367",
      "creeA":"2022-08-05T08:14:39.000+00:00",
      "ticketId":14591,
      "commentaire":"text",
      "idClient":"62ecdf89f783c2fa417dc326",
      "univers":[
         "Electricité"
      ],
      "__v":0
   }
}
```

## License
[MIT](https://choosealicense.com/licenses/mit/)