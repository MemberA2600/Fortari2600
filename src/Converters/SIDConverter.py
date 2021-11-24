# Using SID and MIDI modules from https://github.com/c64cryptoboy/ChiptuneSAK
# Unfortunately, I was not able to install the module properly because of
# compatibility errors.

class SIDConverter:

    def __init__(self, loader, path, removePercuss, maxChannels, removeOutside, rangeToCut):

        self.__loader = loader
        self.__loader.collector.manuallyRegisterPackage("chiptunesak")
        from sid import SID
        from midi import MIDI
        from MidiConverter import MidiConverter

        sid = SID()
        midi = MIDI()

        from random import randint

        r = randint(0, 1000)
        if r < 995:
            self.__loader.soundPlayer.playSound("Ask")
        else:
            self.__loader.soundPlayer.playSound("Probe")

        sid.set_options(seconds=self.__loader.fileDialogs.askForInteger("askForSomething", "askForSeconds"))

        r = randint(0, 1000)
        if r < 995:
            self.__loader.soundPlayer.playSound("Ask")
        else:
            self.__loader.soundPlayer.playSound("Probe")

        sid.set_options(subtune=self.__loader.fileDialogs.askForInteger("askForSomething", "askForSubTune"))

        chirp = sid.to_rchirp(path)
        try:
            from os import remove
            remove("temp/temp.mid")
        except:
            pass

        midi.export_chirp_to_midi(chirp.to_chirp(), "temp/temp.mid")
        midiConverter = MidiConverter("temp/temp.mid", self.__loader, 1, maxChannels, removeOutside, 8.5, rangeToCut)
        self.result, self.songName = midiConverter.result, midiConverter.songName

        self.__loader.collector.restoreSystemPath()