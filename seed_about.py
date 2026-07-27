"""Script para popular os tópicos da página Sobre."""
from app import create_app
from models import db, AboutTopic

TOPICS = [
    {
        "title": "Um pouco da nossa história",
        "content": (
            "O Colégio Rui Afrânio Peixoto foi fundado pelo Professor Rui Afrânio Peixoto, "
            "uma figura carismática e respeitada pela comunidade de Nova Iguaçu. O colégio ficava "
            "localizado na base de um morro, e para chegar até ele os alunos subiam uma ladeira "
            "calçada de paralelepípedos, em meio a muitas árvores e passarinhos."
        ),
        "order": 0,
    },
    {
        "title": "O Professor Rui",
        "content": (
            "O Professor Rui Afrânio Peixoto, diretor e dono do colégio, era conhecido por sua "
            "\"bata impecavelmente branca, com seu nome gravado no bolso sobre o coração\". "
            "Solene e bondoso, ele tratava todos os alunos com afeto e atenção. Sentado em seu posto "
            "estratégico entre os dois pátios, observava toda a área como um verdadeiro guardião.\n\n"
            "Ele possuía uma estação de radioamador (PY), de onde modulava com o mundo. Também "
            "mantinha um sistema de som com pequenas caixas em cada sala de aula, acima do quadro "
            "negro, por onde ouvia e se comunicava com os alunos durante as aulas."
        ),
        "order": 1,
    },
    {
        "title": "A vida no colégio",
        "content": (
            "Naquele tempo, meninos e meninas estudavam em salas e recreios separados. Havia o "
            "pátio dos alunos, acima, e o das alunas, num nível mais abaixo — que era ao mesmo tempo "
            "quadra de futebol, vôlei e basquete. Cada um com sua cantina.\n\n"
            "O colégio possuía uma biblioteca, um teatro, e uma área verde enorme com muitas árvores. "
            "Uma das atividades dos professores de arte era construir casinhas de passarinho, que "
            "depois eram penduradas nas árvores da área central. O baixo pátio mais tarde ganhou "
            "uma piscina."
        ),
        "order": 2,
    },
    {
        "title": "Professores inesquecíveis",
        "content": (
            "Dentre os professores que marcaram gerações, estão Prof. Neo (matemática), "
            "Prof. Georgina, Prof. Jorge, Prof. Adalberto (educação física), Prof. Iracema (geografia), "
            "Prof. Rosinha, Prof. Alice, Prof. Zezé, Prof. Ferenk (inglês), Prof. Zezinho (geografia) "
            "e Seu Mello (inspetor)."
        ),
        "order": 3,
    },
    {
        "title": "O legado",
        "content": (
            "O Colégio Afrânio Peixoto marcou a vida de inúmeras gerações de iguaçuanos. "
            "Como disse um ex-aluno: \"Foi uma infância maravilhosa com um mega ensino de qualidade.\" "
            "Este site é uma homenagem a essa história, preservando as memórias e fotos "
            "de quem viveu momentos inesquecíveis naquele colégio."
        ),
        "order": 4,
    },
]

app = create_app()

with app.app_context():
    if AboutTopic.query.first():
        print("Tópicos já existem. Pulando...")
    else:
        for t in TOPICS:
            topic = AboutTopic(title=t["title"], content=t["content"], order=t["order"])
            db.session.add(topic)
        db.session.commit()
        print(f"{len(TOPICS)} tópicos criados com sucesso!")
