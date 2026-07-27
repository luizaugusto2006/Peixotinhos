import os
from app import app

# PythonAnywhere WSGI configuration
# Copie este conteúdo para o seu arquivo WSGI no PythonAnywhere:
# /var/www/luizaugusto2006_pythonanywhere_com_wsgi.py

# Adicione o diretório do projeto ao sys.path
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
if PROJECT_DIR not in __import__("sys").path:
    __import__("sys").path.insert(0, PROJECT_DIR)

application = app
