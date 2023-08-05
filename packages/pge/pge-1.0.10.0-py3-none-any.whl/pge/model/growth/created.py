from pge.model.growth.bsc.basic import SchemaGrowth
from pge.model.growth.bsc.pa import PAGrowth


class PASchemaFreeEvolve(SchemaGrowth, PAGrowth):
    def __init__(self, graph, deg, params, schema):
        SchemaGrowth.__init__(self, graph, deg, params, schema)
