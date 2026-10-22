#!/usr/bin/env python3
"""
Port scanner - v1 (puertos conocidos)

Le pasás una IP o un nombre y te dice que puertos conocidos tiene abiertos,
o sea que servicios esta exponiendo esa maquina.

Como funciona: por cada puerto, intenta ABRIR una conexion normal (TCP).
Si conecta, hay un servicio escuchando -> puerto abierto. Si la rechazan
o no contesta -> cerrado. Es trafico comun, por eso NO necesita sudo.

USO ETICO Y LEGAL: escaneá SOLO tus propias maquinas o con permiso explicito.
Escanear equipos ajenos es la antesala de un ataque y es ilegal (en Argentina,
ley 26.388). Blancos para practicar con permiso:
    127.0.0.1         -> tu propia maquina
    192.168.0.1       -> tu router
    scanme.nmap.org   -> server que Nmap ofrece justo para practicar

Uso:
    python3 port_scanner.py                  # escanea 127.0.0.1
    python3 port_scanner.py 192.168.0.1      # escanea tu router
    python3 port_scanner.py scanme.nmap.org -t 1
"""

import socket
import argparse

# Puertos conocidos -> servicio (la misma tabla del packet-sniffer)
SERVICIOS = {
    20: "FTP", 21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 123: "NTP", 143: "IMAP",
    443: "HTTPS", 465: "SMTPS", 587: "SMTP", 993: "IMAPS",
    995: "POP3S", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
    8080: "HTTP-alt",
}


def parsear_args():
    p = argparse.ArgumentParser(
        description="Escaner de puertos educativo: dice que servicios expone una maquina."
    )
    p.add_argument("host", nargs="?", default="127.0.0.1",
                   help="IP o nombre a escanear (default: 127.0.0.1)")
    p.add_argument("-t", "--timeout", type=float, default=0.5,
                   help="segundos a esperar por puerto antes de darlo por cerrado (default: 0.5)")
    return p.parse_args()


def escanear_puerto(ip, puerto, timeout):
    """Intenta conectar a un puerto. Devuelve True si esta abierto."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    # connect_ex devuelve 0 si conecto (abierto), o un codigo de error si no.
    # Usamos esta en vez de connect() porque no lanza excepcion: mas limpio.
    resultado = s.connect_ex((ip, puerto))
    s.close()
    return resultado == 0


def main():
    args = parsear_args()

    # Si nos dieron un nombre (scanme.nmap.org), lo pasamos a IP
    try:
        ip = socket.gethostbyname(args.host)
    except socket.gaierror:
        print(f"No pude resolver '{args.host}'. Revisá el nombre o la conexion.")
        return

    print(f"Escaneando {args.host} ({ip})")
    print(f"Puertos conocidos, timeout {args.timeout}s\n")

    abiertos = []
    for puerto in sorted(SERVICIOS):
        if escanear_puerto(ip, puerto, args.timeout):
            abiertos.append(puerto)
            print(f"  [ABIERTO] {puerto:5}  {SERVICIOS[puerto]}")

    print()
    if abiertos:
        print(f"{len(abiertos)} puerto(s) abierto(s) de {len(SERVICIOS)} conocidos.")
    else:
        print("Ningun puerto conocido abierto. La maquina no expone estos servicios.")


if __name__ == "__main__":
    main()
