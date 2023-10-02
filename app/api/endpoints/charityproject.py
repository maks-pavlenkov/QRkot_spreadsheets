from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.validators import (check_name_duplicate, check_project_exists,
                                check_projects_before_delete,
                                check_projects_before_update)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charityproject import (charity_project_crud,
                                     create_charity_project)
from app.schemas.charityproject import (CharityProjectCreate, CharityProjectDB,
                                        CharityProjectUpdate)
from app.services.investing import invest_after_project

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True
)
async def create_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    await check_name_duplicate(project.name, session)
    project_data = await invest_after_project(session, project)
    new_project = await create_charity_project(project_data, session)
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_projects(
    session: AsyncSession = Depends(get_async_session)
):
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_project(
    project_id: int,
    obj_data: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    project = await check_project_exists(project_id, session)
    if obj_data.name is not None:
        await check_name_duplicate(obj_data.name, session)
    await check_projects_before_update(project_id, obj_data, session)
    project = await charity_project_crud.update(
        project, obj_data, session
    )
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]

)
async def remove_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    project = await check_project_exists(project_id, session)
    await check_projects_before_delete(project_id, session)
    project = await charity_project_crud.remove(project, session)
    return project