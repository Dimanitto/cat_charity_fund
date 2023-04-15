from fastapi import APIRouter

from app.api.endpoints import (
    donation_router, user_router, project_router
)

main_router = APIRouter()
main_router.include_router(
    donation_router, prefix='/donation', tags=['Donations']
)
main_router.include_router(
    project_router, prefix='/charity_project', tags=['Charity Projects']
)
# main_router.include_router(
#     reservation_router, prefix='/reservations', tags=['Reservations']
# )
main_router.include_router(user_router)