class MidiNote:

    def __init__(self, v, n, d):
        self.velocity = v
        self.note = n
        self.duration = d

    def returnData(self):
        return(self.velocity, self.note, self.duration)

