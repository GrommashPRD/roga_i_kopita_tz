from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey, Integer, Table
from app.database import Base
import uuid

organization_activities = Table(
    "organization_activities",
    Base.metadata,
    Column("organization_id", String, ForeignKey("organizations.id", ondelete="CASCADE"), primary_key=True),
    Column("activity_id", Integer, ForeignKey("activities.id", ondelete="CASCADE"), primary_key=True),
)

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    title = Column(String(100), nullable=False)
    building_id = Column(String, ForeignKey("buildings.id", ondelete="RESTRICT"), nullable=False)

    building = relationship(
        "Building",
        back_populates="organizations"
    )
    activities = relationship(
        "Activity",
        secondary=organization_activities,
        back_populates="organizations"
    )
    phones = relationship(
        "OrganizationPhone",
        cascade="all, delete-orphan",
        backref="organization"
    )

class OrganizationPhone(Base):
    __tablename__ = "organization_phones"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    organization_id = Column(String, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    phone_number = Column(String(32), nullable=False)


