from typing import Optional
from sqlalchemy import func, select, extract, desc, literal
from sqlalchemy.ext.asyncio import AsyncSession

from .base_investment import base_investmemt
from app.crud.base import CRUDBase
from app.models import CharityProject, Donation


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
        return db_project_id.scalars().first()

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
        return db_project.scalars().first()

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

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession,
    ):
        sec_diff = (extract('epoch', CharityProject.close_date) -
                    extract('epoch', CharityProject.create_date))
        query = select(
            [CharityProject.name,
             sec_diff.label('sec_diff'),
             CharityProject.description]
        )

        all_closed_project = await session.execute(
            query.where(
                CharityProject.fully_invested == 1
            ).order_by('sec_diff')
        )
        return all_closed_project.all()


charityproject_crud = CRUDCharityproject(CharityProject)
