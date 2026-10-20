"""Page Object экрана входа Mini Tickets."""


class LoginPage:
    """Собрать локаторы и пользовательские действия формы входа."""

    def __init__(self, page) -> None:
        """Привязать объект к Playwright Page текущего теста."""
        self.page = page
        self.heading = page.get_by_role("heading", name="Вход в систему")
        self.email = page.get_by_label("Email", exact=True)
        self.password = page.get_by_label("Пароль", exact=True)
        self.submit = page.get_by_role("button", name="Войти", exact=True)

    def open(self, url: str) -> None:
        """Открыть внешний адрес клиент-серверного приложения."""
        self.page.goto(url)

    def login(self, email: str, password: str) -> None:
        """Заполнить подписанные поля и отправить форму."""
        self.email.fill(email)
        self.password.fill(password)
        self.submit.click()