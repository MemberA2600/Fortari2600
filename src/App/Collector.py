
class Collector:
    from sys import path as systemPath

    def __init__(self, systemPath):
        import os
        for root, dir, files in os.walk(".", topdown=False):
            systemPath.append(root)