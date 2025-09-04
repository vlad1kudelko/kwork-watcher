from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from api.statistics import route as route__api_statistics

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(route__api_statistics, prefix='/api')

@app.get('/')
async def api_index():
    return FileResponse('static/index.html')

app.mount('/', StaticFiles(directory='static'), name='static')

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0')
