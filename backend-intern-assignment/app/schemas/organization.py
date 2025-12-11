from pydantic import BaseModel

class CreateOrgRequest(BaseModel):
    organization_name: str
    email: str
    password: str

class GetOrgRequest(BaseModel):
    organization_name: str

class UpdateOrgRequest(BaseModel):
    organization_name: str
    email: str
    password: str

class DeleteOrgRequest(BaseModel):
    organization_name: str
