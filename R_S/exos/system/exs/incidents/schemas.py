import uuid
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from entities import Level


Base = declarative_base()


class IncidentSchema(Base):
    __tablename__ = 'incident'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    level: Mapped[Level] = mapped_column(Enum(Level), default=Level.LEVEL_1)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Incident [{self.id}]: {self.title}>"
