#!/usr/bin/python3
""" Script that runs Flask """
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def teardown_session():
    """ Removes SQLAlchemy session """
    storage.close()


@app.route('/states_list', strict_slashes=False)
def display_html():
    """ Function called with /states_list route """
    states = storage.all(State)
    dict_to_html = {value.id: value.name for value in states.values()}
    return render_template('7-states_list.html',
                           cont=dict_to_html)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
