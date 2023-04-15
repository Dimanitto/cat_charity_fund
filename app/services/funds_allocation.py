from typing import Optional, Union, Dict
from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User, CharityProject


async def invested_donation(session: AsyncSession, donation: Donation):
    for obj in await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested == False
            )
        ):
            # если донат меньшей суммы чем нужная сумма проекта
            if donation.full_amount - donation.invested_amount < obj[0].full_amount - obj[0].invested_amount:
                ostatok = donation.full_amount - donation.invested_amount
                obj[0].invested_amount += ostatok
                donation.fully_invested = True
                donation.invested_amount += ostatok
                donation.close_date = datetime.now()
                break
            # если донат большей суммы чем нужная сумма проекта
            else:
                ostatok = obj[0].full_amount - obj[0].invested_amount
                obj[0].invested_amount += ostatok
                obj[0].fully_invested = True
                obj[0].close_date = datetime.now()
                donation.invested_amount += ostatok
                
    await session.commit()
    await session.refresh(donation)

async def invested_project(session: AsyncSession, project: CharityProject):
    for obj in await session.execute(
            select(Donation).where(
                Donation.fully_invested == False
            )
        ):
            # если проект меньшей суммы чем нужная сумма проекта
            if project.full_amount - project.invested_amount <= obj[0].full_amount - obj[0].invested_amount:
                ostatok = project.full_amount - project.invested_amount
                obj[0].invested_amount += ostatok
                project.fully_invested = True
                project.invested_amount += ostatok
                project.close_date = datetime.now()
                break
            # если проект большей суммы чем нужная сумма проекта
            else:
                ostatok = obj[0].full_amount - obj[0].invested_amount
                obj[0].invested_amount += ostatok
                obj[0].fully_invested = True
                obj[0].close_date = datetime.now()
                project.invested_amount += ostatok
                
    await session.commit()
    await session.refresh(project)
    return project
