# Stats service entry point (FastAPI)
from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'Stats Service'}
