import datetime
import requests


class PyAirtable:
    def __init__(self, table_name):
        self.all_rows = None
        self.table_name = table_name
        self.payload = {
            "records": [
                {
                    "fields": {

                    }
                },
            ]
        }
        self.header_array = ["ID Ticket", "Nom/prénom client", "Métiers concernés", "Coordinateur",
                             "Type d'intervention",
                             "Date/heure de l'intervention", "Commentaires/Dispo du client", "Lien du devis/facture",
                             "Artisans", "Statut de l'intervention", "Etat de l'intervention", "Modifié le",
                             "Modifié par",
                             "Créé par", "Créé le", "Commentaires", "Date d'affectation", "Pro en retard",
                             "Réseau d'artisans copy", "Réseau d'artisans copy 2", "Réseau de prestataires copy",
                             "Réseau de prestataires copy 2", "Pro No-Show", "Réseau de prestataires copy 3",
                             "Réseau de prestataires copy 4", "Réseau de prestataires copy 5"]

        self.header = {
            "ticketId": "ID Ticket",
            "nomClient": "Nom/prénom client",
            "commentaire": "Commentaires/Dispo du client",
            "creeA": "Créé le",
            "univers": "Métiers concernés",
            "typeIntervention": "Type d'intervention"
        }

        self.headers = {
            "Authorization": "Bearer keyA5f9aRHbmsueYa",
            "Content-Type": "application/json"
        }
        self.post_request = None

    def getAllRecords(self, fields):
        filterByFormula = []
        for key, val in fields.items():
            filterByFormula.append("{" + key + "} = '" + str(val) + "'")

        params = {
            "filterByFormula": f'AND({", ".join(filterByFormula)})',
            "maxRecords": 1
        }

        print(params)

        response = requests.get(f"https://api.airtable.com/v0/app1a68POzN9C7dHL/{self.table_name}",
                                headers=self.headers, params=params)

        print(response)
        if len(response.json()['records']) > 0:
            self.all_rows = response.json()['records']
        else:
            return -1

    def searchRecord(self):
        fields = {}
        for key, val in self.post_request['key'].items():
            if key == "creeA":
                fields[self.header[key]] = self.generateDate(val)
            else:
                fields[self.header[key]] = val

        return self.getAllRecords(fields)

    def updateRecord(self, post_request: dict):
        if post_request:
            self.post_request = post_request
        if self.searchRecord() == -1:
            return 'not found'
        self.buildPayload()
        self.payload['records'][0]['id'] = self.all_rows[0]['id']
        # print(self.payload)
        print(len(self.all_rows), self.all_rows)
        response = requests.patch(f"https://api.airtable.com/v0/app1a68POzN9C7dHL/{self.table_name}",
                                  headers=self.headers,
                                  json=self.payload)

        print(response.text)

    def generateDate(self, string_date):
        return datetime.datetime.strptime(
            string_date.split('.')[0].replace('T', ' '), "%Y-%m-%d %H:%M:%S"). \
            strftime("%m/%d/%Y %I:%M%p").lower()

    def buildPayload(self):
        self.post_request = self.post_request['data']
        for jsonKey, airtableName in self.header.items():

            # if isinstance(self.post_request[jsonKey], list):
            #     multiple_choice = []
            #     for i in self.post_request[jsonKey]:
            #         if '/' in i:
            #             multiple_choice += i.split("/")
            #         else:
            #             multiple_choice += [i]
            #
            #     self.payload['records'][0]['fields'][airtableName] = multiple_choice
            if self.post_request[jsonKey] == "":
                pass
            elif jsonKey == "creeA":
                self.payload['records'][0]['fields'][airtableName] = self.generateDate(self.post_request[jsonKey])
            elif jsonKey == "ticketId":
                self.payload['records'][0]['fields'][airtableName] = int(self.post_request[jsonKey])
            else:
                self.payload['records'][0]['fields'][airtableName] = self.post_request[jsonKey]

        print(self.payload)

    def createRecord(self, post_request: dict):
        if post_request:
            self.post_request = post_request

        self.buildPayload()
        self.payload['records'][0]['fields']["Statut de l'intervention"] = "A Programmer"
        response = requests.post(f"https://api.airtable.com/v0/app1a68POzN9C7dHL/{self.table_name}",
                                 headers=self.headers,
                                 json=self.payload)

        print(response.text)
