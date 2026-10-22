# port-scanner

Escáner de puertos educativo, hecho con Python. Le pasás una IP o un nombre y te dice qué puertos conocidos tiene abiertos, o sea qué servicios está exponiendo esa máquina.

Es el complemento del [packet-sniffer](https://github.com/acostanoemi/packet-sniffer): el sniffer **escucha** el tráfico de forma pasiva; este **toca** puertos de forma activa para ver cuáles están abiertos.

## Uso ético y legal

Escaneá **solo tus propias máquinas o con permiso explícito**. Un escáner de puertos es la antesala técnica de un ataque: sondea qué servicios expone un equipo para saber por dónde entrar. Escanear equipos ajenos es ilegal (en Argentina, ley 26.388).

Blancos para practicar con permiso:

- `127.0.0.1` → tu propia máquina
- `192.168.0.1` → tu router
- `scanme.nmap.org` → server que Nmap ofrece justamente para practicar

## Cómo funciona

Por cada puerto, el scanner intenta abrir una conexión TCP normal. Si conecta, hay un servicio escuchando (puerto abierto); si la rechazan o no contesta, está cerrado. Es tráfico común, por eso **no necesita sudo**.

## Requisitos

Solo Python 3. No usa librerías externas (el módulo `socket` viene con Python).

## Uso

```bash
python3 port_scanner.py                  # escanea 127.0.0.1
python3 port_scanner.py 192.168.0.1      # escanea tu router
python3 port_scanner.py scanme.nmap.org -t 1
```

| Opción | Qué hace |
|--------|----------|
| `host` | IP o nombre a escanear (default: `127.0.0.1`) |
| `-t`, `--timeout` | Segundos a esperar por puerto antes de darlo por cerrado (default: 0.5) |

## Roadmap

- [x] v1: escanear los puertos conocidos de una máquina
- [ ] v2: escanear un rango completo de puertos (1-1024 o 1-65535)
- [ ] v3: acelerar con hilos (escanear muchos puertos en paralelo)
- [ ] v4: banner grabbing (leer qué versión de servicio corre en cada puerto)
