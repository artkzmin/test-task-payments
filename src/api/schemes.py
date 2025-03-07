from pydantic import BaseModel


class AccessToken(BaseModel):
    access_token: str


class ID(BaseModel):
    id: int


class StatusOK(BaseModel):
    status: str = "OK"
