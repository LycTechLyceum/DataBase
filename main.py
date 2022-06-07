from werkzeug.security import generate_password_hash

from data import db_session
from data.events import Event
from data.organizations import Organization
from data.personas import Persona
from data.positions import Position

from users.sqlalchemy_repo import SQLAlchemyRepo



def main():
    # как-то так создаётся подключение к базе данных
    db_session.global_init("db/db_proglyc.db")
    db_sess = db_session.create_session()

    # далее взаимодействие с бд идёт вне  класса sql_repo, чего делать нельзя
    pos = Position()
    pos.name = "куратор"
    pos2 = Position()
    pos2.name = "заказчик"
    pos3 = Position()
    pos3.name = "программист обычный"
    db_sess.add(pos)
    db_sess.add(pos2)
    db_sess.add(pos3)
    db_sess.commit()

    print("добавлены пару должностей: ", pos.name, pos2.name, pos3.name)


    per = Persona()
    per.name = "тима"
    per.surname = "kopijohu"
    per.grade = "10b6"
    per.login = "okiu"
    per.set_password("opkijoui")
    per.id_position = 1

    per1 = Persona()
    per1.name = "мотя"
    per1.surname = "kopijohu"
    per1.grade = "10b6"
    per1.login = "okiuр"
    per1.set_password("opkijoui")
    per1.id_position = 2

    per2 = Persona()
    per2.name = "петя"
    per2.surname = "kopijohu"
    per2.grade = "10b6"
    per2.login = "okiuрро"
    per2.set_password("opkijoui")
    per2.id_position = 3

    org = Organization()
    org.name = "Организация"

    db_sess.add(per)
    db_sess.add(per1)
    db_sess.add(per2)
    db_sess.add(org)
    db_sess.commit()

    print("добавлены  пару пользователей: ", per.surname, per1.position.name, per2.login)
    print("а вот имена всех людей, которые работают на первой должности")
    for persona in pos.personas:
        print(persona.name)

    event = Event()
    event.name = "name"
    event.id_org = 1
    event.id_curator = 1
    event.id_customer = 2

    db_sess.add(event)
    db_sess.commit()

    print("добавлено событие {}".format(event.name), "его куратор: {}".format(event.curator.name),
          "а организация, от которой поступил заказ: {}".format(event.organization.name))

    repo = SQLAlchemyRepo("db/db_proglyc.db")
    # проверяем работу написанного класса SQLAlchemyRepo
    # в будущем будет рассмотрен  вопрос возвращения методами репозитория созданных объектов
    print(repo.set_customer(per1, event))  # добавляем заказчика на проект
    print(repo.set_visitor(per2, event))  # добавляем посетителя проекта
    print(repo.set_curator(per, event))  # добавляем куратора на проект
    print(repo.set_customer(per1, event))  # добавляем повторяющегося заказчика
    print(repo.add_organization(  # добавляем организацию
        org_name="шргп"
    ))
    print(repo.add_organization(  # добавляем организацию с неправльным именем
        org_name=0
    ))
    print(repo.add_event(  # добавляем событие
        event_name="name event",
        org=org,
        per_cur=per1,
        per_cus=per
    ))
    print(repo.add_user(  # добавляем пользователя
        name="нууу",
        surname="pkojhi",
        grade="10i4",
        login="ipuh",
        password="iubhfv",
        position=pos
    ))

    # и всё остальное
    print(repo.add_position("position"))
    print(repo.add_position("куратор"))
    print(repo.add_organization("зшощгш"))
    print(repo.add_organization("jihbug"))
    print(repo.set_visitor(
        user=per1,
        event=event
    ))


if __name__ == '__main__':
    main()
