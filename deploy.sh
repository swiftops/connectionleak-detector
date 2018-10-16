#!/bin/bash
export HOST_IP=<host>
cd /home/ubuntu/microservice
docker-compose scale connectionleak=0
docker rm $(docker ps -q -f status=exited)
docker rmi -f <image-name> && docker pull <image-name> && docker-compose up -d --remove-orphans
