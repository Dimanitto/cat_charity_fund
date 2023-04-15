from typing import List
from fastapi import APIRouter, Depends
# Импортируем класс асинхронной сессии для аннотации параметра.
from sqlalchemy.ext.asyncio import AsyncSession

# Импортируем асинхронный генератор сессий.
from app.core.db import get_async_session
# from app.crud.meeting_room import meeting_room_crud
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectDB, CharityProjectCreate, CharityProjectUpdate
)
from app.api.validators import check_project_exists, check_name_duplicate
from app.core.user import current_superuser, current_user
from app.models import User
from app.services.funds_allocation import invested_project
from app.api.validators import check_project_before_delete, check_project_before_update


router = APIRouter()


@router.post(
    '/',
    # Указываем схему ответа.
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    # TODO потом разкомментить
    dependencies=[Depends(current_superuser)],
)
async def create_new_project(
        project: CharityProjectCreate,
        # Указываем зависимость, предоставляющую объект сессии, как параметр функции.
        session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(project.name, session)
    new_project = await charity_project_crud.create(project, session)
    new_project = await invested_project(session, new_project)
    return new_project

@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session),
):
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects

@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    # TODO потом разкомментить
    dependencies=[Depends(current_superuser)],
)
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    project = await check_project_before_delete(
        project_id=project_id, session=session
    )
    project = await charity_project_crud.remove(db_obj=project, session=session)
    return project

@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    # TODO потом разкомментить
    dependencies=[Depends(current_superuser)],
)
async def update_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    project = await check_project_before_update(
        project_id,
        obj_in.dict(),
        session,
    )
    project = await charity_project_crud.update(
        db_obj=project,
        obj_in=obj_in,
        session=session
    )
    return project
