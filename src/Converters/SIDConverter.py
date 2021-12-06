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

        constant = 8.5

        r = randint(0, 1000)
        if r < 995:
            self.__loader.soundPlayer.playSound("Ask")
        else:
            self.__loader.soundPlayer.playSound("Probe")

        seconds = self.__loader.fileDialogs.askForInteger("askForSomething", "askForSeconds")
        if seconds == None:
           seconds = 15
        sid.set_options(seconds=seconds)

        r = randint(0, 1000)
        if r < 995:
            self.__loader.soundPlayer.playSound("Ask")
        else:
            self.__loader.soundPlayer.playSound("Probe")

        subtune = self.__loader.fileDialogs.askForInteger("askForSomething", "askForSubTune")
        if subtune == None:
           subtune = 0
        sid.set_options(subtune=subtune)

        chirp = None
        try:
            chirp = sid.to_rchirp(path)
        except:
            number = 0
            while True:
                try:
                    sid.set_options(subtune=number)
                    chirp = sid.to_rchirp(path)
                    break
                except:
                    number = number + 1
                    if number == subtune:
                        number = number + 1
                    if number<2:
                        continue
                    else:
                        constant = 2.5
                        try:
                            import os
                            os.remove("temp/temp.mid")
                        except:
                            pass
                        try:
                            import os
                            self.__loader.executor.execute("sid2midi",
                                ("-o"+str(subtune), "-t"+str(seconds),
                                '"'+path+'"', '"' + os.getcwd()+"/temp/temp.mid" + '"'),
                                True)

                        except:
                            print(str(e))
                            while True:
                                number = 0
                                try:
                                    import os
                                    self.__loader.executor.execute("sid2midi",
                                                                   ("-o" + str(number), "-t" + str(seconds)),
                                                                   '"' + path + '"', '"' + os.getcwd()+"/temp/temp.mid" + '"',
                                                                   True)
                                except:
                                    number = number + 1
                                    if number == subtune:
                                        number = number + 1
                                    if number < 2:
                                        continue
                                    else:
                                        break
                    break

        if chirp != None:
            try:
                from os import remove
                remove("temp/temp.mid")
            except:
                pass
            midi.export_chirp_to_midi(chirp.to_chirp(), "temp/temp.mid")

        midiConverter = MidiConverter("temp/temp.mid", self.__loader, 1, maxChannels, removeOutside, constant, rangeToCut, True)
        self.result, self.songName = midiConverter.result, midiConverter.songName

        self.__loader.collector.restoreSystemPath()