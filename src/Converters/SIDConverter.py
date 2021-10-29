# Using SID and MIDI modules from https://github.com/c64cryptoboy/ChiptuneSAK
# Unfortunately, I was not able to install the module properly because of
# compatibility errors.

class SIDConverter:

    def __init__(self, loader, path, removePercuss, maxChannels):

        self.__loader = loader
        self.__loader.collector.manuallyRegisterPackage("chiptunesak")
        from sid import SID
        from midi import MIDI
        from MidiConverter import MidiConverter

        sid = SID()
        midi = MIDI()

        chirp = sid.to_rchirp(path)

        midi.export_chirp_to_midi(chirp.to_chirp(), "temp/temp.mid")
        midiConverter = MidiConverter("temp/temp.mid", self.__loader, removePercuss, maxChannels, 7)
        self.result, self.songName = midiConverter.result, midiConverter.songName

        self.__loader.collector.restoreSystemPath()