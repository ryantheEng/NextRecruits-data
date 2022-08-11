import firebase_admin
from firebase_admin import db
from e2j import read_sheet

#service acc credentials
cred_obj = firebase_admin.credentials.Certificate('key_nr.json')

default_app = firebase_admin.initialize_app(cred_obj)

#root folder for contacts import
root_ = db.reference("/contacts",{'databaseURL':'https://console.firebase.google.com/u/0/project/nextrecruits-8114e/overview'})

sheetname = 'NCAA D1 M'

json = read_sheet(sheetname)
root_.set(json)