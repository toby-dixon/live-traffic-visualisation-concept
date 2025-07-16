# Live traffic visualizations

## TODO

- [ ] Add documentation for adding a new server
  - Requires figuring out how to add a new server.
- [ ] Add ability to replay events
  - Will need to store access logs somewhere, and have some GUI navigation element
  - Maybe allow modification of speed of replay as well - Should only really have to reserve main view page, just with stored logs rather than live logs.
    - Can I just pass them an array of all logs I want to replay, and just have them replay in order?
- [ ] Structure frontend
  - Not some monolithic HTML file
  - Separate logic - will make configuration easier as well (perhaps a config.js file that defines constants)
  - Perhaps serve as a different container than server?
    - Isolated NODE Dockerfile
- [ ] Split into different docker compose files?
  - Docker compose for a server's public and private proxies.
  - Docker compose for a collection of services on a particular server
  - Docker compose for the traffic aggregator
  - In practice I should just be able to deploy these compose files on different servers, maybe test with rpi?
  - For development I will need another solution.

## Description

The outline of this concept is detailed in the [how to monitor networks](how%20to%20monitor%20networks.drawio.pdf) pdf
file. This project attempts to put the concept into practice. It essentially visualises completed requests in realtime -
meaning that subsequent requests will be visualised before initial requests, as they are requested and responded first.

It consists of

1. 2 traefik proxies:
    - Public Server Proxy
        - For public access. Any public facing endpoints/services are accessed through this proxy network
    - Private Server Proxy
        - For communication between containers. Containers won't communicate directly - instead each container will
          communicate via the private proxy.
2. 2 API services
    - communicating service
        - An api service that communicates with any other private service(s) and returns aggregate data.
    - non-communicating service
        - An api service that returns some data. It is essentially the leaf node of this structure.

In order for a network to be considered relevant, its name must be listed
in [the network_names config](services/traffic-aggregation-server/config/config.py)

***IMPORTANT*** - `non-communicating-service` is designed to send 400 response codes sometimes in order to illustrate
what happens on a bad request.

## Live Visualisation

Once this initial structure is set up - the next step would be to build a service that watches the traefik access logs
produced by both the public and private proxies, and live updates (through webhooks) a d3.js node graph visualisation.
It can show each container as a node, and each network connection/communication as an edge.

Any activity should be visually represented in realtime

- Request was sent from service A to service B - edge flash - perhaps indicating direction somehow
- Service returned a non 200-300 response code - flash red
- Service returned a 200-300 response code - flash green
- etc...

## Imitating multiple servers

Once the visualisation of a single mock server has been achieved, try introducing another docker compose, consisting of
the same services but configured on a different network with different proxies. Then add some communication cross
server (imitating private communication via GCP interal networks/ip). Can a visualisation service illustrate both
servers at the same time? Can it detect when an incoming request is from outside the private proxy? etc...

## Potential issues from first thoughts

How do I identify services? The traefik api does allow for the fetching of services/routers - perhaps this could be used
at the inception of the visualisation service to generate our initial nodes (for each proxy). Then, when reading the
traefik logs we attempt to correlate the node names to the client and request details listed in the logs.

- When detailing communication between docker containers, does the `ClientAddr` variable show as the name of the docker
  container or the internal ip address of the container?
- The Request container should be easy enough to deduce, as the service address, or service name etc... should match
  what the api returned when creating the nodes.
- The same question arrises for communication from a private service on proxy to a private service on another proxy, if
  the visualisation service has access to both networks, can it match these node names?
- There should be some handler for the cases where names cannot be matched (some external node representing unrecognised
  traffic into the proxy).

## Endpoints

- localhost:82/
    - Visualisation of realtime requests.
    - To make highlight last longer, modify the `HIGHLIGHT_DURATION` constant
      in [index.html](services/traffic-aggregation-server/static/index.html).
    - Bad requests are logged as well as highlighted red.
- public.localhost
    - Publicly accessible service that communicates with private services
- localhost:82/network_info
    - traffic aggregation server network info endpoint
- localhost:82/access_logs (WEBSOCKET)
    - Realtime updating access logs, formatting with network name, service from and service to

## Adding a new service

In the docker compose:

1. Add a new service

- Make sure that it is on whichever network it should be accessible through
- e.g. if it should be accessible from outside the server, put it on the public-server-proxy-network
- e.g. if it should only be accessible from within the server by other services, put it on the
  private-server-proxy-network

2. Add the service to the config in its corresponding proxy's `dynamic/` directory

- e.g. for public - [public-server-proxy/dynamic/public-services.yml](public-server-proxy/dynamic/public-services.yml)
- e.g. for
  private - [private-server-proxy/dynamic/private-services.yml](private-server-proxy/dynamic/private-services.yml)
- In order to add the service, add a new router and service in the yaml.
    - The service can be copied from another, all that needs changing is the load balancer URL which should just point to
      the service's container, make sure to specify which port.
    - The router can be copied, but the routing rules must be modified (only path prefix for private. Make sure to also
      add the strip prefix middleware) as well as the service it points to  (which should be the one just created).