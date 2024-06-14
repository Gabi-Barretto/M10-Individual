from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import uvicorn
import logging
import os

os.makedirs("./logs", exist_ok=True)
logging.basicConfig(
    filename='./logs/app_logs.log',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.WARNING
)

app = FastAPI()

class BlogPost(BaseModel):
    id: int
    title: str
    content: str

blog_posts: List[BlogPost] = []

@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    log_data = f"METHOD: {request.method}, URL: {request.url}, STATUS: {response.status_code}"
    if response.status_code >= 400:
        logging.warning(log_data)
    return response

@app.post('/blog', response_model=BlogPost)
def create_blog_post(request: BlogPost):
    try:
        blog_posts.append(request)
        logging.warning(f"Created BlogPost: {request.dict()}")
        return JSONResponse(content=request.dict(), status_code=201)
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid request")
    except Exception as e:
        logging.error(f"Error creating BlogPost: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/blog')
def get_blog_posts():
    return JSONResponse({'posts': [blog.dict() for blog in blog_posts]}, status_code=200)

@app.get('/blog/{id}')
def get_blog_post(id: int):
    for post in blog_posts:
        if post.id == id:
            return JSONResponse(content={'post': post.dict()}, status_code=200)
    logging.warning(f"BlogPost not found: {id}")
    return JSONResponse(content={'error': 'Post not found'}, status_code=404)

@app.delete('/blog/{id}')
def delete_blog_post(id: int):
    for post in blog_posts:
        if post.id == id:
            blog_posts.remove(post)
            logging.warning(f"Deleted BlogPost: {id}")
            return JSONResponse(content={'status': 'success'}, status_code=200)
    logging.warning(f"BlogPost not found: {id}")
    return JSONResponse(content={'error': 'Post not found'}, status_code=404)

@app.put('/blog/{id}')
def update_blog_post(id: int, request: BlogPost):
    try:
        for post in blog_posts:
            if post.id == id:
                post.title = request.title
                post.content = request.content
                logging.warning(f"Updated BlogPost: {post.dict()}")
                return JSONResponse(content={'status': 'success'}, status_code=200)
        logging.warning(f"BlogPost not found: {id}")
        return JSONResponse(content={'error': 'Post not found'}, status_code=404)
    except KeyError:
        logging.error("Invalid request format")
        return JSONResponse(content={'error': 'Invalid request'}, status_code=400)
    except Exception as e:
        logging.error(f"Error updating BlogPost: {str(e)}")
        return JSONResponse(content={'error': str(e)}, status_code=500)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
