# -*- coding: utf-8 -*-
from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('limit', type=int)
parser.add_argument('offset', type=int)
