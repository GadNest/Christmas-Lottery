from flask import Flask, render_template, request, session, flash
from main import addUser, addedUsers, removeUser, clearDatabase
from flask_session import Session
from tinydb import TinyDB, Query

db_users = TinyDB('db_users.json')

get = Query()

leftover = db_users.search((get.chosen == '') & (get.participant != 'kacper'))
chosenName = leftover[0]
print(chosenName)