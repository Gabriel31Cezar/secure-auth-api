from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


# --- Novos Schemas para o Filesearch ---

class IndexedFileResponse(BaseModel):
    id: int
    path: str
    filename: str
    extension: str
    size_bytes: int
    mtime: float
    sha256: str | None = None
    indexed_at: datetime
    camera_make: str | None = None
    camera_model: str | None = None
    taken_at: datetime | None = None
    gps_lat: float | None = None
    gps_lon: float | None = None
    orientation: int | None = None

    model_config = ConfigDict(from_attributes=True)


class ScanRequest(BaseModel):
    path: str


class ScanResponse(BaseModel):
    message: str
    files_changed: int