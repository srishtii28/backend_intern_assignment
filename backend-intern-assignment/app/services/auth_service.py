from app.utils.database import master_db
from app.core.security import verify_password, create_access_token

class AuthService:
    @staticmethod
    async def login(email, password):
        admin = await master_db.admins.find_one({"email": email})
        if not admin:
            return None
        if not verify_password(password, admin["password"]):
            return None
        token = create_access_token({"email": email, "org": admin["org"]})
        return token
