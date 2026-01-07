from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from organizations import router as organizations_router
from activities import router as activities_router
from trainers import router as trainers_router
from activitytrainers import router as activity_trainers_router
from attendance import router as attendance_router
from students import router as students_router
from batches import router as batches_router
from batchsessions import router as batch_sessions_router
from categories import router as categories_router
from feeplans import router as feeplans_router
from invoices import router as invoices_router
from payments import router as payments_router
from roles import router as roles_router
from users import router as users_router
from utils.auth import JWTMiddleware

app = FastAPI(title="Organization API", version="1.0.0")

# ============== OPENAPI SECURITY SCHEME ==============
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Organization API",
        version="1.0.0",
        description="Activity Management and Billing System API",
        routes=app.routes,
    )
    
    # Add security scheme for JWT Bearer token
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter JWT token obtained from /users/authenticate/login endpoint"
        }
    }
    
    # Add security requirement to all endpoints (except public ones)
    openapi_schema["security"] = [{"Bearer": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# ============== CORS MIDDLEWARE ==============
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============== JWT AUTHENTICATION MIDDLEWARE ==============
app.add_middleware(JWTMiddleware)

# Include routers
app.include_router(organizations_router)
app.include_router(activities_router)
app.include_router(trainers_router)
app.include_router(activity_trainers_router)
app.include_router(attendance_router)
app.include_router(students_router)
app.include_router(batches_router)
app.include_router(batch_sessions_router)
app.include_router(categories_router)
app.include_router(feeplans_router)
app.include_router(invoices_router)
app.include_router(payments_router)
app.include_router(roles_router)
app.include_router(users_router)

# ============== HEALTH CHECK ==============
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# ============== PROTECTED ENDPOINT (requires JWT token) ==============
@app.get("/protected/profile")
async def get_profile():
    """
    Protected endpoint - requires valid JWT token in Authorization header.
    Example: Authorization: Bearer <your_jwt_token>
    """
    return {
        "message": "Access granted",
        "user_id": "user_id_from_token",
        "email": "email_from_token",
        "token_payload": current_user["payload"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


