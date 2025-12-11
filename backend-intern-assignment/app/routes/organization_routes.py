from fastapi import APIRouter, HTTPException
from app.schemas.organization import CreateOrgRequest, UpdateOrgRequest
from app.services.organization_service import OrganizationService

router = APIRouter(prefix="/org")

@router.post("/create")
async def create_org(data: CreateOrgRequest):
    result = await OrganizationService.create_org(data)
    if not result:
        raise HTTPException(status_code=400, detail="Organization already exists")
    return result

@router.get("/get")
async def get_org(organization_name: str):
    org = await OrganizationService.get_org(organization_name)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org

@router.put("/update")
async def update_org(data: UpdateOrgRequest):
    updated = await OrganizationService.update_org(data)
    if not updated:
        raise HTTPException(status_code=404, detail="Organization does not exist")
    return updated

@router.delete("/delete")
async def delete_org(organization_name: str, email: str):
    deleted = await OrganizationService.delete_org(organization_name, email)
    if not deleted:
        raise HTTPException(status_code=403, detail="Forbidden or not found")
    return {"success": True}
