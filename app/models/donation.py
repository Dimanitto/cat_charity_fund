from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base, ProjectDonationMixin


class Donation(ProjectDonationMixin, Base):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self) -> str:
        return f'Пожертвование на сумму {self.full_amount}'
