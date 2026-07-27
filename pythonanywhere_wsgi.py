import os
import sys

# Configurar variáveis de ambiente ANTES de importar o app
os.environ["SECRET_KEY"] = "peixotinhos-prod-chave-segura-2026"

# Diretório do projeto
PROJECT_DIR = "/home/peixotinhos/Peixotinhos"
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

from app import app as application
