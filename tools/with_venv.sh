#!/bin/bash
TOOLS=`dirname $0`
VENV=$TOOLS/../.kick-venv
source $VENV/bin/activate && $@
