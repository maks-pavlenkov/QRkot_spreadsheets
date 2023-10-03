import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import false

from app.models.charity_project import CharityProject
from app.models.donation import Donation
from app.schemas.charityproject import CharityProjectBase
from app.schemas.donation import DonationCreate


async def update_project_when_donation_bigger(
        project,
        full_amount_project
):
    project.fully_invested = 1
    project.invested_amount = full_amount_project
    project.close_date = datetime.datetime.now()


async def update_donation_when_project_bigger(
        donation
):
    donation.fully_invested = True
    donation.close_date = datetime.datetime.now()
    donation.invested_amount = donation.full_amount


async def invest_donations(
        session: AsyncSession,
        donation: DonationCreate
):
    projects_to_invest = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested == false()).order_by(
                CharityProject.create_date
        )
    )
    donation_data = donation.dict()
    donation_amount = donation_data['full_amount']
    for project in projects_to_invest.scalars().all():
        full_amount_project = project.full_amount
        invested_amount_project = project.invested_amount
        project_amount_left = full_amount_project - invested_amount_project
        if donation_amount >= project_amount_left:
            await update_project_when_donation_bigger(
                project, full_amount_project
            )
            donation_data['invested_amount'] = (
                donation_data.get('invested_amount', 0) + project_amount_left
            )
            donation_amount -= project_amount_left
            if not donation_amount:
                donation_data['fully_invested'] = True
                donation_data['close_date'] = datetime.datetime.now()
                return donation_data
        else:
            project.invested_amount = donation_amount + invested_amount_project
            donation_data['invested_amount'] = donation_amount
            donation_data['fully_invested'] = True
            donation_data['close_date'] = datetime.datetime.now()
            return donation_data
    return donation_data


async def invest_after_project(
        session: AsyncSession,
        project: CharityProjectBase
):
    opened_donations = await session.execute(
        select(Donation).where(
            Donation.fully_invested == false()
        ).order_by(Donation.create_date)
    )
    project_data = project.dict()
    for donation in opened_donations.scalars().all():
        donation_amount_left = donation.full_amount - donation.invested_amount
        project_amount = project_data['full_amount']
        if donation_amount_left >= project_amount:
            project_data['invested_amount'] = project_data['full_amount']
            project_data['fully_invested'] = True
            project_data['close_date'] = datetime.datetime.now()
            donation.invested_amount = project_data['full_amount'] + donation.invested_amount
            donation_amount_left -= project_data['full_amount']
            if not donation_amount_left:
                donation.fully_invested = True
                donation.close_date = datetime.datetime.now()
            return project_data
        else:
            await update_donation_when_project_bigger(donation)
            project_data['invested_amount'] = project_data.get('invested_amount', 0) + donation_amount_left
            return project_data
    return project_data
