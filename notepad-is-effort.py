import tkinter as tk
import tkinter.messagebox, tkinter.font
import os, sys, webbrowser, subprocess, time

'''
A small portable IDE for C
Developed by Sophiadm

'''
class StartApp():
    def __init__(self, **kwargs):

        #Makes master window
        self.master = tk.Tk()
        self.master.wm_title("Notepad is effort")

        #Sets it to full screen automatically
        self.master.geometry("{0}x{1}+0+0".format(
            self.master.winfo_screenwidth(), self.master.winfo_screenheight()))

        #Creates instances of the navbar and text box classes
        self.text = TextInput(self.master)
        self.navbar = Navbar(self.master, self.text)

        #Starts the app
        self.master.mainloop()
        
class Navbar():
    def __init__(self, master, text):
        self.master = master
        self.text = text
        self.filepath = None
        
        self.nav = tk.Menu(self.master)
        self.master.config(menu=self.nav)

        #Creates top level nav buttons
        file = tk.Menu(self.nav)
        edit = tk.Menu(self.nav)
        run = tk.Menu(self.nav)
        help_ = tk.Menu(self.nav)


        self.nav.add_cascade(label='File', menu=file)
        file.add_command(label='Save', command= self.Save)
        file.add_command(label='Save As', command=lambda: self.popup(self.Save_as, 'Save As'))
        file.add_command(label='Open', command=self.Opennew)
        file.add_command(label='Add code', command=lambda: self.popup(self.Open, 'Open'))
        file.add_command(label='New', command=StartApp)        
        file.add_command(label='Exit', command=self.Exit)

        self.nav.add_cascade(label='Edit', menu=edit)
        edit.add_command(label='Undo', command= self.Undo)
        edit.add_command(label='Redo', command=self.Redo)
        edit.add_command(label='Indent', command=self.text.tabtext())

        self.nav.add_cascade(label='Run', menu=run)
        run.add_command(label='Run', command=self.Run)
        run.add_command(label='Save+Run', command=self.savenrun)

        self.nav.add_cascade(label='Help', menu=help_)
        help_.add_command(label='Search Index', command=lambda: self.popup(self.findindex, 'Search index', 'Enter the index'))
        help_.add_command(label='Documentation', command=lambda: self.google('http://devdocs.io/c/'))
        help_.add_command(label='S Overflow', command=lambda: self.google('http://stackoverflow.com/questions/ask'))

        #Binds keys to functions
        self.master.bind("<Control-s>", self.Save)
        self.master.bind("<Control-o>", self.Opennew)
        self.master.bind("<Control-n>", StartApp)
        self.master.bind("<Control-q", self.Exit)
        self.master.bind("<F5>", self.Run)

    def Save(self, e=1):
        if self.filepath != None: #Checks if it knows file location
            contents = self.text.TextBox.get('1.0', tk.END)

            f = open(self.filepath, 'w') # to clear the file
            f.write(contents)
            f.close()
        else: #If it hasn't already been saved/opened
            self.popup(self.Save_as, 'Save As') 
            
    def popup(self, command, title, Text='Please enter the file directory and name: '):
        #makes a second window
        self.master2 = tk.Tk()
        self.master2.title(title)

        #Asks question arg
        self.label2 = tk.Label(self.master2, bg='white', fg='black', text=Text)
        self.label2.pack(side=tk.TOP)

        dir_path = os.path.abspath() + 'hey.c'

        #Makes an input box for answer
        self.entry2 = tk.Entry(self.master2, bg='white', fg='black')
        
        if Text == 'Please enter the file directory and name: ':            
            self.entry2.insert(tkinter.END, dir_path)
        self.entry2.pack(side=tkinter.LEFT, fill=tk.BOTH, expand=1)

        self.button2 = tk.Button(self.master2, text='ok', bg='white', fg='black', command=command).pack(side=tkinter.LEFT)
        self.master2.bind("<Return>", command)

    def Save_as(self, rerun=None):
        #Uses second window to save file as inputted name
        self.filepath = self.entry2.get()
        contents = self.text.TextBox.get("1.0", tk.END)
        
        if self.filepath[len(self.filepath) - 2:] != '.c':
            self.filepath += '.c'        
            
        #Makes sure the file doesn't already exist
        if not os.path.exists(self.filepath):
            
            #Writes contents to text file
            f = open(self.filepath, 'w+')
            f.write(contents)
            f.close()
            self.master2.destroy()
            
            if rerun:
                self.Run()
            
        else:
            self.label2.config(text='That file already exists')

    def Open(self):
        self.filepath = self.entry2.get()

        if self.filepath[len(self.filepath) - 2:] != '.c':
            self.filepath += '.c'        
            
        if os.path.exists(self.filepath):
            f = open(self.filepath)
            filetext = f.read()
            self.text.TextBox.insert(tkinter.END, filetext)
            f.close()
            self.master2.destroy()

            for i in range(1, len(self.text.TextBox.get("1.0", tk.END).split('\n')) + 1):
                
                self.text.TextBox.mark_set("insert", str(i) + '.0')
                self.text.starthighlight()

        else:
            self.filepath = None
            self.label2['text'] = "That file doesn't exist"
            
    def Opennew(self):
        self.popup(self.Open, 'Open')
        self.text.TextBox.delete(1.0,tk.END)
        
    def Exit(self):
        msgbox = tkinter.messagebox.askquestion('Exit', 'Would you like to save first')

        if msgbox == 'yes':
            self.Save()

        self.master.destroy()

    def Undo(self):
        self.text.TextBox.edit_undo()

    def Redo(self):
        self.text.TextBox.edit_redo()

    def Run(self, e=1):
        if self.filepath == None:
            self.popup(lambda: self.Save_as(True), 'Save As')
            
        else:
            split = self.filepath.rsplit('\\', 1)
            exe = split[1][:len(split[1]) - 2] + '.exe'

            command = 'cd ' + split[0] + ' && gcc ' + split[1] + ' -o ' + exe
            p = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            error = p.communicate()[1].decode("utf-8")
            if error != '':
                self.master3 = tk.Tk()
                self.master3.title('Error')

                label = tk.Label(self.master3, bg='white', fg='black', text=error).pack(side=tk.TOP)

                button = tk.Button(self.master3, text='ok', bg='white', fg='black', command=lambda: self.master3.destroy()).pack(side=tk.LEFT)
            else:
                time.sleep(1)
                os.system('cmd /k ' + self.filepath[:len(self.filepath) - 2])
                os.remove(self.filepath[:len(self.filepath) - 2] + '.exe')

    def savenrun(self):
        self.Save()
        self.Run()

    def findindex(self):
        theindex = self.entry2.get()

        self.text.TextBox.mark_set("matchStart", theindex)
        self.text.TextBox.mark_set("matchEnd", "%s+%sc" % (theindex, 1))
        self.text.TextBox.tag_add('highlight', "matchStart", "matchEnd")

        self.text.TextBox.mark_set("insert", theindex)
        self.text.TextBox.see("insert")

        self.master2.destroy()


    def google(self, url):
        webbrowser.open(url)

    

