# info.py
from datetime import datetime
import django
from termcolor import colored
from prettytable import PrettyTable
from prettytable import ALL
from drf import settings

def print_info(environment, db_config, allowed_hosts):
    # Configurar colores
    color_azul = lambda text: colored(text, 'blue')
    color_verde = lambda text: colored(text, 'green')

    # Crear la tabla con encabezados
    table = PrettyTable()
    table.field_names = ["Configuración", "Valor"]
    table.align = "l"  # Alinear a la izquierda para más compacidad
    table.max_width = 55  # Limitar el ancho de la columna de valores
    table.hrules = ALL  # Agregar bordes entre todas las filas

    # Añadir las filas
    table.add_row([color_azul('Entorno'), environment])
    table.add_row([color_azul('Versión de Django'), django.get_version()])
    table.add_row([color_azul('Fecha y Hora de Inicio'), datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
    table.add_row([color_verde('Configuración de la base de datos'), db_config])
    table.add_row([color_verde('ALLOWED_HOSTS'), allowed_hosts])

    # Obtener INSTALLED_APPS y MIDDLEWARE como cadenas
    installed_apps = "\n".join(settings.INSTALLED_APPS)
    middleware = "\n".join(settings.MIDDLEWARE)

    # Añadir las filas de INSTALLED_APPS y MIDDLEWARE
    table.add_row([color_azul('INSTALLED_APPS'), installed_apps])
    table.add_row([color_azul('MIDDLEWARE'), middleware])

    # Imprimir la tabla completa
    print(table)