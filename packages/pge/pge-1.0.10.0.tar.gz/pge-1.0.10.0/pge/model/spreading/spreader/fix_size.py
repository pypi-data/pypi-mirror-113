import numpy as np

from pge.model.spreading.spreader.basic import SpreadingModel


class FixSpreadModel(SpreadingModel):
    def __init__(self, graph, in_direct=False):
        super().__init__(graph)
        self.ids = self.graph.get_ids(stable=True)
        self.in_direct = in_direct

    def init(self):
        self.received = {
            k: self.initial_status[k].copy() for k in self.initial_status.keys()
        }
        self.update(0)

    def iteration_bunch_comm(self, num_iter, tick, rs):
        res = []
        self.rs = rs

        for _ in np.arange(num_iter):
            n = 1
            self.init()

            while self.rs > np.min([time[1] for time in self.times]):
                if n > tick:
                    break

                self.iteration()
                self.update(n)
                n += 1

            res.append(self.times)
        return res
