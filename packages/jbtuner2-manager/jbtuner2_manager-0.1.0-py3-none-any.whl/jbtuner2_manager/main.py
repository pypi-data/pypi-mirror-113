import socket
from typing import Optional

import typer

from jbtuner2_manager import __version__
from . import espota

app = typer.Typer()


def version_callback(value: bool):
    if value:
        typer.secho(f"CLI Version: {__version__}", fg=typer.colors.MAGENTA)
        raise typer.Exit()


# Main command
@app.callback()
def main(
        _version: Optional[bool] = typer.Option(
            None, "--version", "-v", callback=version_callback, is_eager=True
        ),
):
    """
    =======================================================================
    JB Tuner 2 Manager - An integrated tool for managing Chord X JB Tuner 2
    =======================================================================
    """
    typer.echo(f"Welcome to use JB Tuner 2 manager <{__version__}>\n")


def scan(dest_ip, udp_port, timeout):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        # Enable broadcasting mode
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(timeout)
        # Send the message
        sock.sendto(bytes("hello", "utf-8"), (dest_ip, udp_port))
        try:
            for i in range(10):
                data, addr = sock.recvfrom(1024)
                typer.echo(f"{addr} response: {data}")
        except Exception:
            pass


@app.command("list")
def ls(
    ip: str = typer.Option("10.0.0.255", "--ip-address", "-a", help="the IP/Broadcast address"),
    port: Optional[int] = typer.Option(1979, "--port", "-p", help="the port number"),
    timeout: Optional[int] = typer.Option(1.0, "--timeout", "-t", help="the timeout seconds"),
):
    typer.echo(f"Start scanning for {timeout} seconds... ")
    scan(ip, port, timeout)


@app.command("update")
def update_program(
    host: str = typer.Argument(..., help="the hostname or IP address of JB Tuner"),
    fwfile: str = typer.Option(..., "--firmware", "-f", help="the file of firmware"),
):
    command = ['-i', host, '-p', '3232', '-r', '-d', '-f', fwfile]
    print('Using command %s' % ' '.join(command))
    espota.main(command)


@app.command("config")
def config(
    host: str = typer.Argument(..., help="the hostname or IP address of JB Tuner"),
    configfile: str = typer.Option(..., "--config", "-c", help="the config file"),
):
    command = ['-i', host, '-p', '3232', '-r', '-d', '-s', '-f', configfile]
    print('Using command %s' % ' '.join(command))
    espota.main(command)


if __name__ == "__main__":
    app()
