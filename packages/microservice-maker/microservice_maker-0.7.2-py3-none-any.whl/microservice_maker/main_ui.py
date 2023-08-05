import os
import importlib.util
import PySimpleGUI as sg
from microservice_maker.flask_maker import FlaskMaker
from microservice_maker.django_maker import (
    DjangoMaker,
    HERE
)


class MicroServiceUI:
    def __init__(self):
        sg.theme("DarkAmber")
        layout = [
            [sg.Text('Nome do App: '), sg.Input(key="app_name")],
            [sg.Text('Porta do App: '), sg.Input(key="app_port")],
            [sg.Text("Banco de Dados Porta: "), sg.Input(key="db_port")],
            [sg.Text("Python Versão: "), sg.Input(key="python_version")],
            [sg.Text("Postgres User: "), sg.Input(key="postgres_user")],
            [sg.Text("Postgres Password: "), sg.Input(key="postgres_password")],
            [sg.Text("Postgres DB: "), sg.Input(key="postgres_db")],
            [sg.Text("Path: "), sg.FolderBrowse(key="path")],
            [sg.Text("Tipo de serviço: "), sg.Combo(['django', 'flask'], key="kind_service")],
            [sg.Button("Criar")],
            [sg.Output(size=(60,10))]
        ]

        window = sg.Window("Microservice Maker", icon=os.path.join(HERE, 'logo.py')).layout(layout)
        self.button, self.values = window.Read()

    def run(self):
        print(self.values)
        if self.values["kind_service"].lower() == "django":
            try:
                import django
                print("django aready install")
            except ImportError:
                flag = os.system("pip3 install git+https://github.com/victorhdcoelho/django.git")
                if flag == 0:
                    print("Django victorhdcoelho install success")
                else:
                    print("Django victorhdcoelho install unsuccess")
            print("Start django maker")
            dj = DjangoMaker(self.values)
            dj.run_subs_dockers()
        else:
            flk = FlaskMaker(self.values)
            flk.run()


def main():
    Window = MicroServiceUI()
    Window.run()
