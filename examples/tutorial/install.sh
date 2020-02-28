#!/usr/bin/env bash

pip install -U pip
pip install -U Flask

# Install dos from source, then install pet_shop
pip install -e ../..
pip install -e .
