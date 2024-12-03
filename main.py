import requests

URL = "http://127.0.0.1:8000"


class BlogManagement:
    def __init__(self, login, password):
        self.__login = login
        self.__password = password
        self.__token = self.get_token()

    # Задание Объедините следующие методы сервиса “Django Blog API” в класс BlogManagement(
    # https://github.com/keyayeten/test_api) описав работу со сторонним апи через удобный код:

    # Регистрация нового пользователя: Напишите скрипт, который использует requests для отправки POST-запроса с данными
    # для регистрации нового пользователя. Обработайте возможные ошибки и получите успешный ответ с подтверждением
    # регистрации.
    @staticmethod
    def register_user(username, password, re_password, mail):
        posts_data = {
            "email": mail,
            "username": username,
            "password": password,
            "re_password": re_password
        }
        request_headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }

        endpoint = "/auth/users/"

        response = requests.post(
            url=URL + endpoint,
            headers=request_headers,
            json=posts_data)
        return response.json()

    # Авторизация пользователя с использованием JWT: Реализуйте запрос для отправки POST-запроса с логином и паролем
    # пользователя, получив JWT-токен в ответе. Используйте этот токен для дальнейшей авторизации при отправке
    # запросов к защищённым эндпоинтам API.
    def get_token(self):
        posts_data = {
            "username": self.__login,
            "password": self.__password
        }
        request_headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }

        response = requests.post(
            url=URL + "/auth/jwt/create/",
            headers=request_headers,
            json=posts_data)
        token = dict(response.json())
        return token.get("access")

    # Получение списка всех постов: Создайте скрипт, который выполняет GET-запрос к API для получения списка всех
    # постов. Для этого потребуется использовать авторизационный заголовок с JWT-токеном.
    @staticmethod
    def get_posts_list():
        endpoint = "/api/posts/"

        response = requests.get(URL + endpoint)
        return response.json()

    # Создание нового поста: Напишите функцию, которая отправляет POST-запрос для создания нового поста. Необходимо
    # передавать данные поста (заголовок, содержание и т. д.) и авторизационный токен в заголовках.
    def create_new_post(self, title: str, content: str):
        posts_data = {
            "title": title,
            "content": content
        }
        request_headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            'authorization': f"Bearer {self.__token}"
        }
        endpoint = "/api/posts/"

        response = requests.post(
            url=URL + endpoint,
            json=posts_data,
            headers=request_headers)
        return response.json()

    # Добавление комментария к посту: Разработайте скрипт для добавления комментария к существующему посту через
    # POST-запрос Включите авторизационные данные и текст комментария в запрос.
    def create_new_comment(self, post_id: int, comment: str):
        posts_data = {
            "post": post_id,
            "text": comment
        }
        request_headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            'authorization': f"Bearer {self.__token}"
        }
        endpoint = "/api/comments/"

        response = requests.post(
            url=URL + endpoint,
            json=posts_data,
            headers=request_headers)
        return response.json()

    # Получение комментариев к посту: Реализуйте функцию, которая делает GET-запрос на получение всех комментариев для
    # конкретного поста, передавая идентификатор поста в URL и авторизационный токен в заголовке.

    def get_comments_id(self, post_id: int):
        params_data = {
            "id": post_id
        }
        request_headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            'authorization': f"Bearer {self.__token}"
        }
        endpoint = f"/api/comments/{post_id}/"
        response = requests.get(
            url=URL + endpoint,
            params=params_data,
            headers=request_headers)
        return response.json()

    # Обновление поста: Напишите запрос для PUT-метода, который позволяет обновить информацию о посте (например,
    # заголовок и текст), отправив обновленные данные в теле запроса, с токеном авторизации.
    def update_post(self, post_id: int, title: str, content: str):
        posts_data = {
            "title": title,
            "content": content
        }
        request_headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            'authorization': f"Bearer {self.__token}"
        }
        endpoint = f"/api/posts/{post_id}/"

        response = requests.put(
            url=URL + endpoint,
            json=posts_data,
            headers=request_headers)
        return response.json()

    # Удаление комментария или поста: Реализуйте DELETE-запросы для удаления поста или комментария по их ID.
    # Убедитесь, что токен авторизации передан в заголовке запроса.
    def delete_post(self, post_id: int):
        request_headers = {
            "accept": "application/json",
            'authorization': f"Bearer {self.__token}"
        }
        endpoint = f"/api/posts/{post_id}/"

        response = requests.delete(
            url=URL + endpoint,
            headers=request_headers)
        return response.status_code

    def delete_comment(self, comment_id: int):
        request_headers = {
            "accept": "application/json",
            'authorization': f"Bearer {self.__token}"
        }
        endpoint = f"/api/comments/{comment_id}/"

        response = requests.delete(
            url=URL + endpoint,
            headers=request_headers)
        return response.status_code


if __name__ == "__main__":
    user = BlogManagement("banderos", "45MhxNT|")
    manager = BlogManagement("tony", "tony")
    user1 = BlogManagement.register_user("Alex1", "akjshkjhfdfdsf", "akjshkjhfdfdsf", "asdasd@mail.ru")
    print(user1)
    new_post = dict(user.create_new_post("Новый пост", "Ляяя, какова красота"))
    print(new_post)
    new_comment = dict(user.create_new_comment(new_post["id"], "Первый нах!"))
    print(new_comment)
    print(user.get_comments_id(new_comment["id"]))
    print(user.update_post(new_post["id"], "Обновленный заголовок", "Это тоже обновили"))
    print(user.delete_comment(new_comment["id"]))
    print(user.delete_post(new_post["id"]))
    print(manager.get_posts_list())
