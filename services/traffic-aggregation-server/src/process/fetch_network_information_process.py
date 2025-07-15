from config import network_names
import docker

network_information = {}

def get_network_information():
    if len(network_information.values()) == 0:
        print("fetching", flush=True)
        return fetch_network_information()
    else:
        return network_information



def fetch_network_information():
    docker_client = docker.from_env()
    docker_networks = docker_client.networks.list()

    for n in docker_networks:
        if n.name in network_names:
            network_information[n.name] = {"id": n.id}

    for n in network_information.values():
        network_services = []
        network_containers = docker_client.networks.get(n["id"]).attrs["Containers"]

        for container in network_containers.values():
            network_services.append({
                "name": container["Name"],
                "ip": container["IPv4Address"].split("/")[0],
            })

        n["services"] = network_services

    return network_information