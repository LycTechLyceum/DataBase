from data import db_session


def main():
    # как-то так создаётся подключение к базе данных
    db_session.global_init("db/db_proglyc.db")
    db_sess = db_session.create_session()


if __name__ == '__main__':
    main()
