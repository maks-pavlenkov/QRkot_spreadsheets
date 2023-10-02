from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
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
        text(
            "SELECT name, description, (julianday(close_date) - julianday(create_date))  * 24 * 60 * 60 AS date_diff "
            "FROM charityproject WHERE fully_invested == True "
            "ORDER BY date_diff ASC"
        )
    )
    projects_with_diffs = []
    for result in projects:
        name = result.name
        description = result.description
        diff_milliseconds = result.date_diff
        diff_days = int(diff_milliseconds / (1000 * 60 * 60 * 24))
        diff_hours = int((diff_milliseconds % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
        diff_minutes = int((diff_milliseconds % (1000 * 60 * 60)) / (1000 * 60))
        diff_seconds = int((diff_milliseconds % (1000 * 60)) / 1000)
        diff_milliseconds = int(diff_milliseconds % 1000)
        prepared_diff = f"{diff_days}д {diff_hours}:{diff_minutes}:{diff_seconds}:{diff_milliseconds}"
        res = (name, description, prepared_diff)
        projects_with_diffs.append(res)
    for project in projects_with_diffs:
        print(project)
    return projects_with_diffs
