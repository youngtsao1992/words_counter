from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
import os
from word_counter.counter import WordCounter
from filetype_convert.doc2txt import FileTypeConvert

# defining options for opening a directory  
class Application(Frame):
    def __init__(self, master=None):
        self.fi_name = ""
        self.out_dir = ""
        self.dir_opt = options = {}
        options['initialdir'] = 'C:\\'  
        options['mustexist'] = False  
        options['parent'] = root  
        options['title'] = 'This is a title' 

        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def select_file(self, lb):
        self.fi_name = tkinter.filedialog.askopenfilename(filetypes=[("DOCX",".docx"), ("DOC",".doc"), ("TXT", ".txt")])
        if self.fi_name != '':
            lb.config(text='File chosen: ' + self.fi_name)
        else:
            lb.config(text='You did not choose any file!')

    def save_file(self, lb):
        self.out_dir= tkinter.filedialog.askdirectory(**self.dir_opt)
        if self.out_dir != '':
            lb.config(text='Save to: ' + self.out_dir)
        else:
            lb.config(text='You did not specify any directory!')

    def run(self, fi_name, wds_given, out_dir):

        txt_file = FileTypeConvert(fi_name)
        txt_file.convertDocxToText()

        wc = WordCounter(txt_file.textFilename)
        wc.counter_words_v2(wds_given, out_dir)

        fileExtension = fi_name.split(".")[-1]
        if fileExtension != "txt":
            os.remove(txt_file.textFilename)

        tkinter.messagebox.showinfo('Hi Miss,','Done! \nResult has been saved to '+self.out_dir)

    def createWidgets(self):
        fi_lb = Label(self, text='File Input: ')
        fi_lb.grid(column=0, row=0)
        fi_show_lb = Label(self, text='')
        fi_show_lb.grid(column=1, row=0)
        fi_select_btn = Button(self, text='Select File', command=lambda:self.select_file(fi_lb))
        fi_select_btn.grid(column=2, row=0)

        fo_lb = Label(self, text='Result Save: ')
        fo_lb.grid(column=0, row=1)
        fo_show_lb = Label(self, text='')
        fo_show_lb.grid(column=1, row=1)
        fo_select_btn = Button(self, text='Select File', command=lambda:self.save_file(fo_lb))
        fo_select_btn.grid(column=2, row=1)

        # put given words
        wds_given_entry = Entry(self)
        wds_given_entry.grid(column=0, row=2)

        run_btn = Button(self, text='Run', command=lambda:self.run(self.fi_name, wds_given_entry.get(), self.out_dir))
        run_btn.grid(column=0, row=3)


if __name__ == "__main__":

    root = Tk()
    root.title('TANGTANG(R) Word Counter')
    root.geometry('1240x640')

    app = Application(master=root)

    app.mainloop()

