from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject, Donation
from .base_investment import base_investmemt


class CRUDCharityproject(CRUDBase):

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def get_project_by_id(
        self,
        project_id: int,
        session: AsyncSession,
    ) -> CharityProject:
        db_project = await session.execute(
            select(CharityProject).where(
                CharityProject.id == project_id
            )
        )
        db_project = db_project.scalars().first()
        return db_project

    async def distribution_free_donations(
        self,
        project: CharityProject,
        session: AsyncSession,
    ):
        all_positive_donations = await session.execute(
            select(Donation).where(Donation.fully_invested == 0))
        all_positive_donations = all_positive_donations.scalars().all()

        for donation in all_positive_donations:
            base_investmemt(
                project=project, donation=donation, session=session
            )

        await session.commit()
        await session.refresh(project)


charityproject_crud = CRUDCharityproject(CharityProject)