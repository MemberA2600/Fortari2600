class Command:

    def __init__(self, loader, string):
        self.__loader = loader
        data = string.split(",")
        self.alias = data[0][1:-1].split(" ")
