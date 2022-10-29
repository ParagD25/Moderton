from fastapi import FastAPI
from Blog.routers import blog,user,authentication
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials= True,
    allow_methods=['*'],
    allow_headers=['*']
)


app.include_router(authentication.authRouter)
app.include_router(blog.blogRouter)
app.include_router(user.userRouter)

@app.get("/",tags=['Welcome'])
def home():
    return {"Message":"Welcome To Moderton Blog Application"}