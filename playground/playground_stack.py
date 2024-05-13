from aws_cdk import (
    Stack, RemovalPolicy
)
from aws_cdk.aws_apigateway import LambdaRestApi, StageOptions
from aws_cdk.aws_dynamodb import Table, Attribute, AttributeType, BillingMode
from aws_cdk.aws_iam import Role, ServicePrincipal, PolicyDocument, PolicyStatement, Effect
from aws_cdk.aws_lambda import Function, Runtime, RuntimeFamily, Code
from constructs import Construct


class PlaygroundStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        table = Table(self,
                      id='Table',
                      table_name='table',
                      partition_key=Attribute(name='type', type=AttributeType.STRING),
                      sort_key=Attribute(name='id', type=AttributeType.STRING),
                      removal_policy=RemovalPolicy.DESTROY,
                      billing_mode=BillingMode.PAY_PER_REQUEST)

        lambda_role = Role(self,
                           id='lambda-role',
                           assumed_by=ServicePrincipal('lambda.amazonaws.com'),
                           inline_policies={'lambda-policy': PolicyDocument(statements=[
                               PolicyStatement(actions=[
                                   "logs:CreateLogGroup",
                                   'logs:CreateLogStream',
                                   "logs:PutLogEvents"],
                                   effect=Effect.ALLOW,
                                   resources=['*']
                               ),
                               PolicyStatement(actions=[
                                   "dynamodb:PutItem",
                                   'dynamodb:GetItem',
                                   "dynamodb:Query"],
                                   effect=Effect.ALLOW,
                                   resources=['*'])
                           ])})

        lambda_function = Function(self,
                                   id='Lambda',
                                   function_name='lambda',
                                   runtime=Runtime(name='python3.10',
                                                   family=RuntimeFamily.PYTHON),
                                   handler='func.handler',
                                   environment={'TABLE_NAME': table.table_name},
                                   code=Code.from_asset('./func'),
                                   role=lambda_role)

        api = LambdaRestApi(self,
                            id="RestApi",
                            rest_api_name='rest-api',
                            handler=lambda_function,
                            deploy_options=StageOptions(
                                stage_name='api',
                                metrics_enabled=False,
                                tracing_enabled=False,
                                data_trace_enabled=False,
                                caching_enabled=False
                            ),
                            endpoint_export_name='rest-api-url',
                            proxy=False,
                            )

        api.root.add_method("GET")

        fav = api.root.add_resource("favourites")
        fav.add_method("GET")
        fav.add_method("POST")
        fav.add_method("DELETE")

        list_endpoint = api.root.add_resource("list")
        list_endpoint.add_method("GET")
