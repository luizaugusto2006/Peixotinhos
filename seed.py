"""Script para criar o album inicial com as fotos do Colégio Afrânio Peixoto."""
import os
from app import create_app
from models import db, Event, Photo
from datetime import date

app = create_app()

PHOTOS = [
    ("fachada_com_sr_rui.jpg", "Fachada do Colégio com o Sr. Rui"),
    ("fachada_2_antiga.jpg", "Fachada antiga do Colégio"),
    ("descida_do_afranio.jpg", "Descida do Afrânio Peixoto"),
    ("rua_do_afranio.jpg", "Rua do Afrânio Peixoto"),
    ("prof_ruy_afranio.jpg", "Professor Ruy - Afrânio Peixoto"),
    ("foto1.jpg", "Registro histórico"),
]

with app.app_context():
    if Event.query.first():
        print("Album ja existe. Pulando...")
    else:
        event = Event(
            title="Colégio Afrânio Peixoto - Acervo Histórico",
            description="Registro historico do Colégio Afrânio Peixoto, com fotos da fachada, arredores e professores.",
            date=date(2025, 1, 1),
            cover_photo="fachada_com_sr_rui.jpg",
            is_published=True,
        )
        db.session.add(event)
        db.session.flush()

        for i, (filename, caption) in enumerate(PHOTOS):
            photo = Photo(
                event_id=event.id,
                filename=filename,
                caption=caption,
                order=i,
            )
            db.session.add(photo)

        db.session.commit()
        print(f"Album criado com {len(PHOTOS)} fotos!")
        print(f"Capa: fachada_com_sr_rui.jpg")
