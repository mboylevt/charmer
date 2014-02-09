# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask.ext.assets import Environment, Bundle

from reflection import reflection
from shapewaysapi import shapeways_api

# Register flask application and blueprints, and retrieve environment
app = Flask(__name__)
app.register_blueprint(reflection)
app.register_blueprint(shapeways_api)
env = Environment(app)

app.config.update(dict(
    ASSETS_DEBUG=True
))

# Register javascript
js_common = Bundle('js/jquery/jquery.js', 'js/jquery/jquery-forms.js', output='gen/common.js')
js_charmer = Bundle('js/charmer/shapejs-charmer.js', 'js/charmer/sw.shapejs.creator-2.0.js',
                    'js/charmer/charmer.js', output='gen/charmer.js')
env.register('js_common', js_common)
env.register('js_charmer', js_charmer)

# Register css
css_common = Bundle('css/style.css', output='gen/common.css')
env.register('css_common', css_common)

@app.route('/')
def main_template():
    return render_template('selector/selector.html', widgets=[])

if __name__ == '__main__':
    app.run(debug=True, port=5051)
