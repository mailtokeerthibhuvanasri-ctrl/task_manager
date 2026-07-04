from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import models
from database import engine
from routers import auth, task, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TaskFlow API",
    version="1.0.0",
    description="""
## TaskFlow Task Manager API

**How to use:**
1. **Register** → `POST /auth/register` with username, email, password
2. **Login** → `POST /auth/login` → copy the `access_token` from response
3. **Authorize** → Click 🔒 Authorize → paste just the token (no "Bearer " prefix)
4. Now use Tasks endpoints freely!
""",
    openapi_tags=[
        {"name": "1. Auth", "description": "Register and login to get your Bearer token"},
        {"name": "2. Tasks", "description": "Create, view, update and delete your tasks (requires auth)"},
        {"name": "3. Users", "description": "Get current user info (requires auth)"},
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(auth.router)
app.include_router(task.router)
app.include_router(user.router)

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def index(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.get("/register", response_class=HTMLResponse, include_in_schema=False)
def register_page(request: Request):
    return templates.TemplateResponse(request, "register.html")

@app.get("/login", response_class=HTMLResponse, include_in_schema=False)
def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html")

@app.get("/dashboard", response_class=HTMLResponse, include_in_schema=False)
def dashboard_page(request: Request):
    return templates.TemplateResponse(request, "dashboard.html")