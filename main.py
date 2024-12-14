from database import engine, Base, SessionLocal
from models import User, Post
from part2 import *
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Часть 3: Базовые операции с базой данных в веб-приложении
@app.post("/users/")
def create_user(username: str, email: str, password: str, db: Session = Depends(get_db)):
    new_user = User(username=username, email=email, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@app.put("/users/{user_id}")
def update_user(user_id: int, username: str = None, email: str = None, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if username:
        user.username = username
    if email:
        user.email = email
    db.commit()
    db.refresh(user)
    return user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}



@app.post("/posts/")
def create_post(title: str, content: str, user_id: int, db: Session = Depends(get_db)):
    new_post = Post(title=title, content=content, user_id=user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/")
def read_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts


@app.put("/posts/{post_id}")
def update_post(post_id: int, title: str = None, content: str = None, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if title:
        post.title = title
    if content:
        post.content = content
    db.commit()
    db.refresh(post)
    return post


@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully"}




if __name__ == "__main__":
    print("Таблицы созданы!")
    session = SessionLocal()
    
    # Часть 2: Взаимодействие с базой данных
    try:
        print("Добавление данных...")
        add_data(session)

        print("\nИзвлечение данных...")
        fetch_data(session)

        print("\nОбновление данных...")
        update_data(session)

        print("\nУдаление данных...")
        delete_data(session)
    finally:
        session.close()
        print("\nСессия закрыта.")