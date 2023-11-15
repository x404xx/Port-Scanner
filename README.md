<div align='center'>

# PortScanner <img src='https://github.com/x404xx/Port-Scanner/assets/114883816/446085c1-09cc-4d39-846f-c059f8619d0e' width='50'>

**PortScanner** determines the status of `open` and `closed` ports on specified IP addresses by employing multithreading to concurrently scan multiple ports.

<img src='https://github.com/x404xx/Port-Scanner/assets/114883816/66ff3f7b-cf5b-4771-ae87-cd502cc52ed0' width='700' height='auto'>

</div>

## Installation

```
pip install rich
```

## Usage

Running _**PortScanner**_ using command-line ::

```
usage: main.py [-h] [-ip IP] [-f FILE]

Simple port scanner using threading.

options:
-h, --help            show this help message and exit
-ip IP                IP address to scan
-f FILE, --file FILE  Text file containing a list of IPs to scan (one IP per line)
```

Command-line example ::

-   Single IP

```python
python main.py -ip 207.180.224.191
```

-   Multiple IP

```python
python main.py -f ip_list.txt
```

## Legal Disclaimer

> **Note**
> This was made for educational purposes only, nobody which directly involved in this project is responsible for any damages caused. **_You are responsible for your actions._**

