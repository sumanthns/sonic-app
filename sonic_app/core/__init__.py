from flask import Blueprint, render_template

core = Blueprint('core', __name__,
                 template_folder='templates',
                 url_prefix='/')