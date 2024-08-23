from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class PostBase(BaseModel):
    title: str
    content: str
    user_id: int

class UserBase(BaseModel):
    username: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: Session = Depends(get_db)):
    db_user = models.User(**user.dict())
    # db_user.username = user.username
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

    
    
    
@app.get("/users/" , status_code=status.HTTP_200_OK) 
async def read_user(db:Session = Depends(get_db)):
    return db.query(models.User).all()




@app.get("/users/{user_id}",status_code=status.HTTP_200_OK)
async def get_byId(user_id : int , db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code= 404,
            detail= f"ID {user_id} : Does not exist"
        )
        
    return user.username
        
    
    
     

@app.put("/{user_id}")
async def update_user(user_id:int , user:UserBase , db:Session = Depends(get_db)):
    
    user_model = db.query(models.User).filter(models.User.id == user_id).first()
    if user_model is None:
        raise HTTPException(
            status_code= 404,
            detail= f"ID {user_id} : Does not exist"
        )
    
    user_model.username = user.username
    
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    
    return user
    
    


@app.delete("/{user_id}",status_code=status.HTTP_200_OK)
async def delete_user(user_id : int , db:Session = Depends(get_db)):
    user_model = db.query(models.User).filter(models.User.id ==user_id).first()
    
    if user_model is None:
        raise HTTPException(
            status_code= 404,
            detail= f"ID {user_id} : Does not exist"
        )
    
    
    db.query(models.User).filter(models.User.id == user_id).delete()
    
    db.commit()
    
    return f"Silme işlemi başarılı.."



    
@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def post_user(post: PostBase, db: Session = Depends(get_db)):
    # db_post = models.Post()
    # db_post.title = post.title
    # db_post.content = post.content
    # db_post.user_id = post.user_id  
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post



