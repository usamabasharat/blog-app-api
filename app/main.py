from fastapi import FastAPI, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from . import models, schemas

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


@app.post('/blogs', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
  new_blog = models.Blog(title=request.title, body=request.body)
  db.add(new_blog)
  db.commit()
  db.refresh(new_blog)
  return new_blog


@app.get('/blogs', status_code=status.HTTP_200_OK)
def show_all(db: Session = Depends(get_db)):
  blogs = db.query(models.Blog).order_by('id').all()
  return blogs


@app.get('/blogs/{id}', status_code=status.HTTP_200_OK)
def show(id: int, db: Session = Depends(get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id).first()

  if not blog:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Blog with id {id} not found!')
  return blog


@app.put('/blogs/{id}', status_code=status.HTTP_202_ACCEPTED)
def change(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id)

  if not blog.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Blog with id {id} not found!')

  blog.update({"title": request.title, "body": request.body})
  db.commit()
  return 'updated'


@app.delete('/blogs/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id ==
                                      id)
  if not blog.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Blog with id {id} not found!')

  blog.delete(synchronize_session=False)
  db.commit()

  return 'Deleted'
