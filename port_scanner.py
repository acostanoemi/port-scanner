#!/usr/bin/env python3
"""
Port scanner - v2 (rango de puertos, con hilos)

Le pasás una IP o un nombre y escanea un rango de puertos para decirte
cuales estan abiertos. Usa muchos hilos en paralelo para que sea rapido.

Como funciona: por cada puerto, intenta ABRIR una conexion TCP. Si conecta,
hay un servicio escuchando -> abierto. Es trafico comun, NO necesita sudo.

Por que hilos: escanear de a un puerto, esperando cada respuesta, tardaria
horas para miles de puertos. Lanzando muchas pruebas a la vez (hilos), el
tiempo baja a minutos. Sirve porque el scanner pasa casi todo el tiempo
ESPERANDO a la red, no calculando: mientras un hilo espera, otros trabajan.

USO ETICO Y LEGAL: escaneá SOLO tus propias maquinas o con permiso explicito.
Escanear equipos ajenos es la antesala de un ataque y es ilegal (en Argentina,
ley 26.388). Blancos para practicar con permiso:
    127.0.0.1         -> tu propia maquina
    192.168.0.1       -> tu router
    scanme.nmap.org   -> server que Nmap ofrece justo para practicar

Uso:
    python3 port_scanner.py                          # 127.0.0.1, puertos 1-1024
    python3 port_scanner.py 192.168.0.1              # tu router
    python3 port_scanner.py scanme.nmap.org --hasta 65535
    python3 port_scanner.py 192.168.0.1 --desde 1 --hasta 100 --hilos 200
"""

import socket
import argparse
from concurrent.futures import ThreadPoolExecutor

# Puertos conocidos -> servicio (para ponerle nombre a lo que encontramos)
SERVICIOS = {
    20: "FTP", 21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 123: "NTP", 143: "IMAP",
    443: "HTTPS", 465: "SMTPS", 587: "SMTP", 993: "IMAPS",
    995: "POP3S", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
    8080: "HTTP-alt", 9929: "Nping-echo", 31337: "Elite/backdoor",
}


def parsear_args():
    p = argparse.ArgumentParser(
        description="Escaner de puertos educativo con hilos: dice que servicios expone una maquina."
    )
    p.add_argument("host", nargs="?", default="127.0.0.1",
                   help="IP o nombre a escanear (default: 127.0.0.1)")
    p.add_argument("--desde", type=int, default=1,
                   help="primer puerto del rango (default: 1)")
    p.add_argument("--hasta", type=int, default=1024,
                   help="ultimo puerto del rango (default: 1024)")
    p.add_argument("--hilos", type=int, default=100,
                   help="cuantos puertos probar en paralelo (default: 100)")
    p.add_argument("-t", "--timeout", type=float, default=0.5,
                   help="segundos a esperar por puerto (default: 0.5)")
    return p.parse_args()


def escanear_puerto(ip, puerto, timeout):
    """Intenta conectar a un puerto. Devuelve True si esta abierto."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    resultado = s.connect_ex((ip, puerto))   # 0 = abierto
    s.close()
    return resultado == 0


def main():
    args = parsear_args()

    try:
        ip = socket.gethostbyname(args.host)
    except socket.gaierror:
        print(f"No pude resolver '{args.host}'. Revisá el nombre o la conexion.")
        return

    cantidad = args.hasta - args.desde + 1
    print(f"Escaneando {args.host} ({ip})")
    print(f"Puertos {args.desde}-{args.hasta} ({cantidad}), {args.hilos} hilos, timeout {args.timeout}s\n")

    # Esta funcion corre en cada hilo: prueba un puerto y devuelve el resultado.
    def tarea(puerto):
        return puerto, escanear_puerto(ip, puerto, args.timeout)

    abiertos = []
    # ThreadPoolExecutor maneja el grupo de hilos por nosotros. map() reparte
    # los puertos entre los hilos y nos devuelve los resultados EN ORDEN.
    with ThreadPoolExecutor(max_workers=args.hilos) as ejecutor:
        for puerto, esta_abierto in ejecutor.map(tarea, range(args.desde, args.hasta + 1)):
            if esta_abierto:
                servicio = SERVICIOS.get(puerto, "?")
                abiertos.append(puerto)
                print(f"  [ABIERTO] {puerto:6}  {servicio}")

    print()
    if abiertos:
        print(f"{len(abiertos)} puerto(s) abierto(s) en el rango {args.desde}-{args.hasta}.")
    else:
        print(f"Ningun puerto abierto en el rango {args.desde}-{args.hasta}.")


if __name__ == "__main__":
    main()
