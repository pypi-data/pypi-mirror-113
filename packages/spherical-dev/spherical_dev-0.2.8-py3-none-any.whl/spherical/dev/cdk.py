import shutil

import invoke

from .node import node_install, npm_install


@invoke.task(node_install)
def cdk(ctx):
    if shutil.which('cdk') is not None:
        return
    npm_install(ctx, ('aws-cdk',))


@invoke.task(cdk)
def deploy(ctx):
    ctx.run('cdk --app "inv cdk.infra" bootstrap')
    ctx.run('cdk --app "inv cdk.infra" deploy --all --require-approval=never', pty=True)


@invoke.task(cdk)
def destroy(ctx):
    ctx.run('cdk --app "inv cdk.infra" destroy --all --require-approval=never', pty=True)
