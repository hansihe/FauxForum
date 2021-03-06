from flask import Flask, render_template
from flask.ext.assets import Environment, Bundle

app = Flask(__name__)

app.config.from_pyfile("local_config.py")

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

import ext
ext.init(app)
import models
ext.db.create_all()

import jinja
jinja.init(app)

from blueprints import auth, forum, static
app.register_blueprint(auth.blueprint)
app.register_blueprint(forum.blueprint)
app.register_blueprint(static.blueprint)

from models.thread import Thread
from models.post import Post
from sqlalchemy.orm import aliased

@app.route('/')
def index():
    #last_post = Post.query.order_by(Post.id.desc()).limit(1).subquery()
    #last_post_alias = aliased(Post, last_post)
    #threads = ext.db.session.query(Thread, last_post_alias).join(last_post_alias, Thread.id == last_post_alias.thread_id).order_by(Thread.id.desc()).all()
    threads = ext.db.session.query(Thread).order_by(Thread.id.desc()).all()

    print(threads)
    return render_template("forum_threads_view.jinja2", active_board_id="recent", title="Recent threads",
                           threads=threads)

if __name__ == '__main__':
    app.run(port=8181, debug=True)
