class Lock:
    def __init__(self, text):
        # It is not implemented yet, shoudl be something like this:
        # metal,music,0,{END}
        text = text.replace("\r","").replace("\n", "").split(",")
        self.name = text[0]
        self.type = text[1]
        self.number = int(text[2])
        try:
            if text[3] == "LAST":
                self.last = True
        except:
            self.last = False