"""Page Object рабочего пространства заявок."""


class TicketsPage:
    """Предоставить семантические локаторы и действия с заявками."""

    def __init__(self, page) -> None:
        """Собрать локаторы страницы без выполнения действий."""
        self.page = page
        self.heading = page.get_by_role("heading", name="Заявки")
        self.table = page.get_by_role("table", name="Список заявок")
        self.status_message = page.get_by_role("status")
        self.create_title = page.get_by_label("Заголовок новой заявки")
        self.create_priority = page.get_by_label("Приоритет новой заявки")
        self.create_button = page.get_by_role(
            "button",
            name="Создать заявку",
            exact=True,
        )
        self.card = page.get_by_role(
            "complementary",
            name="Карточка заявки",
            exact=True,
        )

    def ticket_row(self, ticket_id: str):
        """Вернуть строку заявки по известному серверному UUID."""
        return self.page.get_by_test_id(f"ticket-{ticket_id}")

    def ticket_row_by_title(self, title: str):
        """Вернуть строку только что созданной UI-заявки по уникальному тексту."""
        link = self.page.get_by_role("button", name=title, exact=True)
        return self.page.get_by_role("row").filter(has=link)

    def create_ticket(self, title: str, priority: str = "normal") -> None:
        """Заполнить форму новой заявки и отправить её."""
        self.create_title.fill(title)
        self.create_priority.select_option(priority)
        self.create_button.click()

    def open_ticket(self, ticket_id: str) -> None:
        """Открыть карточку из точной строки таблицы."""
        self.ticket_row(ticket_id).get_by_role("button").click()

    def change_priority(self, priority: str) -> None:
        """Изменить приоритет в открытой карточке и сохранить."""
        self.card.get_by_label("Приоритет заявки").select_option(priority)
        self.card.get_by_role(
            "button",
            name="Сохранить изменения",
            exact=True,
        ).click()

    def selected_title(self):
        """Вернуть поле заголовка открытой карточки."""
        return self.card.get_by_label("Заголовок заявки")

    def selected_priority(self):
        """Вернуть select приоритета открытой карточки."""
        return self.card.get_by_label("Приоритет заявки")

    def row_priority(self, ticket_id: str):
        """Вернуть отображаемый приоритет внутри конкретной строки."""
        return self.ticket_row(ticket_id).get_by_test_id("ticket-priority")