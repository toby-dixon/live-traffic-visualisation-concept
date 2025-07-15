from config import network_names
from docker import DockerClient

def fetch_network_information(docker_client: DockerClient):
    docker_networks = docker_client.networks.list()

    network_information = {}
    for n in docker_networks:
        if n.name in network_names:
            network_information[n.name] = {"id": n.id}

    for n in network_information.values():
        network_services = []
        network_containers = docker_client.networks.get(n["id"]).attrs["Containers"]
        print(network_containers, flush=True)

        for container in network_containers.values():
            print(container, flush=True)
            network_services.append({
                "name": container["Name"],
                "ip": container["IPv4Address"].split("/")[0],
            })

        n["services"] = network_services

    return network_information