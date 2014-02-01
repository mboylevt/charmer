# -*- coding: utf-8 -*-

from flask import render_template, Blueprint

reflection = Blueprint('reflection', __name__, template_folder='templates/reflection')


@reflection.route('/reflection')
def main_template():
    return render_template('reflection.html')