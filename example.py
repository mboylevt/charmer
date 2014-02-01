# -*- coding: utf-8 -*-

from flask import render_template, Blueprint

example = Blueprint('example', __name__, template_folder='templates/example')


@example.route('/example')
def main_template():
    return render_template('example.html')