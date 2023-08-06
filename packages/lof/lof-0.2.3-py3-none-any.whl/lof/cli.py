from typing import Optional

import typer

from lof import runner


def main(
    template: str = typer.Option(
        "template.yaml", help="Path to AWS Code Deploy template with lambdas"
    ),
    env: str = typer.Option(None, help="Path to file with environment variables"),
    exclude: Optional[str] = typer.Option("", 
                                          help="Exclude lambdas. FastAPI will not up & run them. Pass as string with comma. Example: PostTrafficHook,PretrafficHook."),
    port: Optional[int] = typer.Option(8000, help="Port to run lof"),
    host: Optional[str] = typer.Option("0.0.0.0", help="Host to run lof"),
    debug: Optional[bool] = typer.Option(True, help="Debug flag for FastAPI"),
):
    exclude = exclude.split(",")
    runner(template, env, exclude, port, host, debug)


def cli():
    typer.run(main)
