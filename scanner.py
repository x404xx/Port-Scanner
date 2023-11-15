import socket
import threading
from collections import namedtuple
from contextlib import contextmanager
from queue import Queue

from rich.console import Console
from rich.table import Table

from commonport import COMMON_PORTS


PortService = namedtuple('PortService', ['port', 'service'])

class PortScanner:
    def __init__(self, ip_list):
        self._start(ip_list)

    @staticmethod
    @contextmanager
    def _create_threads_context(num_threads=None, target=None, ip_list=None):
        threads = [threading.Thread(target=target, args=(ip,)) for ip in ip_list] \
            if ip_list \
            else [threading.Thread(target=target) for _ in range(num_threads)]

        for thread in threads:
            thread.start()
        yield threads

    def _start(self, ip_list):
        with self._create_threads_context(target=self._scan_ip, ip_list=ip_list) as threads:
            for thread in threads:
                thread.join()

    def _scan_ip(self, ip):
        results = {
            'protocol': 'tcp',
            'fqdn': socket.getfqdn(ip),
            'port_info': {'open': [], 'closed': []}
        }
        queue = Queue()
        for port, service in COMMON_PORTS.items():
            queue.put(PortService(port, service))

        def scan_port():
            while not queue.empty():
                port_service = queue.get()
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(1)
                    try:
                        sock.connect((ip, port_service.port))
                        payload = f'HEAD / HTTP/1.1\r\nHost: {ip}\r\nConnection: close\r\n\r\n'
                        sock.sendall(payload.encode('utf-8'))
                        sock.recv(1024)
                        handle_port_result(results, port_service, 'open')
                    except (ConnectionRefusedError, TimeoutError, Exception) as error:
                        handle_port_result(results, port_service, 'closed', str(error).title())
                    finally:
                        queue.task_done()

        def handle_port_result(results, port_service, state, reason=None):
            port_info = {
                'port': port_service.port,
                'service': port_service.service,
                'state': state,
                'reason': reason
            }
            results['port_info'][state].append(port_info)

        def display_results():
            console = Console()
            table = Table(expand=True, title=f"[bright_white]Report for[/bright_white] : [deep_pink2]{results['fqdn']}[/deep_pink2]")
            add_table_columns(table)
            add_table_rows(table, 'open', 'light_green')
            add_table_rows(table, 'closed', 'red1')
            console.print(table)

        def add_table_columns(table):
            columns = ['IP', 'Port', 'Protocol', 'Service', 'State', 'Reason']
            styles = ['slate_blue1', 'dodger_blue2', 'magenta', 'cyan', None, None]
            justifications = ['center'] * len(columns)
            for column, style, justification in zip(columns, styles, justifications):
                table.add_column(column, style=style, justify=justification)

        def add_table_rows(table, state, colour):
            for port_info in results['port_info'][state]:
                table.add_row(
                    ip,
                    str(port_info['port']),
                    results['protocol'],
                    port_info['service'],
                    f'[{colour}]{state.capitalize()}[/{colour}]',
                    f"[orange_red1]{port_info['reason']}[/orange_red1]" if state == 'closed' else ''
                )

        num_threads = min(10, queue.qsize())
        with self._create_threads_context(num_threads, target=scan_port) as threads:
            for thread in threads:
                thread.join()

        display_results()
