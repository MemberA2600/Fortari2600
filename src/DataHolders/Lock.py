class Lock:
    def __init__(self, text):
        # It is not implemented yet, shoudl be something like this:
        # metal,music,0
        text = text.replace("\r","").replace("\n", "").split(",")
        self.name = text[0]
        self.type = text[1]
        self.number = int(text[2])

