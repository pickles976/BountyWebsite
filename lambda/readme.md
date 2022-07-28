Lambda function for sending Discord notifs

To build and reploy, run autodeploy.sh

Test locally:

    docker build -t lambda-discord .
    docker run -p 9000:8080 lambda-discord
    POST "http://localhost:9000/2015-03-31/functions/function/invocations" { "messages" : {...}}

To deploy:

Create an ECR repository with the same name as the docker image

Run autodeploy.sh