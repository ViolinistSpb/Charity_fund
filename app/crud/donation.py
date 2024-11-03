from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject, Donation, User
from .base_investment import base_investmemt


class CRUDDonation(CRUDBase):

    async def distribution_to_projects(
        self,
        donation: Donation,
        session: AsyncSession,
    ):
        all_open_projects = await session.execute(
            select(CharityProject).where(CharityProject.fully_invested == 0))
        all_open_projects = all_open_projects.scalars().all()

        for project in all_open_projects:
            base_investmemt(
                project=project, donation=donation, session=session
            )
        await session.commit()
        await session.refresh(donation)

    async def get_donation_by_user(
        self,
        session: AsyncSession,
        user: User
    ):
        donations = await session.execute(
            select(Donation).where(Donation.user_id == user.id))
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
