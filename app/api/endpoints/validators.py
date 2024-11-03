from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charityproject_crud
from app.models.charity_project import CharityProject
from app.schemas.charityproject import CharityprojectUpdate


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    project_id = await charityproject_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await charityproject_crud.get_project_by_id(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return project


async def check_invested_amount_is_zero(
    project_id: int,
    session: AsyncSession,
) -> None:
    project = await charityproject_crud.get_project_by_id(project_id, session)
    if project.invested_amount != 0:
        raise HTTPException(
            status_code=400,
            detail='Проект уже содержит внесенные средства!',
        )


async def check_new_full_amount_is_higher(
    project_id: int,
    obj_in: CharityprojectUpdate,
    session: AsyncSession,
) -> None:
    project = await charityproject_crud.get_project_by_id(project_id, session)
    if obj_in.full_amount < project.full_amount:
        raise HTTPException(
            status_code=422,
            detail='Новая требуемая сумма меньше изначальной!',
        )


async def check_project_is_close(
    project_id: int,
    session: AsyncSession,
) -> None:
    project = await charityproject_crud.get_project_by_id(project_id, session)
    if project.fully_invested == 1:
        raise HTTPException(
            status_code=400,
            detail='Нельзя удалять или модифицировать закрытые проекты!',
        )