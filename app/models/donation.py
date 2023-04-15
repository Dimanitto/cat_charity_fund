from sqlalchemy import Column, ForeignKey, Text, Integer
from sqlalchemy.orm import relationship
from app.core.db import Base, ProjectDonationMixin


class Donation(ProjectDonationMixin, Base):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self) -> str:
        return f'Пожертвование на сумму {self.full_amount}'
