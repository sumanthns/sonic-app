from flask import flash
from sqlalchemy import and_
from sqlalchemy.orm import exc
from werkzeug.exceptions import abort


def get_object_or_404(model, *criterion):
    try:
        return model.query.filter(and_(*criterion)).one()
    except exc.NoResultFound, exc.MultipleResultsFound:
        abort(404)


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), "error")