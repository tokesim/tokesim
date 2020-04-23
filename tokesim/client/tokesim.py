from tokesim.client import client_util
from tokesim.client.generated_types import (
    EndBlockTransactionResult,
    SimulationId,
    SimulationParams,
    SimulationResult,
    StartedBlockTransactionResult,
    StoppedSimulation,
)


class TokesimClient:
    def __init__(self, url: str):
        self.request = client_util.make_requestor(url)

    def start_simulation(self, params: SimulationParams) -> SimulationResult:
        return self.request("startSimulation", params)

    def stop_simulation(self, simulation_id: SimulationId) -> StoppedSimulation:
        return self.request("stopSimulation", simulation_id)

    def start_block_transactions(
        self, simulation_id: SimulationId
    ) -> StartedBlockTransactionResult:
        return self.request("startBlockTransactions", simulation_id)

    def end_block_transactions(
        self, simulation_id: SimulationId
    ) -> EndBlockTransactionResult:
        return self.request("endBlockTransactions", simulation_id)
