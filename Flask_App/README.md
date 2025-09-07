1 build:
docker build -t flask-application:test .

2 deploy:
docker run --rm -p 5000:5000 flask-application:test