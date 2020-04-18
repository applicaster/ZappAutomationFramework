

class BuildingBlocksInterface(object):
    def __init__(self, test):
        self.test = test
        self.screens = {}
        self.__setup_building_blocks__()

    def boot_step(self): raise NotImplementedError
    def __setup_building_blocks__(self): raise NotImplementedError
