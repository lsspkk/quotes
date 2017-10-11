# API with quotes and tags

Docker, Flask, Redis

# setup

        apt install redis-server
        apt install python3-pip

        pip3 install -r requirements.txt
        export FLASK_DEBUG=1
        export REDIS_HOST=localhost
        python3 api.py


# setup with docker

        apt install docker-compose
        cd to quotes folder
        docker-compose --project-name quotes -f docker-compose.yml up

## if you make changes
        docker-compose --build


## clear all docker stuff
        docker stop $(docker ps -a -q) ; docker rm $(docker ps -a -q)



# test

        curl localhost:8042/quotes -H "Content-Type: application/json" -X POST -d '{"quote":"Nurture a culture of monitoring everything.", "tags": [ "API", "DevOps", "technology" ]}' 

        curl localhost:8042/quotes -H "Content-Type: application/json" -X POST -d '{"quote":"Developer groups of humans are microservices themselves.", "tags": [ "Efficiency", "business" ]}' 

        curl localhost:8042/quotes -H "Content-Type: application/json" -X POST -d '{"quote":"Transient states do not belong in the database.", "tags": [ "scaling", "SQL", "technology" ]}' 

        curl localhost:quotes

        curl localhost:8042/quotes
        curl localhost:8042/quotes/4
        curl localhost:8042/quotes
        curl localhost:8042/quotes/5
        curl localhost:8042/quotes/4
        curl localhost:8042/tags
        curl localhost:8042/quotes/random




# todo

## Add filters: 
/quotes/?tag=something         get quotes with tags
/quotes/?q=letters             get quotes with search string

## Add stars:
let users give stars to quotes
/quotes/id/stars/1-100

let users filter quotes with stars
