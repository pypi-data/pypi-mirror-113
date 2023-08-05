import os


FLASK_TEMPLATE = "https://gitlab.com/victorhdcoelho/flask-template-project.git"


class FlaskMaker:
    def __init__(self, user_args):
        self.user_args = user_args
        self.user_args["path"] = os.path.abspath(self.user_args["path"])

    def clone_flask_repo(self):
        os.system("git clone {} {}".format(
                FLASK_TEMPLATE,
                self.user_args["path"]
            )
        )
        os.system("rm -rf {}".format(
                    os.path.join(self.user_args["path"],
                    ".git"
                )
            )
        )

    def subs_env(self):
        path = os.path.join(self.user_args["path"], ".env")
        with open(path, 'r') as f:
            env_file = f.read()

        env_file = env_file.replace("[APP_NAME]", self.user_args["app_name"])
        env_file = env_file.replace("[FLASK_EXTERNAL_PORT]", self.user_args["app_port"])
        env_file = env_file.replace("[FLASK_INTERNAL_PORT]", self.user_args["app_port"])
        env_file = env_file.replace("[DB_PORT]", self.user_args["db_port"])
        env_file = env_file.replace("[DEBUG]", "True")
        env_file = env_file.replace("[APP_HOST]", "0.0.0.0")
        env_file = env_file.replace("[POSTGRES_USER]", self.user_args["postgres_user"])
        env_file = env_file.replace("[POSTGRES_PASSWORD]", self.user_args["postgres_password"])
        env_file = env_file.replace("[POSTGRES_DB]", self.user_args["postgres_db"])
        env_file = env_file.replace("[POSTGRES_HOST]", "database")

        with open(path, "w") as f:
            f.write(env_file)


    def run(self):
        self.clone_flask_repo()
        self.subs_env()
