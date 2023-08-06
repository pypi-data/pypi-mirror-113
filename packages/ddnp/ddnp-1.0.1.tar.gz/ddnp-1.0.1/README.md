# DDNP: Docker Data Network Proxy

Utility for providing data from the build host to the build process container.


## Check code (static analysis)

```
pylint -d C0321,C0326,C0411,W0107,R1711 ddnp
```

## Build docker container

```
export DDNP_VERSION=1.0.1
docker build --build-arg VERSION=$DDNP_VERSION \
             --tag ddnp:${DDNP_VERSION} - < Dockerfile
```

## Run locally (mainly for testing)

```
PYTHONPATH=/home/niessner/Projects/DCP python3 -m ddnp -e /home/niessner/Projects/DCP/example.txt -v /tmp/test
```
