import aws_cdk as cdk
from playground.playground_stack import PlaygroundStack

app = cdk.App()
PlaygroundStack(app, "PlaygroundStack")
app.synth()
