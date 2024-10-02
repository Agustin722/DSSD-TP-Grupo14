import requests
from my_app.helpers.auth_helper import authenticate_bonita
from django.conf import settings

def start_bonita_process(process_definition_id, variables):
    bonita_url = getattr(settings, 'BONITA_URL', 'http://localhost:8080/bonita')
    url = f"{bonita_url}/API/bpm/case"
    
    # Autenticar y obtener cookies
    session_cookies = authenticate_bonita()

    # Formatear las variables para Bonita
    bonita_variables = format_variables(variables)

    payload = {
        "processDefinitionId": process_definition_id,
        "variables": bonita_variables
    }
    
    headers = {
        'Content-Type': 'application/json',
        'JSESSIONID': session_cookies['JSESSIONID'],
        'X-Bonita-API-Token': session_cookies["X-Bonita-API-Token"]
    }

    response = requests.post(url, json=payload, headers=headers , cookies=session_cookies)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error al iniciar el proceso en Bonita: {response.text}")

def format_variables(input_variables):
    formatted_variables = []
    
    for item in input_variables:
        for key, value in item.items():
            formatted_variables.append({"name": key, "value": value})
    
    return formatted_variables
