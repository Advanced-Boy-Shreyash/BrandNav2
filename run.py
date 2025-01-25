from fastapi import FastAPI
from routes import book_routes, user_routes, borrow_routes

app = FastAPI(title="Library Management System")

# Include routers
app.include_router(book_routes.router, prefix="/books", tags=["Books"])
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(borrow_routes.router, prefix="/borrow",
                   tags=["Borrow Records"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
