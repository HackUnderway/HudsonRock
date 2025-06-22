import requests
import os
from colorama import init, Fore, Style

os.system("printf '\033]2;Hudson Rock v1.0 👨🏽‍💻\a'")

init(autoreset=True)

def mostrar_banner():
    banner = f"""
{Fore.RED}▗▖ ▗▖█  ▐▌▐▌ ▄▄▄  ▄▄▄  ▄▄▄▄      ▗▄▄▖  ▄▄▄  ▗▞▀▘█  ▄ 
{Fore.RED}▐▌ ▐▌▀▄▄▞▘▐▌▀▄▄  █   █ █   █     ▐▌ ▐▌█   █ ▝▚▄▖█▄▀  
{Fore.RED}▐▛▀▜▌  ▗▞▀▜▌▄▄▄▀ ▀▄▄▄▀ █   █     ▐▛▀▚▖▀▄▄▄▀     █ ▀▄ 
{Fore.RED}▐▌ ▐▌  ▝▚▄▟▌                     ▐▌ ▐▌          █  █
{Style.RESET_ALL}
{Fore.WHITE}{Style.BRIGHT}== 🔍 Infostealer Intelligence Free Integration 👁️ =={Style.RESET_ALL}
"""
    print(banner)
    spaces = 18
    print(f"{' ' * spaces}{Fore.WHITE}{Style.BRIGHT}By: HackUnderway{Style.RESET_ALL}")

def consultar_api(tipo, valor):
    base_urls = {
        'email': f'https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-email?email={valor}',
        'username': f'https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-username?username={valor}',
        'domain': f'https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-domain?domain={valor}',
        'urls-by-domain': f'https://cavalier.hudsonrock.com/api/json/v2/osint-tools/urls-by-domain?domain={valor}',
        'ip': f'https://cavalier.hudsonrock.com/api/json/v2/osint-tools/search-by-ip?ip={valor}'
    }

    url = base_urls.get(tipo)
    if not url:
        print(Fore.RED + "Tipo de consulta inválido.")
        return

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        print(Fore.CYAN + "\n--- Resultados ---")
        
        # Mensajes personalizados para cada tipo de búsqueda
        mensajes_no_resultados = {
            'email': f"No se encontraron equipos infectados asociados al email: {valor}",
            'username': f"No se encontraron equipos infectados asociados al usuario: {valor}",
            'domain': f"No se encontraron resultados para el dominio: {valor}",
            'urls-by-domain': f"No se encontraron URLs comprometidas para el dominio: {valor}",
            'ip': f"No se encontraron equipos infectados asociados a la IP: {valor}"
        }
        
        # Verificar si hay resultados
        if not data or data.get('stealers') == [] or (isinstance(data, dict) and data.get('total_user_services', 0) == 0):
            print(Fore.YELLOW + mensajes_no_resultados[tipo])
            return
            
        print_formato_plano(data)

    except requests.exceptions.RequestException as e:
        print(Fore.RED + "Error en la petición:", e)

def print_formato_plano(data, indent=0, in_stealers=False):
    # Si los datos están vacíos, no imprimir nada
    if not data or data == {} or data == []:
        return
        
    # Campos a excluir (incluimos 'message' para no mostrar el mensaje en inglés)
    excluded_fields = {'message', 'logo', 'is_shopify'}
    
    # Resto de la función permanece igual...
    important_fields = {
        'total_corporate_services', 'total_user_services', 'date_compromised',
        'computer_name', 'operating_system', 'malware_path', 'ip',
        'top_passwords', 'top_logins', 'stealer_family', 'total',
        'totalStealers', 'employees', 'users', 'third_parties', 'totalUrls',
        'url', 'type', 'occurrence'
    }
    
    if isinstance(data, dict):
        if not in_stealers and 'stealers' in data:
            print_formato_plano(data['stealers'], indent, True)
            return
            
        for key, value in data.items():
            if key in excluded_fields:
                continue
                
            if key in important_fields:
                if key == 'top_passwords' or key == 'top_logins':
                    print("  " * indent + f"{Fore.RED}{key.upper()}:{Style.RESET_ALL}")
                else:
                    print("  " * indent + f"{Fore.YELLOW}{key}:{Style.RESET_ALL}")
                    
                print_formato_plano(value, indent + 1, in_stealers)
            else:
                print_formato_plano(value, indent, in_stealers)
                
    elif isinstance(data, list):
        if in_stealers:
            for i, item in enumerate(data, 1):
                print("  " * indent + f"{Fore.GREEN}--- INFOSTEALER {i} ---{Style.RESET_ALL}")
                print_formato_plano(item, indent + 1, True)
        else:
            for item in data:
                print_formato_plano(item, indent, in_stealers)
    else:
        if data is not None and str(data).strip() != '' and str(data) != 'Not Found':
            print("  " * indent + str(data))

def menu():
    print(f"\n{Fore.RED}1{Style.RESET_ALL} - Consultar email")
    print(f"{Fore.RED}2{Style.RESET_ALL} - Consultar username")
    print(f"{Fore.RED}3{Style.RESET_ALL} - Consultar dominio")
    print(f"{Fore.RED}4{Style.RESET_ALL} - Consultar URLs afectadas por dominio")
    print(f"{Fore.RED}5{Style.RESET_ALL} - Consultar dirección IP")
    print(f"{Fore.RED}0{Style.RESET_ALL} - Salir")

    opcion = input(Fore.CYAN + "\nSelecciona una opción: ").strip()

    if opcion == '1':
        valor = input("Ingresa el email: ").strip()
        consultar_api('email', valor)
    elif opcion == '2':
        valor = input("Ingresa el username: ").strip()
        consultar_api('username', valor)
    elif opcion == '3':
        valor = input("Ingresa el dominio: ").strip()
        consultar_api('domain', valor)
    elif opcion == '4':
        valor = input("Ingresa el dominio: ").strip()
        consultar_api('urls-by-domain', valor)
    elif opcion == '5':
        valor = input("Ingresa la dirección IP: ").strip()
        consultar_api('ip', valor)
    elif opcion == '0':
        print(Fore.GREEN + "¡Hasta luego!")
        exit()
    else:
        print(Fore.RED + "Opción inválida. Intenta de nuevo.")

if __name__ == "__main__":
    mostrar_banner()
    while True:
        menu()
