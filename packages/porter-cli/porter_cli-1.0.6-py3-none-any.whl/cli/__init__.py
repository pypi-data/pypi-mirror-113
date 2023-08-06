import sys
from chalice.cli import main as chalice_main, cli
from docker_cli import long_time

def cli_main():
    args = sys.argv
    if "--help" in args or len(args) == 1:
        print("Porter CLI")
    cli.add_command(long_time)
    chalice_main()
