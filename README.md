# 🐟 Peixotinhos — Site Institucional de Peixaria

Site institucional para peixaria com página inicial, seção "Sobre", **galeria de eventos com fotos** e painel administrativo completo.

> 🌐 **Online:** [peixotinhos.pythonanywhere.com](https://peixotinhos.pythonanywhere.com)

---

## ✨ Funcionalidades

### 🏠 Área Pública
- Página inicial com identidade visual da peixaria.
- Página **"Sobre"** com tópicos editáveis.
- **Galeria de eventos** com fotos, legendas e páginas detalhadas.
- Animações de scroll-reveal e **modo escuro**.

### 🔒 Painel Administrativo
- **Login de administradores** (Flask-Login).
- CRUD de **eventos** com upload de múltiplas fotos.
- Edição de legendas e exclusão de fotos.
- **Gestão de usuários**: criar, alterar senha e excluir.
- Edição dos tópicos da página "Sobre".

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Uso |
|---|---|
| **Python** | Linguagem principal |
| **Flask** | Framework web |
| **Flask-SQLAlchemy** | ORM e banco de dados |
| **Flask-Login** | Autenticação |
| **SQLite** | Banco de dados |
| **PythonAnywhere** | Hospedagem em produção |

---

## 🚀 Como rodar localmente

```bash
# 1. Clonar
git clone https://github.com/luizaugusto2006/Peixotinhos.git
cd Peixotinhos

# 2. Ambiente virtual
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/macOS

# 3. Dependências
pip install -r requirements.txt

# 4. Rodar
python app.py
```

Acesse `http://127.0.0.1:5000`.

---

## 📄 Licença

Este projeto é de uso pessoal e está licenciado sob a [MIT License](LICENSE).
