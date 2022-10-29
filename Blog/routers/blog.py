from fastapi import HTTPException, status, Depends, APIRouter
from Blog.models import Blog,BlogShow
from Blog.database import blog_collection
from Blog import oauth2
from Blog.convertion import convert_bson_to_json,convert_json_to_bson
import datetime
from typing import List

blogRouter = APIRouter(
    prefix="/blog",
    tags = ["Blog"]
)

@blogRouter.get("/", response_model=List[BlogShow],status_code=status.HTTP_200_OK)
async def view_blogs(current_user: int = Depends(oauth2.get_current_user)):
    blogs_list = []
    find_blog = blog_collection.find({"user": convert_bson_to_json(current_user['_id'])})
    async for blog in find_blog:
        blogs_list.append(blog)
    return blogs_list

# async def view_blogs():
#     blogList = []

#     async for blog in blog_collection.find():
#         blogList.append(blog)

#     return blogList


@blogRouter.get("/{id}", response_model=BlogShow,status_code=status.HTTP_200_OK)
async def view_blog(id: str, current_user: int = Depends(oauth2.get_current_user)):
    
    find_blog = await blog_collection.find_one({"_id": convert_json_to_bson(id)})
    if not find_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog of id {id} not found.")

    if find_blog["user"] != convert_bson_to_json(current_user["_id"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not Authorized")
        
    return find_blog

# async def view_blog(id: str):
    
#     find_blog = await blog_collection.find({"_id":id})

#     if not find_blog:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog of id {id} does not exist.")
    
#     return find_blog


@blogRouter.post("/create",status_code=status.HTTP_201_CREATED, response_model=BlogShow)
async def create_blog(blog: Blog, current_user : int = Depends(oauth2.get_current_user)):
    new_blog = blog.dict()
    new_blog['blog_created'] = datetime.datetime.now()
    new_blog['user'] = convert_bson_to_json(current_user["_id"])
    insert_blog = await blog_collection.insert_one(new_blog)
    return new_blog

# async def create_blog(blog: Blog):
#     ib = blog.dict()
#     res = await blog_collection.insert_one(ib)
#     return ib
#     # new_blog =blog_collection.insert_one(dict(blog))
#     # insert_blog = await blog_collection.find_one({"_id": new_blog.inserted_id})
#     # return {"New Blog":insert_blog}


@blogRouter.put("/{id}/update", response_model=BlogShow)
async def update_blog(blog: Blog, id: str, current_user: int = Depends(oauth2.get_current_user)):
    updated = await blog_collection.find_one({"_id": convert_json_to_bson(id)})
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog of id {id} not found.")
    if updated['user'] != convert_bson_to_json(current_user["_id"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not Authorized.")
   
    await blog_collection.update_one({"_id": convert_json_to_bson(id)}, {"$set":dict(blog)})

    return await blog_collection.find_one({"_id": convert_json_to_bson(id)})

# async def update_blog(blog: Blog, id: str):

#     find_blog = await blog_collection.find_one({"_id":id})

#     if not find_blog:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog of id {id} does not exist.")
   
#     await blog_collection.update_one({"_id": objectid(id)}, {"$set": dict(blog)})
#     return await blog_collection.find_one({"_id": objectid(id)})


@blogRouter.delete("/{id}/delete",status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(id: str, current_user: int = Depends(oauth2.get_current_user)):
    deleted = await blog_collection.find_one({"_id": convert_json_to_bson(id)})
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog of id {id} not found.")

    if deleted["user"] != convert_bson_to_json(current_user["_id"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not Authorized")
   
    await blog_collection.delete_one({"_id": convert_json_to_bson(id)})

# async def delete_todo(id: str):

#     find_blog = await blog_collection.find_one({"_id": id})
#     if not find_blog:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id {id} does not exist.")
   
#     await blog_collection.delete_one({"_id": objectid(id)})