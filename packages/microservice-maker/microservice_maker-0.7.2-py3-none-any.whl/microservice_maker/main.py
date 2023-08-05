from microservice_maker.django_maker import DjangoMaker


if __name__ == "__main__":
    user_args = {}
    user_args["app_name"] = input("Nome do app: ")
    user_args["app_port"] = input("Port do app: ")
    user_args["db_port"] = input("Port db: ")
    user_args["python_version"] = input("Python version: ")
    user_args["postgres_user"] = input("Postgres user: ")
    user_args["postgres_password"] = input("Postgres password: ")
    user_args["postgres_db"] = input("Postgres db: ")
    user_args["path"] = input("Project path: ")

    dj = DjangoMaker(user_args)
    dj.run_subs_dockers()
