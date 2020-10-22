import string, random

from .model import Query
from . import db
""" Create unique ID not in DB """
def create_unique_id(length= 5):

    while True:

        id = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(length))

        if Query.query.filter_by(friendly_id= id).first():
            pass
        else:
            break

    return id
