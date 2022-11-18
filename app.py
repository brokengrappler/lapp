#!/usr/bin/env python3

import aws_cdk as cdk

from lapp.lapp_stack import LappStack


app = cdk.App()
LappStack(app, "lapp")

app.synth()
