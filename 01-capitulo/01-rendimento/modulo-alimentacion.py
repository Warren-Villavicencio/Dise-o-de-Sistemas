# models.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Alimentacion(Base):
    __tablename__ = 'alimentacion'

    id = Column(Integer, primary_key=True)
    animal_id = Column(Integer, nullable=False)
    tipo_alimento = Column(String, nullable=False)
    cantidad = Column(Float, nullable=False)
    fecha = Column(DateTime, nullable=False)

# repositories.py
from sqlalchemy.orm import Session
from models import Alimentacion

class AlimentacionRepository:
    def __init__(self, session: Session):
        self.session = session

    def crear_registro(self, alimentacion: Alimentacion):
        self.session.add(alimentacion)
        self.session.commit()
        return alimentacion

    def obtener_por_animal(self, animal_id: int):
        return self.session.query(Alimentacion).filter(Alimentacion.animal_id == animal_id).all()

# services.py
from datetime import datetime
from repositories import AlimentacionRepository
from models import Alimentacion

class AlimentacionService:
    def __init__(self, repo: AlimentacionRepository):
        self.repo = repo

    def registrar_alimentacion(self, animal_id: int, tipo_alimento: str, cantidad: float):
        nuevo_registro = Alimentacion(
            animal_id=animal_id,
            tipo_alimento=tipo_alimento,
            cantidad=cantidad,
            fecha=datetime.now()
        )
        return self.repo.crear_registro(nuevo_registro)

    def obtener_historial_alimentacion(self, animal_id: int):
        return self.repo.obtener_por_animal(animal_id)

# controllers.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from repositories import AlimentacionRepository
from services import AlimentacionService

router = APIRouter()

@router.post("/alimentacion")
def registrar_alimentacion(animal_id: int, tipo_alimento: str, cantidad: float, db: Session = Depends(get_db)):
    repo = AlimentacionRepository(db)
    service = AlimentacionService(repo)
    return service.registrar_alimentacion(animal_id, tipo_alimento, cantidad)

@router.get("/alimentacion/{animal_id}")
def obtener_historial_alimentacion(animal_id: int, db: Session = Depends(get_db)):
    repo = AlimentacionRepository(db)
    service = AlimentacionService(repo)
    return service.obtener_historial_alimentacion(animal_id)
