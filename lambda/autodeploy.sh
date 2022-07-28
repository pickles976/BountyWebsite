#! /bin/bash

echo "enter image name:"
read img

aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 531418479922.dkr.ecr.us-east-2.amazonaws.com
docker build -t $img . 
docker tag $img:latest 531418479922.dkr.ecr.us-east-2.amazonaws.com/$img:latest
docker push 531418479922.dkr.ecr.us-east-2.amazonaws.com/$img:latest