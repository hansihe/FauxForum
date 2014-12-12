__author__ = 'hansihe'

from flask import Blueprint, abort, render_template
import os
import re

import markdown
import mdx_oembed
md = markdown.Markdown(extensions=[mdx_oembed.makeExtension({})])
32
blueprint = Blueprint("static", "static")

DOC_PATH = os.path.abspath(os.path.dirname(__file__) + '/../../static_pages/')

@blueprint.route("/s/<string:name>")
def get_static(name):
    p = os.path.abspath(os.path.join(DOC_PATH, name + '.md'))  # I am and should be really paranoid about this
    if not p.startswith(DOC_PATH) or not os.path.exists(p) or re.match('^[\w-]+$', name) is not None:
        abort(404)

    with open(p, 'r') as f:
        markup = md.convert(f.read())
        return render_template('static_container.jinja2', markup=markup)