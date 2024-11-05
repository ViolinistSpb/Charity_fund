from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .validators import (
    check_name_duplicate,
    check_project_exists,
    check_invested_amount_is_zero,
    check_new_full_amount_is_higher,
    check_project_is_close
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charityproject import charityproject_crud
from app.schemas.charityproject import (
    CharityprojectCreate, CharityprojectDB, CharityprojectUpdate
)


router = APIRouter()


@router.post(
    '/',
    response_model=CharityprojectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charityproject(
        charityproject: CharityprojectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(charityproject.name, session)
    new_project = await charityproject_crud.create(charityproject, session)
    await charityproject_crud.distribution_free_donations(new_project, session)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityprojectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charityproject(
    project_id: int,
    obj_in: CharityprojectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    project = await check_project_exists(project_id, session)
    await check_project_is_close(project)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        await check_new_full_amount_is_higher(project, obj_in)

    return await charityproject_crud.update(project, obj_in, session)


@router.delete(
    '/{project_id}',
    response_model=CharityprojectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    project = await check_project_exists(project_id, session)
    await check_project_is_close(project)
    await check_invested_amount_is_zero(project)
    return await charityproject_crud.remove(project, session)


@router.get(
    '/',
    response_model=list[CharityprojectDB],
    response_model_exclude_none=True,
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session),
):
    return await charityproject_crud.get_multi(session)
