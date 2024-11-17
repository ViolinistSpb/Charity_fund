from typing import Any
from datetime import datetime
# Класс «обёртки»
from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser

from app.crud.charityproject import charityproject_crud
from app.services_google_api import (
    set_user_permissions, spreadsheets_create, spreadsheets_update_value)


router = APIRouter()


@router.post(
    '/',
    # response_model=list[dict[str, str]],
    # dependencies=[Depends(current_superuser)],
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service)
):
    """Только для суперюзеров."""
    projects = await charityproject_crud.get_projects_by_completion_rate(
        session)
    print('get_all_closed_project from get report: ', projects)
    #  Вызов функций
    spreadsheetid = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheetid, wrapper_services)
    await spreadsheets_update_value(spreadsheetid,
                                    projects,
                                    wrapper_services)
    return projects