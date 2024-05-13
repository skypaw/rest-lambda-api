# rest-lambda-api

Simple AWS rest api with nosql database and AWS lambda as a handler.

Routes:

- `/list` - endpoint for listing characters
- `/favourites` - endpoint to read and write favourite characters
    - add -> POST Request with body `{"add": "character_name"}`
    - remove -> DELETE Request with body `{"remove": "character_name"}`

For IaaC using AWS cdk.

How to deploy:

1. Follow AWS documentation to install [AWS CDKv2](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html)
2. Run `cdk deploy -c ACCOUNT_ID=YOUR_AWS_ID`
