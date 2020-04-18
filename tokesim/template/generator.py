import tokesim.template.ethereum.generator as ethereum_template


def generate_initial_template(dest: str, num_agents: int) -> None:
    ethereum_template.setup(dest, num_agents)
