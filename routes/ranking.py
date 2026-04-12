from flask import Blueprint, jsonify, request
from db import get_connection

ranking_bp = Blueprint("ranking", __name__)