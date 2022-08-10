import datetime
import requests


class PyAirtable:
    def __init__(self, table_name):
        self.all_rows = None
        self.airtable_base = 'appKBi6VovD1nbeHJ'
        self.table_name = table_name
        self.payload = {
            "records": [
                {
                    "fields": {

                    }

                }

            ],
            "typecast": True

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
            "typeIntervention": "Type d'intervention",
            "nomCoordinateur": "Coordinateur",
            "nomArtisan": "Artisans",
            "status": "Statut de l'intervention",
            "modifiePar": "Modifié par",
        }

        self.headers = {
            "Authorization": "Bearer keyOlIBQGmClGzin1",
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

        response = requests.get(f"https://api.airtable.com/v0/{self.airtable_base}/{self.table_name}",
                                headers=self.headers, params=params)

        if len(response.json()['records']) > 0:
            self.all_rows = response.json()['records']
        else:
            return -1

    def searchRecord(self):
        fields = {}
        for key, val in self.post_request['key'].items():
            fields[self.header[key]] = val
        return self.getAllRecords(fields)

    def updateRecord(self, post_request: dict):
        # fixed
        self.post_request = post_request
        if self.post_request['key'] != {}:
            if self.searchRecord() == -1:
                return 'not found'
            self.buildPayload()
            self.payload['records'][0]['id'] = self.all_rows[0]['id']

            print(f'UPDATE PAYLOAD: {self.payload}')

            response = requests.patch(f"https://api.airtable.com/v0/{self.airtable_base}/{self.table_name}",
                                      headers=self.headers,
                                      json=self.payload)

            print(f'RESPONSE UPDATE: {response.json()}')
        else:
            print(f'NO FILTER TO APPLY!')

    def generateDate(self, string_date):
        return datetime.datetime.strptime(
            string_date.split('.')[0].replace('T', ' '), "%Y-%m-%d %H:%M:%S"). \
            strftime("%m/%d/%Y %I:%M%p").lower()

    def buildPayload(self, create=False):
        self.post_request = self.post_request['data']
        recordBuild = self.payload['records'][0]['fields']
        for jsonKey, airtableName in self.header.items():
            if jsonKey in self.post_request.keys():
                if self.post_request[jsonKey] == "":
                    pass
                elif jsonKey == "creeA":
                    recordBuild[airtableName] = self.post_request[jsonKey]
                elif jsonKey == "ticketId":
                    try:
                        recordBuild[airtableName] = int(self.post_request[jsonKey])
                    except Exception as e:
                        print(f'Ticket not added or not Integer')

                elif jsonKey == "nomArtisan":
                    recordBuild[airtableName] = ', '.join(self.post_request[jsonKey])
                else:
                    recordBuild[airtableName] = self.post_request[jsonKey]
        if 'disponibilite' in self.post_request.keys():
            dispo = self.post_request["disponibilite"]
            # startAt = self.generateDate(f'{dispo["date"]}T{dispo["starthour"]}:00')
            # endAt = self.generateDate(f'{dispo["date"]}T{dispo["endhour"]}:00')
            if 'starthour' in dispo.keys():
                print(f'{dispo["date"]}T{dispo["starthour"]}:00.000Z')
                recordBuild["Date/heure de l'intervention"] = f'{dispo["date"]}T{dispo["starthour"]}:00.000Z'
            else:
                print(f'{dispo["date"]}T00:00.000Z')
                recordBuild["Date/heure de l'intervention"] = f'{dispo["date"]}T00:00:00.000Z'
        print(recordBuild)

    def createRecord(self, post_request: dict, fromUpdate=False):
        self.post_request = post_request

        if not fromUpdate:
            self.payload['records'][0]['fields']["Statut de l'intervention"] = "A Programmer"
        self.buildPayload(create=True)

        response = requests.post(f"https://api.airtable.com/v0/{self.airtable_base}/{self.table_name}",
                                 headers=self.headers,
                                 json=self.payload)

        print(f'ON CREATE RESPONSE: {response.json()}')
