# Tokesim 
![CI](https://github.com/tokesim/tokesim/workflows/CI/badge.svg)
<center>
  <h3 align="center">Tokesim</h3>

  <p align="center">
    A Tokeneconomics Simulator.
    <br />
    <a href="https://youtube.com/">View Demo</a>
    ·
    <!-- <a href="https://github.com/tokesim/issues/new?assignees=&labels=&template=bug_report.md&title=">Report Bug</a>-->
    ·
    <!-- <a href="https://github.com/tokesim/issues/new?assignees=&labels=&template=feature_request.md&title=">Request Feature</a> -->
  </p>
</center>

<!-- table of contents -->
## Table of Contents
  - [About The Project](#about-the-project)
  - [Getting Started](#getting-started)
      - [Prerequisites](#prerequisites)
      - [Installation](#installation)
- [Usage](#usage)
  - [Run Simulation](#run-simulation)
  - [Start explorer](#start-the-explorer)
  - [Configurations](#configurations)
- [Contributing](#contributing)
- [Resources](#resources)

<!-- about the project -->
## About The Project

[Tokesim](https://tokesim.org) is an Agent Based Modeling tool that makes it easy to test token economic models. It's built using [mesa-behaviors](https://github.com/mesa_behaviors) an extension to [Mesa](https://github.com/mesaproject/mesa) ABM framework bring more type hints and patterns to make models,agents,utility functions and strategies shareable and more extensible.  The goal of Tokesim is to help developers run simulations against Smart Contracts, in a block chain agnostic way, using shreable and reusable modules and libraries to do so. 

Tokesim Features:
- Typehints to make agents and models extensible 
- Ability to run against and simulation against your smart contracts
- An architecture to make the simulations portable to multiple chains
- ChartJS integration from Mesa framework
- Support for testing Ethereum based smart contracts directly


<!-- getting started with the project -->
## Getting Started
### Prerequisites
- node `v10.15.3` or later
- npm `v6.4.1` or later
- python `3.7` or later but not 3.8 ;) 

### Installation
Clone/ download the project, and install dependencies. For development
```bash
git clone https://github.com/tokesim/tokesim.git && cd tokesim 
python3.7 -m venv venv
source venv/bin/activate
pip install poetry
poetry build
npm install -g @tokesim/tokesim-chain
# in a new terminal window
tokesim-chain --port 5554
```
or 
```bash
pip install tokesim
npm install -g @tokesim/tokesim-chain
# in a new terminal window
tokesim-chain --port 3004
```


<!-- example usage, screen shots, demos -->
## Usage
### Run simulation 
In order to run a simulation against a chain the default init will create a simulation for you to modify as you see fit. You'll need to start the chain simulation service.
```bash
# remember to activate your venv
source venv/bin/activate
pip install tokesim

# just like create react app generate template
tokesim init --dir simple-token --agents 20

#start chain simulator
tokesim-chain -c ethereum --port 3004

#run the simulation defaults to terminating after 100 steps
tokesim run --config ./simple-token/simulation.json --port 3004
```

#### Simulation App Layout 

By default tokesim init will generate a default application layout, that specifies the accounts used a balance for each of the agents as well as configuration file and some simple bonded token curve agents. The contracts specified are a listed [here](https://github.com/tokesim/example-smart-contracts)

```bash
# ./simple-token/
.
└── simple-token    
    └── contracts 
    |    |── SimpleToken.bin
    |    └── SimpleToken_abi.json
    |── accounts.json    
    |── config_schema.json       
    |── simple_token_agent.py
    |── simple_token_model.py
    |── simple_token_config.py
    └── simulation.json
```

### Configurations
Explanation coming soon
<!-- template just leave alone  -->
## Roadmap
Coming soon

<!-- template just leave alone  -->
## Contributing
How to contribute, build and release are outlined in [CONTRIBUTING.md](CONTRIBUTING.md), [BUILDING.md](BUILDING.md) and [RELEASING.md](RELEASING.md) respectively. Commits in this repository follow the [CONVENTIONAL_COMMITS.md](CONVENTIONAL_COMMITS.md) specification.

## License
Apache License 2.0

<!-- references and additional resources  -->
## Resources
- [Mesa](https://github.com/mesaproject/mesa)
- [mesa-behaviors](https://github.com/tokesim/mesa_behaviors)
- [tokesim-chain](https://github.com/tokesim/tokesim-chain)
- [OpenRPC](https://open-rpc.org)
