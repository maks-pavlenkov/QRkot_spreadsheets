from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import true


from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject

charity_project_crud = CRUDBase(CharityProject)


async def create_charity_project(
        new_project: dict,
        session: AsyncSession
) -> CharityProject:
    db_project = CharityProject(**new_project)
    session.add(db_project)
    await session.commit()
    await session.refresh(db_project)
    return db_project


async def get_projects_by_completion_rate(
        session: AsyncSession
):
    projects = await session.execute(
        select(
            CharityProject
        ).where(CharityProject.fully_invested == true())
    )
    return sorted(
        projects.scalars().all(),
        key=lambda obj: obj.close_date - obj.create_date
    )
