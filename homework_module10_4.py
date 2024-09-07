import threading
import time
import random
from queue import Queue

# Класс, представляющий стол в кафе
class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None

# Класс, представляющий гостя, наследуется от потока
class Guest(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        # Имитируем процесс принятия пищи
        time_to_eat = random.randint(3, 10)
        time.sleep(time_to_eat)

# Класс, представляющий кафе
class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = list(tables)

    def guest_arrival(self, *guests):
        for guest in guests:
            # Ищем свободный стол
            table = next((t for t in self.tables if t.guest is None), None)
            if table is not None:
                # Сажаем гостя за стол
                table.guest = guest
                guest.start()
                print(f"{guest.name} сел(-а) за стол номер {table.number}")
            else:
                # Если нет свободных столов, ставим гостя в очередь
                self.queue.put(guest)
                print(f"{guest.name} в очереди")

    def discuss_guests(self):
        while not self.queue.empty() or any(t.guest is not None for t in self.tables):
            for table in self.tables:
                if table.guest is not None and not table.guest.is_alive():
                    print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")
                    print(f"Стол номер {table.number} свободен")
                    table.guest = None

                    # Если очередь не пуста, сажаем следующего гостя за стол
                    if not self.queue.empty():
                        next_guest = self.queue.get()
                        table.guest = next_guest
                        next_guest.start()
                        print(f"{next_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")

# Пример использования
if __name__ == "__main__":
    # Создание столов
    tables = [Table(number) for number in range(1, 6)]

    # Имена гостей
    guests_names = [
        'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
        'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
    ]

    # Создание гостей
    guests = [Guest(name) for name in guests_names]

    # Заполнение кафе столами
    cafe = Cafe(*tables)

    # Приём гостей
    cafe.guest_arrival(*guests)

    # Обслуживание гостей
    cafe.discuss_guests()
