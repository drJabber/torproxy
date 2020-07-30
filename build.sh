#!/bin/bash

sudo chown -R djabber:djabber data
cp -R ./docker/config/* ./data

docker-compose build