from sqlalchemy import Column, String, Text

from app.core.db import UnionBase


class CharityProject(UnionBase):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (
            f'Благотварительный проект {self.name} на сумму {self.full_amount}'
            f'открыт {self.create_date}, собрано {self.invested_amount}'
        )