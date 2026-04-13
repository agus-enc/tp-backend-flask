from flask import Blueprint, jsonify, request
from db import get_connection
from paginacion import generar_links_paginacion

usuarios_bp = Blueprint("usuarios", __name__)