class TextInput():
    def __init__(self, master, text=None):
        self.master = master
        self.previousContent = ''
        self.functions = ['printf', 'scanf', 'getchar', 'putchar']            
        self.types = ['int', 'char', 'float', 'double', 'void']
        self.stringstarts = ['"']
        self.comments = ['/*', '*/']
        self.keywords = ['if', 'else', 'for', 'while', 'do', '#include', '#define', 'break', 'return']
        
        self.mylist = [
            [self.functions, lambda x: r'%s(?=[\(\s])' % x, "functions"],
            [self.stringstarts, lambda x: r'".+?"', "strings"],
            [self.comments, lambda x: r'\/*.+?\*\/', "strings"],
            [self.types + self.keywords, lambda x: r'%s(?=[\(\s<])' % x, "types"],
        ]

        self.scrollbar = tk.Scrollbar(self.master)
        self.TextBox = tk.Text(self.master, bg='#1e1f29', fg='white', font=("Courier", 14), insertbackground='white', undo=True, yscrollcommand=self.scrollbar.set)

        auto = '''#include <stdio.h>
 
int main() {

  printf("Hello World\\n");
  return 0;

};'''
        self.TextBox.insert(tk.END, auto)        
        self.starthighlight(alll=True)

        if text != None:
            pass
        
        self.TextBox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        
        self.scrollbar.config(command=self.TextBox.yview)
        self.TextBox.focus_set()

        self.xy = tk.Label(self.TextBox, width=10, borderwidth=1, relief="solid", text='1.0', bg='white')
        self.xy.place(relx=1.0, rely=1.0, x=-2, y=-50, anchor="se")
        
        font = tkinter.font.Font(font = self.TextBox['font'])  
        tab_width = font.measure(' ' * 2)  
        self.TextBox.config(tabs=(tab_width,))

        self.TextBox.bind('<Key>', self.cursorpos)
        self.TextBox.bind('<KeyPress-Tab>', self.tabtext)
        self.TextBox.bind('<KeyRelease>', self.starthighlight)

        self.TextBox.tag_configure("functions", foreground="#aca6f4")
        self.TextBox.tag_configure("types", foreground="#6bdde5")
        self.TextBox.tag_configure("strings", foreground="#cbf4a6")
        self.TextBox.tag_configure("names", foreground="green")
        self.TextBox.tag_configure("comments", foreground="black")
        self.TextBox.tag_configure("highlight", background="white", foreground="black")

        for i in range(1, len(self.TextBox.get("1.0", tk.END).split('\n')) + 1):                
            self.TextBox.mark_set("insert", str(i) + '.0')
            self.starthighlight()


    def cursorpos(self,e):
        self.TextBox.tag_delete('highlight')
        pos = self.TextBox.index(tk.INSERT)
        self.xy['text'] = pos

    def tabtext(self, e=None):
        # Adds indentation to all selected text
        try:
            untabbed = self.TextBox.selection_get()
            lines = untabbed.split('\n')
            index = self.TextBox.index("sel.first linestart")
            
            for i in range(len(lines) - 1):
                lines[i] = '  ' + lines[i]

            tabbed = '\n'.join(lines)

            old = self.TextBox.get("1.0", tk.END)
            new = old.replace(untabbed, tabbed)
            self.TextBox.delete("sel.first linestart", "sel.last linestart")
            self.TextBox.insert(index, tabbed)

            return 'break'
        
        except:
            return None

    def starthighlight(self, e=None, alll=None):
        content = self.TextBox.get("1.0", tk.END)
        lines = content.split("\n")
        
        self.row = int(self.TextBox.index(tk.INSERT).split('.')[0])
        if alll == None:
            start = self.TextBox.index(str(self.row) + '.0')
            end = self.TextBox.index(str(self.row+1) + '.0')
            self.line = lines[self.row - 1]

        else:
            start = self.TextBox.index('1.0')
            end = self.TextBox.index(tk.END)
            self.line = self.TextBox.get('1.0', tk.END)
            
        self.TextBox.mark_set("matchStart", start)
        self.TextBox.mark_set("matchEnd", start)
        self.TextBox.mark_set("searchLimit", end)

        for i in self.TextBox.tag_names():
            self.TextBox.tag_remove(i, str(self.row) + '.0', str(self.row+1) + '.0')

        for i in self.mylist:
            self.highlight_pattern(i)

    def highlight_pattern(self, listt):
        for item in listt[0]:
            if item in self.line:
                count = tk.IntVar()
                #listt[1](item)
                while True:
                    index = self.TextBox.search(listt[1](item), "matchEnd","searchLimit",
                                        count=count, regexp=True)
                    if index == "" or count.get() == 0:
                        break #string not found
                    self.TextBox.mark_set("matchStart", index)
                    self.TextBox.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
                    self.TextBox.tag_add(listt[2], "matchStart", "matchEnd")

if __name__ == "__main__":

    StartApp()
