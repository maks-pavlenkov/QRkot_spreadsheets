from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.charityproject import charity_project_crud
from app.schemas.charityproject import CharityProjectUpdate


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession
):
    project_id = await charity_project_crud.get_by_attribute('name', project_name, True, session)
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession
):
    project = await charity_project_crud.get_by_attribute('id', str(project_id), True, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Такого проекта не существует!'
        )
    return project


async def check_projects_before_delete(
        project_id: int,
        session: AsyncSession
):
    project = await charity_project_crud.get_by_attribute('id', str(project_id), True, session)
    if project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def check_projects_before_update(
    obj_id: int,
    obj_data: CharityProjectUpdate,
    session: AsyncSession
):
    obj_data_d = obj_data.dict(exclude_unset=True)
    project = await charity_project_crud.get_by_attribute('id', str(obj_id), True, session)
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
    is_none = all(value is None for value in list(obj_data_d.values()))
    if is_none:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Разрешенные поля не переданы'
        )
    print(obj_data_d, '===========================================')
    if 'invested_amount' in obj_data_d:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Разрешенные поля не переданы'
        )
    if 'full_amount' in obj_data_d:
        update_amount = obj_data_d['full_amount']
        print(update_amount)
        print(project.invested_amount)
        if update_amount < project.invested_amount:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Не разрешено ставить требуемую сумму меньше текущей'
            )