class Goal:
    def __init__(self, name, target, category):
        self.name = name
        self.target = target
        self.balance = 0
        self.category = category
        self.status = "в процессе"

    def add_money(self, amount):
        if self.balance + amount > self.target:
            print("Нельзя превысить цель!")
        else:
            self.balance += amount
            print("Баланс пополнен!")

        if self.balance >= self.target:
            self.status = "выполнена"

    def show_progress(self):
        percent = (self.balance / self.target) * 100
        print(f"{self.name}: {percent:.2f}% выполнено")

goals = []

while True:
    print("\n1. Добавить цель")
    print("2. Пополнить баланс")
    print("3. Показать прогресс")
    print("4. Удалить цель")
    print("5. Выход")

    choice = input("Выбери действие: ")

    if choice == "1":
        name = input("Название цели: ")
        target = float(input("Сколько нужно накопить: "))
        category = input("Категория: ")
        goals.append(Goal(name, target, category))

    elif choice == "2":
        name = input("Название цели: ")
        for g in goals:
            if g.name == name:
                amount = float(input("Сумма: "))
                g.add_money(amount)

    elif choice == "3":
        for g in goals:
            g.show_progress()

    elif choice == "4":
        name = input("Название цели: ")
        goals = [g for g in goals if g.name != name]

    elif choice == "5":
        break
