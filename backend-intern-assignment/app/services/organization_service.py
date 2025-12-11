from app.utils.database import master_db, client
from app.core.security import hash_password
from app.models.organization import org_collection_name
from bson import ObjectId

class OrganizationService:
    @staticmethod
    async def create_org(data):
        name = data.organization_name.lower()
        exists = await master_db.organizations.find_one({"name": name})
        if exists:
            return None
        collection_name = org_collection_name(name)
        db = client[name]
        try:
            db.create_collection(collection_name)
        except Exception:
            pass
        admin = {
            "email": data.email,
            "password": hash_password(data.password),
            "org": name
        }
        admin_result = await master_db.admins.insert_one(admin)
        org_data = {
            "name": name,
            "collection": collection_name,
            "admin_id": str(admin_result.inserted_id)
        }
        await master_db.organizations.insert_one(org_data)
        return org_data

    @staticmethod
    async def get_org(name):
        return await master_db.organizations.find_one({"name": name.lower()})

    @staticmethod
    async def update_org(data):
        name = data.organization_name.lower()
        org = await master_db.organizations.find_one({"name": name})
        if not org:
            return None
        new_collection = org_collection_name(name + "_updated")
        db = client[name]
        try:
            db.create_collection(new_collection)
        except Exception:
            pass
        await master_db.organizations.update_one(
            {"name": name},
            {"$set": {"collection": new_collection}}
        )
        return await master_db.organizations.find_one({"name": name})

    @staticmethod
    async def delete_org(name, admin_email):
        name = name.lower()
        org = await master_db.organizations.find_one({"name": name})
        if not org:
            return False
        admin = await master_db.admins.find_one({"org": name, "email": admin_email})
        if not admin:
            return False
        await client.drop_database(name)
        await master_db.organizations.delete_one({"name": name})
        return True
