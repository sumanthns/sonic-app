from flask import Blueprint

device = Blueprint("device", __name__,
                   template_folder='templates',
                   static_folder='static',
                   url_prefix='/device')