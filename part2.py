from models import User, Post
from database import SessionLocal

# Часть 2: Взаимодействие с базой данных

# 4. Добавление данных
def add_data(session):
    petya = User(username='petya739', email='petya@gmail.com', password='petya678910')
    tanya = User(username='tanya35', email='tanya@mail.ru', password='tanya272727')
    session.add(petya)
    session.add(tanya)
    session.commit()
    print("Пользователи добавлены.")

    post1 = Post(title="Post About Work", content="Rabota ne wolk, rabota - work.", user_id=petya.id)
    post2 = Post(title="Post About Life", content="What a beautiful day!!!", user_id=tanya.id)
    session.add(post1)
    session.add(post2)
    session.commit()
    print("Посты добавлены.")


# 5. Извлечение данных
def fetch_data(session):
    # Извлечение всех пользователей
    users = session.query(User).all()
    print("\nПользователи:")
    for user in users:
        print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}")

    # Извлечение всех постов и их авторов
    posts = session.query(Post).join(User).all()
    print("\nПосты:")
    for post in posts:
        print(f"Post title: {post.title}, Author: {post.author.username}")

    # Извлечение постов конкретного пользователя
    user_id = 1
    user_posts = session.query(Post).filter(Post.user_id == user_id).all()
    for post in user_posts:
        print(f"User's post: {post.title}")


# 6. Обновление данных
def update_data(session):
    # Обновление email у пользователя
    user_to_update = session.query(User).filter(User.username == 'petya739').first()
    if user_to_update:
        user_to_update.email = 'new_email@ya.ru'
        session.commit()
        print(f"\nEmail пользователя {user_to_update.username} обновлен.")
    else:
        print("Пользователь не найден.")

    # Обновление content у поста
    post_to_update = session.query(Post).filter(Post.title == 'Post About Work').first()
    if post_to_update:
        if post_to_update.user_id is None:
            print(f"Ошибка: user_id у поста '{post_to_update.title}' отсутствует. Устанавливаю значение по умолчанию.")
            post_to_update.user_id = 1
        post_to_update.content = 'Updated content for the post.'
        session.commit()
        print(f"Контент поста '{post_to_update.title}' успешно обновлен.")
    else:
        print("Пост не найден.")


# 7. Удаление данных
def delete_data(session):
    # Удаление поста
    post_to_delete = session.query(Post).filter(Post.title == 'Post About Life').first()
    if post_to_delete:
        session.delete(post_to_delete)
        session.commit()
        print("\nПост удален.")

    # Удаление пользователя и всех его постов
    user_to_delete = session.query(User).filter(User.username == 'petya739').first()
    if user_to_delete:
        user_posts = session.query(Post).filter(Post.user_id == user_to_delete.id).all()
        for post in user_posts:
            session.delete(post)
        session.delete(user_to_delete)
        session.commit()
        print(f"Пользователь {user_to_delete.username} и его посты удалены.")
