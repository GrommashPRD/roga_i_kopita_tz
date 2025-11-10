from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from app.database import Base
from app.repo.organization.models import organization_activities


class Activity(Base):
    __tablename__ = "activities"

    __table_args__ = (
        UniqueConstraint("name", "parent_id", name="uq_activity_name_parent"),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    parent_id = Column(
        Integer,
        ForeignKey("activities.id", ondelete="CASCADE"),
        nullable=True,
    )
    parent = relationship(
        "Activity",
        back_populates="children",
        remote_side=[id],
    )
    children = relationship(
        "Activity",
        back_populates="parent",
        cascade="all, delete-orphan",
    )

    organizations = relationship(
        "Organization",
        secondary=organization_activities,
        back_populates="activities",
)