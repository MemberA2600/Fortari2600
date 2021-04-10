from tkinter import *

class LoadingScreen():
    """This class only opens a loading screen image and swaits for 3 seccnds,
    then destroys the window and then goes back to the main window."""

    def __init__(self, size, super, tk):
        from PIL import ImageTk, Image

        self.__w_Size=round(800*(size[0]/1600))
        self.__h_Size=round(self.__w_Size*0.56)
        self.__Loading_Window=Toplevel()
        self.__Loading_Window.geometry("%dx%d+%d+%d" % (self.__w_Size, self.__h_Size,
                                                        (size[0]/2)-self.__w_Size/2,
                                                        (size[1]/2)-self.__h_Size/2-50))
        self.__Loading_Window.overrideredirect(True)
        self.__Loading_Window.resizable(False, False)

        self.__Img = ImageTk.PhotoImage(Image.open("others/img/loading.png").resize((self.__w_Size,self.__h_Size)))

        self.__ImgLabel = Label(self.__Loading_Window, image=self.__Img)
        self.__ImgLabel.pack()

        super.setLoadingScreen(self)
        #self.__Loading_Window.after(3000, self.destroySelf)
        self.__Loading_Window.wait_window()

    def destroySelf(self):
        self.__Loading_Window.destroy()

