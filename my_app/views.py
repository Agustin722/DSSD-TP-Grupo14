import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models.material import Material

@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        material = request.POST.get('material')
        quantity = request.POST.get('quantity')

        # Obtén el token de la cookie
        token = request.COOKIES.get('access_token')

        # Verifica que el token esté disponible
        if token is None:
            messages.error(request, 'Necesitas iniciar sesión para crear una orden.')
            return redirect('login_api')

        # Enviar solicitud a la API externa con el token en el encabezado
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.post(
            "https://dssd-api-grupo14-e0s1.onrender.com/api/create-order/",
            json={'material_name': material, 'quantity': quantity},
            headers=headers
        )
        print(response.status_code)
        print(response.text)

        if response.status_code == 201:
            messages.success(request, 'Orden creada con éxito.')
            return redirect('order_list')
        else:
            messages.error(request, 'Error al crear la orden.')
            return redirect('create_order')

    material_choices = Material.TIPO_MATERIAL_CHOICES
    return render(request, 'create_order.html', {'material_choices': material_choices})

@csrf_exempt
def reserve_order(request, order_id):
    if request.method == 'POST':
        token = request.COOKIES.get('access_token')
        
        if token is None:
            messages.error(request, 'Necesitas iniciar sesión para reservar una orden.')
            return redirect('login_api')

        headers = {'Authorization': f'Bearer {token}'}
        response = requests.post(
            f'https://dssd-api-grupo14-e0s1.onrender.com/api/orders/reserve/{order_id}/',
            headers=headers
        )

        print(response.status_code)
        print(response.text)

        if response.status_code == 200:
            messages.success(request, 'Orden reservada con éxito.')
        else:
            messages.error(request, 'Error al reservar la orden.')

    return redirect('order_list')

@csrf_exempt
def deliver_order(request, order_id):
    if request.method == 'POST':
        token = request.COOKIES.get('access_token')
        
        if token is None:
            messages.error(request, 'Necesitas iniciar sesión para entregar una orden.')
            return redirect('login_api')

        headers = {'Authorization': f'Bearer {token}'}
        response = requests.post(
            f'https://dssd-api-grupo14-e0s1.onrender.com/api/deliver-order/{order_id}/',
            headers=headers
        )

        print(response.status_code)
        print(response.text)

        if response.status_code == 200:
            messages.success(request, 'Orden entregada con éxito.')
        else:
            messages.error(request, 'Error al entregar la orden.')

    return redirect('order_list')
@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Enviar solicitud a la API externa
        response = requests.post(
            'https://dssd-api-grupo14-e0s1.onrender.com/register/',
            json={'username': username, 'email': email, 'password': password}
        )

        if response.status_code == 201:
            messages.success(request, 'Usuario registrado con éxito.')
            return redirect('login_api')  # Redirige a la página de login o donde desees
        else:
            messages.error(request, 'Error al registrar el usuario.')
            return redirect('register_user')

    return render(request, 'register_user.html')


def login_api(request):
    if request.method == 'POST':
        # Obtén los datos de inicio de sesión del formulario
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Define la URL de inicio de sesión de la API
        api_login_url = f"https://dssd-api-grupo14-e0s1.onrender.com/api/token/"  # Reemplaza con la URL de tu API

        # Enviar una solicitud de autenticación a la API para obtener el token JWT
        response = requests.post(api_login_url, data={'username': username, 'password': password})


        print(response.status_code)
        print(response.text)
        # Si la autenticación es exitosa, la API devolverá el token de acceso
        if response.status_code == 200:
            tokens = response.json()  # {'access': 'access_token_value', 'refresh': 'refresh_token_value'}
            access_token = tokens['access']
            refresh_token = tokens['refresh']

            # Crear una respuesta de redirección y almacenar los tokens en las cookies
            response = redirect('create_order')  # Redirige a la página deseada después del login
            response.set_cookie('access_token', access_token)
            response.set_cookie('refresh_token', refresh_token, httponly=True)

            return response
        else:
            # En caso de error, muestra un mensaje de error
            error_message = "Credenciales incorrectas. Inténtalo de nuevo."
            return render(request, 'login-api.html', {'error': error_message})

    return render(request, 'login-api.html')  # Muestra el formulario de inicio de sesión

@csrf_exempt
def order_list(request):
    # Obtiene el token de la cookie
    token = request.COOKIES.get('access_token')
    
    # Verifica que el token esté disponible
    if token is None:
        messages.error(request, 'Necesitas iniciar sesión para ver las órdenes.')
        return redirect('login_api')
    
    # Define la URL de la API y el encabezado de autorización
    api_url = "https://dssd-api-grupo14-e0s1.onrender.com/api/orders/"
    headers = {'Authorization': f'Bearer {token}'}
    
    # Realiza la solicitud GET a la API para obtener la lista de órdenes
    response = requests.get(api_url, headers=headers)
    
    # Verifica el estado de la respuesta
    if response.status_code == 200:
        orders = response.json()  # Obtén la lista de órdenes en formato JSON
    else:
        messages.error(request, 'Error al obtener la lista de órdenes.')
        orders = []  # Si hay error, inicializa una lista vacía
    
    # Renderiza el template con la lista de órdenes
    return render(request, 'order_list.html', {'object_list': orders})

@csrf_exempt
def material_list(request):
    # Obtiene el token de la cookie
    token = request.COOKIES.get('access_token')

    # Verifica que el token esté disponible
    if token is None:
        messages.error(request, 'Necesitas iniciar sesión para ver los materiales.')
        return redirect('login_api')

    # Define la URL de la API y el encabezado de autorización
    api_url = "https://dssd-api-grupo14-e0s1.onrender.com/api/materials/"
    headers = {'Authorization': f'Bearer {token}'}

    # Realiza la solicitud GET a la API para obtener la lista de materiales
    response = requests.get(api_url, headers=headers)

    # Verifica el estado de la respuesta
    if response.status_code == 200:
        materials = response.json()  # Obtén la lista de materiales en formato JSON
    else:
        messages.error(request, 'Error al obtener la lista de materiales.')
        materials = []  # Si hay error, inicializa una lista vacía

    # Renderiza el template con la lista de materiales
    return render(request, 'material_list.html', {'object_list': materials})