from testcontainers.general import DockerContainer
from .retry import retry


@retry(TypeError, retries=3, cooldown=3)
def get_exposed_port(container: DockerContainer, port: int):
    return container.get_exposed_port(port)


def get_bridge_ip(container: DockerContainer) -> str:
    """
    Returns the IP address of the container on the default bridge network.
    :param container: a docker container.
    :return: an IP address.
    """
    return container.get_docker_client().bridge_ip(container.get_wrapped_container().id)
