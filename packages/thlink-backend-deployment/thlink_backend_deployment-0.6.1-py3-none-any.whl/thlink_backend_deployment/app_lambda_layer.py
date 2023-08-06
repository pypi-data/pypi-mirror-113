from typing import List
import os
import shutil
import subprocess
from aws_cdk import core
import aws_cdk.aws_lambda as lambda_


class AppLambdaLayer(lambda_.LayerVersion):

    def __init__(self, scope: core.Construct, construct_id: str,
                 scope_dir: str,
                 include: List[str] = None, **kwargs,
                 ):
        """
        :param scope:
        :param construct_id:
        :param scope_dir: scope directory (relative to project root) -> parent dir of include path
        :param include: list of paths to include -> lambda layer paths
        :param kwargs: compatible_runtimes (required), ... passed down to lambda_.LayerVersion
        """
        if include is None:
            include = {}
        build_path = f"_build/{scope_dir}"

        # clean build path
        shutil.rmtree(build_path, ignore_errors=True)
        os.makedirs(build_path)

        # app lambda layer
        os.makedirs(f"{build_path}/app_lambda_layer/python")
        # app -> external requirements
        subprocess.run(
            f"poetry export -f requirements.txt > {os.path.abspath(f'{build_path}/app_lambda_layer/requirements.txt')}",
            cwd=scope_dir,
            shell=True,
        )
        subprocess.run(
            f"pip install -r app_lambda_layer/requirements.txt -t app_lambda_layer/python",
            cwd=build_path,
            shell=True,
        )
        # app -> include paths
        for path in include:
            os.makedirs(f"{build_path}/app_lambda_layer/python/{path}")
            shutil.copytree(
                f"{scope_dir}/{path}", f"{build_path}/app_lambda_layer/python/{path}",
                dirs_exist_ok=True,
            )

        # optimize (remove Lambda Runtime modules)
        lambda_included = [
            "boto3",
            "botocore",
            "s3transfer",
        ]
        for module in lambda_included:
            shutil.rmtree(f"{build_path}/app_lambda_layer/python/{module}", ignore_errors=True)

        super().__init__(
            scope,
            construct_id,
            code=lambda_.Code.from_asset(f"{build_path}/app_lambda_layer"),
            **kwargs,
        )
