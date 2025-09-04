from fastapi import APIRouter

route = APIRouter()
#--------------------------------------------------------------------
@route.get('/all')
async def all():
    return {}
#--------------------------------------------------------------------
