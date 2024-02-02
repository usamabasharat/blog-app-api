from pydantic import BaseModel


class Blog(BaseModel):
  title: str
  body: str


class showBlog(BaseModel):
  title: str

  def Config():
    orm_mode = True
