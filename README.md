# Stockfish HTTP API 0.0.1

It is my first attempt on using Python Flask

The API is a wrapper around Stockfish Chess Engine so that it is possible to use it thru an HTTP endpoint.

It uses [Python Stockfish Library](https://github.com/zhelyabuzhsky/stockfish) (Thanks [Ilya Zhelyabuzhsky](https://github.com/zhelyabuzhsky)), Flask and Gunicorn to initialise a web server with multiple worker threads.


# How To Use

It can easily be run through a Docker Container. Following are non-Docker instructions:

1. Download Stockfish Chess Engine Binary through https://stockfishchess.org/ and save it in `/usr/bin` as `stockfish`
1. Install relevant python modules
```
pip install stockfish
pip install gunicorn
pip install flask
```

3. Run `./start.sh` to start gunicorn and the application. Change the port inside `start.sh` as per your preference.
1. To access, make a POST request. An example is:

```
wget http://localhost/move --post-data="fen=rnbqkbnr/pppppppp/8/8/8/5N2/PPPPPPPP/RNBQKB1R b KQkq - 1 1&level=difficult" -O - -q 

# Result
{
    "fen": "rnbqkbnr/pppppppp/8/8/8/5N2/PPPPPPPP/RNBQKB1R b KQkq - 1 1",
    "level": "difficult",
    "move": "c7c5",
    "status": "ok"
}
```

# Endpoints

At present only one endpoint is available

* `move` : Takes POST input for `fen` and `level` (easy, medium, difficult)

# Example Docker Implemenation

## `Dockerfile`

```
FROM python:3

RUN pip install stockfish
RUN pip install gunicorn
RUN pip install flask
RUN apt-get update
RUN apt-get install -y vim

COPY ./stockfish_20011801_x64 /usr/bin/stockfish
RUN chmod 755 /usr/bin/stockfish

# Comment out the 2 lines below if you
# do not want the code inside the container
COPY ./app /app
RUN chmod 755 /app/start.sh

EXPOSE 80

WORKDIR /app

CMD ["./start.sh"]

```

Followed by

```
docker build -t stockfish .
```

## Docker Command

```
docker run -d \
     --name stockfish \
     --restart always \
     # uncomment the line below if you'd like to keep stockfish
     # development related code (not the libraries) outside of
     # the docker container
     #--mount type=bind,source=/data/stockfish-app,target=/app \
     -p 127.0.0.1:8080:80 \
     stockfish
```

