import os
from datetime import datetime
import json
import getpass
import random
import string
import socket
import requests


def make_log_file(robot_name: str, schedule_value: str, start_date: datetime, status: str, error_value: str = None, detail_value: str = None):

    if status.upper() in ['WARNING', 'FAIL', 'SUCCESS']:
        data = {
            "NAME": robot_name,
            "LOCAL_PATH": os.getcwd(),
            "USER_NAME": getpass.getuser(),
            "SERVER": socket.getfqdn(),
            "SCHEDULE": schedule_value,
            "START_DATE": start_date.isoformat(),
            "END_DATE": datetime.utcnow().isoformat(),
            "STATUS": status.upper(),
            "ERROR":  error_value,
            "MORE_INFORMATION":  detail_value
        }
        return data

    else:
        print("[ERROR] Unexpected status ('WARNING', 'FAIL', 'SUCCESS')")
        return


def save_log(PATH_LOG: str, robot_name: str, schedule_value: str, start_date: datetime, status: str, error_value: str = None, detail_value: str = None):
    """
    Test

    Args:
        PATH_LOG (str): Caminho para a diretorio de processamento de logs json
        robot_name (str): Codigo do robo (ex: DGA-100)
        schedule_value (str): Agendamento do robo em formato padrao cron
        start_date (datetime): Datahora do inicio do processamento do dado
        status (str): Status final do processamento do dado
        error_value (str, optional): Mensagem de erro quando existente. Padrao e' None.
        detail_value (str, optional): Informacoes adicionais ao dado quando necessario. Padrao e' None.
    """

    if status.upper() in ['WARNING', 'FAIL', 'SUCCESS']:
        data = make_log_file(
            robot_name, schedule_value, start_date,
            status, error_value, detail_value
        )
        code_name = ''.join(random.choice(
            string.ascii_lowercase + string.digits) for _ in range(15)
        )

        name_file = f"{PATH_LOG}/{data['NAME']}_{code_name}.json"

        with open(name_file, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data))
        print(f"[INFO] Document created: {name_file}")

    else:
        print("[ERROR] Unexpected status ('WARNING', 'FAIL', 'SUCCESS')")

    return


def post_log(URL: str, robot_name: str, schedule_value: str, start_date: datetime, status: str, error_value: str = None, detail_value: str = None):
    """
        Args:
        url (str): url do webservice (ex: http://xxxxxxx.br:9999/)
        robot_name (str): Codigo do robo (ex: DGA-100)
        schedule_value (str): Agendamento do robo em formato padrao cron
        start_date (datetime): Datahora do inicio do processamento do dado
        status (str): Status final do processamento do dado
        error (str, optional): Mensagem de erro quando existente. Padrao e' None.
        more_information (str, optional): Informacoes adicionais ao dado quando necessario. Padrao e' None.
    """

    if not URL:
        print("[ERROR] URL was not provided")
        return

    if status.upper() not in ['WARNING', 'FAIL', 'SUCCESS']:
        print("[ERROR] Unexpected status ('WARNING', 'FAIL', 'SUCCESS')")
        return

    payload = json.dumps(make_log_file(
        robot_name, schedule_value, start_date,
        status, error_value, detail_value
    ))

    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", URL, headers=headers, data=payload)

    return response
