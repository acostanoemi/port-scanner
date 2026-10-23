# port-scanner

Escáner de puertos educativo, hecho con Python. Le pasás una IP o un nombre y te dice qué puertos tiene abiertos, qué servicio corre en cada uno y, cuando puede, qué programa y versión. Escanea rangos completos usando hilos en paralelo, con barra de progreso.

Es el complemento del [packet-sniffer](https://github.com/acostanoemi/packet-sniffer): el sniffer **escucha** el tráfico de forma pasiva; este **toca** puertos de forma activa para ver cuáles están abiertos.

## ⚠️ Uso ético y legal

Escaneá **solo tus propias máquinas o con permiso explícito**. Un escáner de puertos es la antesala técnica de un ataque: sondea qué servicios expone un equipo para saber por dónde entrar. Escanear equipos ajenos es ilegal (en Argentina, ley 26.388).

Blancos para practicar con permiso:

- `127.0.0.1` → tu propia máquina
- `192.168.0.1` → tu router
- `scanme.nmap.org` → server que Nmap ofrece justamente para practicar

## Cómo funciona

Por cada puerto, el scanner intenta abrir una conexión TCP normal. Si conecta, hay un servicio escuchando (puerto abierto); si la rechazan o no contesta, está cerrado. Es tráfico común, por eso **no necesita sudo**.

Para escanear miles de puertos sin tardar horas, usa **hilos**: lanza muchas pruebas en paralelo. Funciona bien porque el scanner pasa casi todo el tiempo esperando a la red, no calculando.

### Banner grabbing

Por cada puerto abierto, intenta leer el **banner**: la línea de presentación que muchos servicios mandan al conectarse, que suele revelar el programa y la versión (ej: `OpenSSH 8.9`). Saber la versión exacta es el paso previo a buscarle vulnerabilidades conocidas, por eso muchos servidores la ocultan a propósito. Se puede desactivar con `--sin-banner`.

## Requisitos

Solo Python 3. No usa librerías externas.

## Uso

```bash
python3 port_scanner.py                          # 127.0.0.1, puertos 1-1024
python3 port_scanner.py 192.168.0.1              # tu router
python3 port_scanner.py scanme.nmap.org --hasta 65535
python3 port_scanner.py 192.168.0.1 --desde 1 --hasta 100 --hilos 200
```

| Opción | Qué hace |
|--------|----------|
| `host` | IP o nombre a escanear (default: `127.0.0.1`) |
| `--desde` | Primer puerto del rango (default: 1) |
| `--hasta` | Último puerto del rango (default: 1024) |
| `--hilos` | Cuántos puertos probar en paralelo (default: 100) |
| `-t`, `--timeout` | Segundos a esperar por puerto (default: 0.5) |
| `--sin-banner` | No intentar leer el banner de los puertos abiertos |

## Roadmap

- [x] v1: escanear los puertos conocidos de una máquina
- [x] v2: escanear un rango completo de puertos, acelerado con hilos
- [x] v3: banner grabbing (leer qué versión de servicio corre en cada puerto)
- [x] v4: barra de progreso para rangos grandes
- [ ] v5: guardar el resultado a un archivo (reporte)
