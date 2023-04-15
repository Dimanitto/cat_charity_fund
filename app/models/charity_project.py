from sqlalchemy import Column, String, Text

from app.core.db import Base, ProjectDonationMixin


class CharityProject(ProjectDonationMixin, Base):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self) -> str:
        return f'Проект {self.name} на сумму {self.full_amount}'
