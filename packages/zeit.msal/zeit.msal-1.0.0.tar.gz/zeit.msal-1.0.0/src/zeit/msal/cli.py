from zeit.msal.authenticate import Authenticator
import click
import zeit.msal.cache


@click.group()
@click.option('--tenant-id', default=Authenticator.tenant_zeitverlag)
@click.option('--client-id')
@click.option('--client-secret')
@click.option('--cache-url')
@click.pass_context
def cli(ctx, **kw):
    pass


@cli.command()
@click.pass_context
def get(ctx):
    auth = create_authenticator(ctx.parent.params)
    print(auth.get_id_token())


@cli.command()
@click.pass_context
def login(ctx):
    auth = create_authenticator(ctx.parent.params)
    auth.login_interactively()


def create_authenticator(opt):
    return Authenticator(
        opt['client_id'], opt['client_secret'],
        zeit.msal.cache.from_url(opt['cache_url']),
        opt['tenant_id'])
