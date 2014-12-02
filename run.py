from flask import Flask, render_template
from flask.ext.assets import Environment, Bundle

app = Flask(__name__)
app.secret_key = "JSHDAyugr37gYTdf6Fdiy3gdiat7dfjhasdy3i87yuhuydf37duyiuFdfoFTrdsAOtfr"

assets_folder = '../assets/'
environment = Environment(app)
environment.url = "/static"

css_main = Bundle(assets_folder + 'sass/app.scss', filters='scss' if app.debug else 'scss,cssmin', depends=(assets_folder + 'sass/*.scss', assets_folder + 'sass/**/*.scss'), output='gen/css/main.%(version)s.css')
environment.register('css_main', css_main)
js_main = Bundle(assets_folder + 'js/jquery-2.1.1.js',
                 assets_folder + 'js/modernizr.js',
                 assets_folder + 'js/foundation/foundation.js',
                 assets_folder + 'js/foundation/foundation.topbar.js',
                 assets_folder + 'js/foundation/foundation.dropdown.js',
                 assets_folder + 'js/foundation/foundation.alert.js',
                 assets_folder + 'js/foundation/foundation.tooltip.js',
                 filters=None if app.debug else 'rjsmin', output='gen/js/main.%(version)s.js')
environment.register('js_main', js_main)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

import ext
ext.init(app)
import models
ext.db.create_all()

import jinja
jinja.init(app)

from blueprints import auth, forum
app.register_blueprint(auth.blueprint)
app.register_blueprint(forum.blueprint)

from models.thread import Thread
@app.route('/')
def index():
    threads = Thread.query.order_by(Thread.id.desc())
    return render_template("forum_threads_view.jinja2", active_board_id="recent", title="Recent threads",
                           threads=threads)

if __name__ == '__main__':
    print(app.url_map)
    app.run(port=8181, debug=True)
