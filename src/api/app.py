import uvicorn
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from src.api.routers import (
    account_router,
    auth_router,
    transaction_router,
    user_router,
    users_router,
)
from src.config import settings


app = FastAPI(docs_url=None)


app.include_router(account_router)
app.include_router(auth_router)
app.include_router(transaction_router)
app.include_router(user_router)
app.include_router(users_router)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
)


def start_app() -> None:
    uvicorn.run(
        "api.app:app", reload=True, host=settings.API_HOST, port=settings.API_PORT
    )
