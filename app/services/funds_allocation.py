from datetime import datetime
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import false

from app.models import CharityProject, Donation


async def invested_procces(
    session: AsyncSession,
    model: Union[Donation, CharityProject]
) -> Union[Donation, CharityProject]:
    """Процесс инвестирования"""
    db_model = (CharityProject if isinstance(model, Donation) else Donation)
    for obj in await session.execute(
            select(db_model).where(
                db_model.fully_invested == false()
            )
    ):
        # если проект/донат меньшей суммы чем нужная сумма проекта
        if model.full_amount - model.invested_amount < obj[0].full_amount - obj[0].invested_amount:
            remaining_money = model.full_amount - model.invested_amount
            obj[0].invested_amount += remaining_money
            model.fully_invested = True
            model.invested_amount += remaining_money
            model.close_date = datetime.now()
            break
        # если проект/донат большей суммы или равен чем нужная сумма проекта
        else:
            remaining_money = obj[0].full_amount - obj[0].invested_amount
            obj[0].invested_amount += remaining_money
            obj[0].fully_invested = True
            obj[0].close_date = datetime.now()
            model.invested_amount += remaining_money
            # частный случай когда сумма доната/проекта может быть одинаковой с необходимой суммой
            if model.invested_amount == model.full_amount:
                model.fully_invested = True
                model.close_date = datetime.now()

    await session.commit()
    await session.refresh(model)
    return model
