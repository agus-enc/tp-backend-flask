from flask import Blueprint, jsonify, request
from db import get_connection

partidos_bp = Blueprint("partidos", __name__)