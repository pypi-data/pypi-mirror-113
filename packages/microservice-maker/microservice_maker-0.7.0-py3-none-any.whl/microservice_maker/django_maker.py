import os
import threading
from tqdm import tqdm


HERE = os.path.dirname(os.path.abspath(__file__))


class DjangoMaker:
    def __init__(self, user_args):
        self.app_name = user_args["app_name"]
        self.app_port = user_args["app_port"]
        self.db_port = user_args["db_port"]
        self.python_version = user_args["python_version"]
        self.postgres_user = user_args["postgres_user"]
        self.postgres_password = user_args["postgres_password"]
        self.postgres_db = user_args["postgres_db"]
        self.project_path = os.path.abspath(user_args["path"])
        self.subs_results = {}

    def subs_docker_compose(self, path):
        with open(path, "r") as f:
            docker = f.read()

        docker = docker.replace("[app_name]", self.app_name)
        docker = docker.replace("[db_port]", self.db_port)
        docker = docker.replace("[app_port]", self.app_port)
        self.subs_results["compose"] = docker

    def subs_docker_entrypoint(self, path):
        with open(path, "r") as f:
            docker = f.read()
        self.subs_results["entry"] = docker

    def subs_env_file(self, path):
        with open(path, "r") as f:
            docker = f.read()
        docker = docker.replace("[postgres_user]", self.postgres_user)
        docker = docker.replace("[postgres_password]", self.postgres_password)
        docker = docker.replace("[postgres_db]", self.postgres_db)
        docker = docker.replace("[postgres_port]", self.db_port)
        self.subs_results["env"] = docker

    def subs_docker_file(self, path):
        with open(path, "r") as f:
            docker = f.read()
        docker = docker.replace("[app_name]", self.app_name)
        docker = docker.replace("[python_version]", self.python_version)
        self.subs_results["docker"] = docker

    def create_project(self):
        project = os.path.join(self.project_path, self.app_name)
        os.mkdir(project)
        os.system("django-admin startproject {} {}".format(self.app_name,
                                                           project))
        with open(os.path.join(HERE, '5_req.py'), 'r') as f:
            req = f.read()
        with open(os.path.join(project, "requirements.txt"), 'w') as f:
            f.write(req)

    def mv_all_dockers(self):
        with open(os.path.join(self.project_path, "docker-compose.yml"),
                  "w") as f:
            f.write(self.subs_results["compose"])

        with open(os.path.join(self.project_path, ".env"), "w") as f:
            f.write(self.subs_results["env"])

        project = os.path.join(self.project_path, self.app_name)

        with open(os.path.join(project, "Dockerfile"), "w") as f:
            f.write(self.subs_results["docker"])

        with open(os.path.join(project, "docker-entrypoint.sh"), "w") as f:
            f.write(self.subs_results["entry"])

    def run_subs_dockers(self):
        functions = [self.subs_docker_compose,
                     self.subs_docker_entrypoint,
                     self.subs_env_file,
                     self.subs_docker_file]
        paths = []
        print("Get all paths")
        for path, dirs, files in os.walk(HERE):
            for f in tqdm(files):
                if f in ["1_docker-compose.yml.py",
                         "2_docker-entrypoint.sh.py",
                         "4_Dockerfile.py",
                         "3_env.py"]:
                    full_path = os.path.join(path, f)
                    print(full_path)
                    paths.append(full_path)

        paths.sort()
        print(paths)
        print("Threading subs files")
        thrs = []
        idx = 0
        for path, function in zip(paths, functions):
            thrs.append(threading.Thread(target=function, args=(path,)))
            thrs[idx].start()
            idx += 1
        print("Join threads")
        for th in thrs:
            th.join()

        self.create_project()
        self.mv_all_dockers()
