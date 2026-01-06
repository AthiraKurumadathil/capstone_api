from fastapi import FastAPI
from organizations import router as organizations_router
from activities import router as activities_router
from trainers import router as trainers_router

app = FastAPI(title="Organization API", version="1.0.0")

# Include routers
app.include_router(organizations_router)
app.include_router(activities_router)
app.include_router(trainers_router)

# ============== HEALTH CHECK ==============
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


