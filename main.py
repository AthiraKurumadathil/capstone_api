from fastapi import FastAPI
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

app = FastAPI(title="Organization API", version="1.0.0")

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


