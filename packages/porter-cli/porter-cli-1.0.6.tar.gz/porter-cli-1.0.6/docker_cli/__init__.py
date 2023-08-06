import click


@click.group(help='Long time functions commands')
def long_time():
    pass


@long_time.command(help='Deploy a long-lasting function')
def deploy():
    print("Long time function deployment is under development")
