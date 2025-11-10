from sqlalchemy import (
    Column,
    String,
    Float,
    CheckConstraint
)
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from app.database import Base
import uuid

class Building(Base):
    __tablename__ = "buildings"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    address = Column(String(250), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    geom = Column(Geometry(geometry_type="POINT", srid=4326), nullable=False)

    organizations = relationship(
        "Organization",
        back_populates="building",
        cascade="all",
    )

    __table_args__ = (
        CheckConstraint(
            "latitude >= -90 AND latitude <= 90", name="chk_latitude"
        ),
        CheckConstraint(
            "longitude >= -180 AND longitude <= 180", name="chk_longitude"
        ),
    )