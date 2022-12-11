from flask import Blueprint, jsonify, request, make_response
from utils.format import format_currency

format = Blueprint('format', __name__)


@format.route('/', methods=['POST'])
def format_default():
    elements = request.json.get("elements")
    for i in range(len(elements)):
        elements[i]["value"] = format_currency(elements[i]["value"])
    return make_response(jsonify(elements))
