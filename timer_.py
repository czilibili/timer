import datetime
import threading
import time
from tkinter import * 
from tkinter import messagebox
from PIL import Image, ImageTk


class App(Tk):
        
    def createMenu(self):
         
        self.menuBar = Menu(master=self)
         
        self.filemenu = Menu(
        self.menuBar, 
        tearoff=0,
        title='Some Title'
        )
        
        self.filemenu.add_command(
        label="Minutnik",
        )
        
        self.filemenu.add_command(
        label="Rejestrator",
        )
        
        self.filemenu.add_command(
        label="Save and quit",
        command=self.saveQuit,
        )
        
        self.filemenu.add_command(
        label="Quit", 
        command=self.quit,
        )
        
        self.menuBar.add_cascade(
        label="File",
        menu=self.filemenu,
        )
        
    ## Menu functions ##
    def saveQuit(self):
        return 
                
    def createCanvas(self):
        ## Create canvas ##
        # create
        self.canvas = Canvas(
        master=self,
        height=300, 
        width=300,
        bg="#a3c2c2"
        )
        # visible it
        # self.canvas.pack()
        # try grid
        self.canvas.grid()
     
    def createFrameButtons(self):
        
        ## create frame to place buttons in
        self.frame_buttons = Frame(
        master=self, 
        
        padx="10",
        pady="10",
        )
        self.frame_buttons.grid(
        row=1)
        
    def createButtons(self):
        
        ## Button starting a counter, linked to label_controller ##
        # create
                
        ## Prep images with Pillow 
        
        start_pil = Image.open('play.gif')
        pause_pil = Image.open('pause.gif')
        end_pil = Image.open('stop.gif')
        dim = (50, 50)
        
        start_img = start_pil.resize(dim)
        pause_img = pause_pil.resize(dim)
        end_img = end_pil.resize(dim)
        
        start_tk = ImageTk.PhotoImage(start_img)
        pause_tk = ImageTk.PhotoImage(pause_img)
        end_tk = ImageTk.PhotoImage(end_img)
            
        ## Rinse buttons
        
        # Start button
        self.start_button = Button(
        image=start_tk,
        master=self.frame_buttons,
        text="Start", 
        #bg="orange", 
        #fg="blue",
        command=self.label_controller,
        )
                   
        self.start_button.image = start_tk
        self.start_button.configure(image=start_tk)
        
        self.start_button.grid(
        row=1, 
        column=0,
        padx=15,
        #sticky=W
        )
        
        # Pause button
        self.pause_button = Button(
        image=pause_tk,
        master=self.frame_buttons,
        text="Pause",
        #bg="blue",
        #fg="orange",
        command=self.pause_counter)
        # button
        self.pause_button.image = pause_tk 
        self.pause_button.configure(image=pause_tk)
        # visible it
        self.pause_button.grid(
        row=1,
        column=1,
        padx=15,
        #sticky=W,
        )
        
        # Finish button
        self.end_button = Button(
        image=end_tk,
        master=self.frame_buttons,
        text="Finish",
        #bg="blue",
        #fg="orange",
        command=self.finish_counter)
        # button
        self.end_button.image = end_tk 
        self.end_button.configure(image=end_tk)
        
        # visible it
        self.end_button.grid(
        row=1,
        column=2,
        padx=15,
        #sticky=W,
        )
        
    def createLabels(self):
        
        ## Label displaying actual counter state ##
        # set default text
        self.text = StringVar()
        self.text.set("00:25:00")
        # create 
        self.label = Label(

        textvariable=self.text,
        font=("Helvetica", 50),
        )
        # visible it
        self.label.grid(
        row=0,
        )
    
    def createSBFrame(self):
        self.sbframe = Frame(
        master=self,
        )
        
        self.sbframe.grid(
        row=3,
        )


    def createSpinBoxes(self):
        ## Create time spinboxes ##
        
        # Hours
        self.sb_hours = Spinbox(
        master=self.sbframe, 
        from_=0,
        to=23,
        width=2,
        font=("Helvetica", 20),
        )
        self.sb_hours.grid(
        row=3,
        column=0
        )
        
        # Minutes
        self.sb_minutes = Spinbox(
        master=self.sbframe,
        from_=0,
        to=59,
        width=2,
        font=("Helvetica", 20),
        )
        self.sb_minutes.grid(
        row=3,
        column=1,
        )
        self.sb_minutes.delete(0, 'end') 
        self.sb_minutes.insert(0, '25')

        # Seconds
        self.sb_seconds = Spinbox(
        master=self.sbframe,
        from_=0,
        to=59,
        width=2,
        font=("Helvetica", 20),
        )
        self.sb_seconds.grid(
        row=3,
        column=2,
        )
        
    def createWidgets(self):
        self.createMenu()
        self.createFrameButtons()
        self.createSBFrame()
        self.createButtons()
        self.createLabels()
        self.createSpinBoxes()
        
    def __init__(self):
            
        ## Inherit ##
        Tk.__init__(self)
        
        self.title('timer')

        ## Widgets call ##
        self.createWidgets()
        
        
        # create menu
        self.config(menu=self.menuBar)
        
        ## Counter flags ##
        self.paused = False
        self.finished = False
        self.resumed = False

    def label_controller(self):
        
        ## Threading module controls idleness of _label_update process. ##
        # As there are time delays and loops(tkinter fx just doesn't work),
        # to keep app responsive need to control threads
        
        thread_1 = threading.Thread(target=self._label_update)
        thread_1.start()
        
    def _label_update(self):
        
        # Was it resumed? 
        
        if self.resumed:
            
            # get time from last label, and convert it to time obj
            # to get clean data
            # it could be some var but why to double?
            # when it's already stored

            time_obj = datetime.time.fromisoformat(self.text.get())
            hour = int(time_obj.hour)
            minute = int(time_obj.minute)
            second = int(time_obj.second)
            self.resumed = False 
    
        else:
        
            # read spinboxes
            hour = int(self.sb_hours.get())
            minute = int(self.sb_minutes.get())
            second = int(self.sb_seconds.get())
             
        # Deactivate flags
        self.finished = False
        self.paused = False
        
        # MessageBox controller
        uninterrupted = True

        # Disable button to prevent adding new events to mainloop
        self.start_button.config(state="disabled")
                   
        # timer loop
        for count in self.timer(hour, minute, second):
            if self.paused:
                # new instance controller
                self.resumed = True
                # now, if button is enabled new events are added to mainloop
                # it means that current one has to be killed
                # new one has to be started with label read as a start value
                # otherwise there be multiple instances of this fx
                # and all of them want to change the same label 
                self.start_button.config(state="normal")

                while self.paused:
                    time.sleep(0.1)
                    if self.finished:
                        uninterrupted = False
                        break
                else:
                    uninterrupted = False
                    return None
                    
            if self.finished:
                uninterrupted = False
                break
            self.text.set(count)
            self.label.config(textvariable=self.text)
            self.title(count)
                        
            # update_idletasks doesn't work properly inside this loop
            # i.e. counter works, but once you minimize app
            # it only displays counter
            # else it's not possible to close it
            # has to use a threading module to process this fx
            # and it works
            
            #self.label.update_idletasks()

        # Message when counter finishes automatically
        if uninterrupted:
            messagebox.showinfo("Powiadomienie", "Koniec czasu")

        # Restore normal state of start button            
        self.start_button.config(state="normal")
        # and title...
        self.title('timer')
        # finally reset counter
        self.text.set(self._format_ui())  
        return None

    # Do time computations
    def timer(self, hours, minutes, seconds):
            
        seconds_sum = hours * 3600 + minutes * 60 + seconds
        
        if seconds_sum:
            for second in range(seconds_sum, 0, -1):
                time.sleep(1)
                seconds_sum -= 1
                hour = seconds_sum // 3600 % 24
                minute = seconds_sum // 60 % 60
                second = seconds_sum % 60
                yield datetime.time(hour, minute, second).isoformat()
        else:
            return
        
        return
    
    ## Flag controllers

    def pause_counter(self):
        self.paused = True

    def finish_counter(self):
        self.finished = True

    ## Time formatter ##
    def _format_ui(self):
        ## Take number and convert it to a time object.
        
        return datetime.time(
        int(self.sb_hours.get()),
        int(self.sb_minutes.get()),
        int(self.sb_seconds.get())
        ).isoformat()

    def _reformat_ui(self, ui):
        ## Take striing time object and convvert it to a number
        dt = datetime.time.fromisoformat(ui)
        hours = dt.hour * 3600
        minutes = dt.minute * 60
        seconds = dt.second
        return hours + minutes + seconds
    
   
app = App()
app.mainloop()    
