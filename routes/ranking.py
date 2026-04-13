from flask import Blueprint, jsonify, request
from db import get_connection
from paginacion import generar_links_paginacion

ranking_bp = Blueprint("ranking", __name__)