from fastapi import APIRouter
from fastapi.responses import ORJSONResponse


router = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_all_users():
    return ORJSONResponse([{"hello": "world"}])
# @router.get("/")
# async def get_all_users(user: User = 
# Depends(get_current_active_user),
#                         db: Session = Depends(get_db)):
#     """
#     # Get a list of all users

#     **Access:**
#     - Admins get a list of all users.
#     - Users with lower rights get a list with only the enabled users.
#     """
#     if user.super_admin:
#         return get_users_admin(db=db)
#     else:
#         return get_users(db=db)