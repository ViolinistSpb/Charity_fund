from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import UnionBase


class Donation(UnionBase):
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        return (
            f'Пожертвование на сумму {self.full_amount}'
        )
