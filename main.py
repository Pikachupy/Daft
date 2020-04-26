from fastapi import FastAPI, Response, HTTPException
from hashlib import sha256
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse

app = FastAPI()
app.num = 0
app.count = -1
app.users = {"trudnY": "PaC13Nt", "admin": "admin"}
app.secret = "secret"
app.tokens = []
patlist = []


@app.get("/")
def root():
	return {"message": "Hello World during the coronavirus pandemic!"}


@app.get("/welcome")
def welcome_to_the_jungle():
	return {"message": "Welcome to the jungle! We have funny games!"}


@app.post("/login")
def login_to_app(user: str, passw: str, response: Response):
	if user in app.users and passw == app.users[user]:
		s_token = sha256(bytes(f"{user}{passw}{app.secret}", encoding='utf8')).hexdigest()
		app.tokens += s_token
		response.set_cookie(key="session_token",value=s_token)
		response = RedirectResponse(url='/welcome')
		print('logged in')
		return response
	else:
		raise HTTPException(status_code=401)
