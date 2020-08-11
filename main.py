
import win32api, time, os, json


from concurrent.futures.thread import ThreadPoolExecutor


from tkinter import (Frame, Tk, 
                    Button, Entry,Text, Spinbox, Listbox, Label, Checkbutton,
                    messagebox,
                    IntVar, StringVar, 
                    END, SINGLE, ACTIVE, RIGHT, ANCHOR,BOTH,NORMAL, N,S,W,E
                    )

from functions import keyboard_keys,  execute_macro, get_click_positions



class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.number_of_clicks= StringVar()
        self.ms_delay=StringVar()

        #   although we run the macro instructions_entry from a string in the entry box, we are going to load the current saved macros
        #   so we can use the already saved macros
        with open('macros.json', 'r') as macros:
            self.saved_macro_list= json.load(macros)
 
        self.init_window()
              
        

    def init_window(self):
        self.master.title("Macro Tool")

        self.pack(fill=BOTH, expand=1)

        self.columnconfigure(1, weight=1)
        self.rowconfigure(1,weight=1)

        ##############################################################
        saved_macro_label = Label(self,text= "Saved Macros")
        saved_macro_label.grid(row=0,column=4)

        #saved macros list
        self.macro_listbox= Listbox(self, selectmode=SINGLE)
        self.macro_listbox.bind("<<ListboxSelect>>", self.update_current_macro)
        self.macro_listbox.grid(row=1, column=4)
        for macro in self.saved_macro_list["macros"]:
            self.macro_listbox.insert(END, macro)



   
        self.save_macro_button= Button(self,text="Save Current Macro", command=self.save_macro)
        self.save_macro_button.grid(row=4, column=4)

        self.delete_macro_button= Button(self,text="Delete Macro", command=self.delete_macro)
        self.delete_macro_button.grid(row=5, column=4)

        ##############################################################
       




        ##############################################################

        instructions_label=Label(self, text= "Macro Instructions")
        instructions_label.grid(row=0,column=1)

        self.instructions_entry=Text(self)
        self.instructions_entry.grid(row=1, column=1,sticky="news")
        self.instructions_entry.config(state=NORMAL)

        macro_name_label = Label(self,text= "Macro Name")
        macro_name_label.grid(row=2,column=1)

        self.macro_name_entry=Entry(self)
        self.macro_name_entry.grid(row=3, column=1)

        self.run_button=Button(self,text="Run Macro", command=self.run_macro)
        self.run_button.grid(row=4,column=1)


        
        ##############################################################
        
        keys_label= Label(self, text= "Keys")
        keys_label.grid(row=0,column=0)
        self.key_listbox= Listbox(self, selectmode=SINGLE)
        self.key_listbox.grid(row=1,column=0)
        #we initialize the listbox with the valid keycodes provided by pydirectinput
        for key in keyboard_keys:
            self.key_listbox.insert(END, key)

       

        key_frame=Frame(self)
        key_frame.grid(row=2,column=0)


                                                    #i need the + sign only show up when there is something in the instructions_entry entry
                                                    # we can do this multiplying the + sign by an TRUE or FALSE statement, lets check if ':' is in the entry box
        self.key_down= Button(key_frame,text="key_down", command= lambda: self.instructions_entry.insert(END,'+ '*(':' in self.instructions_entry.get("1.0","end-1c")) + f'key_down: {self.key_listbox.get(ANCHOR)} '))
        self.key_down.grid(row=0,column=0)
                                                   
        self.key_up= Button(key_frame,text="key_up", command= lambda: self.instructions_entry.insert(END,'+ '*(':' in self.instructions_entry.get("1.0","end-1c")) + f'key_up:{self.key_listbox.get(ANCHOR)}'))
        self.key_up.grid(row=0,column=1)


        self.press= Button(self,text="press", command= lambda: self.instructions_entry.insert(END,'+ '*(':' in self.instructions_entry.get("1.0","end-1c")) + f'press:{self.key_listbox.get(ANCHOR)}'))
        self.press.grid(row=3,column=0)


        delay_frame= Frame(self)
        delay_frame.grid(row=5,column=0)

        delay_text=Label(delay_frame, text="Delay(ms)")
        delay_text.grid(row=0,column=0)
        self.delay_entry = Entry(delay_frame, textvariable=self.ms_delay, width=10)
        self.delay_entry.grid(row=0,column=1)
        #default delay value
        self.delay_entry.insert(END,"100")

        ##############################################################

        clicks_frame=Frame(self)
        clicks_frame.grid(row=4,column=0)

        
        self.number_of_clicks_spinbox= Spinbox(clicks_frame, from_=1, to=100, width=3, textvariable=self.number_of_clicks)
        self.number_of_clicks_spinbox.grid(row=0,column=1)

        self.left_click= Button(clicks_frame, text="Left Click", command= lambda: self.get_clicks("left_click", int(self.number_of_clicks.get())))
        self.left_click.grid(row=0,column=2)


        self.right_click= Button(clicks_frame, text="Right Click", command= lambda: self.get_clicks("right_click", int(self.number_of_clicks.get())))
        self.right_click.grid(row=0,column=3)

        ##############################################################

    

    def run_macro(self):
        #validate ms delay entry can be converted to int, else raise error.
        ms_delay=False
        try:
            ms_delay= int(self.delay_entry.get())/1000

        except ValueError:
            messagebox.showerror("Error", "Delay must be an integer") 

        if ms_delay:
            with ThreadPoolExecutor(max_workers=1) as executor:
                instructions_text=self.instructions_entry.get('1.0',"end-1c").replace(' ', '')

                                  #string formatting, example: 'key_down: g + key_down: g' -->>> [['key_down', ' g '] + ['key_down', ' g']]
                intructions_list= [instruction.split(':') for instruction in instructions_text.split('+')]

                macro_f= executor.submit(execute_macro, intructions_list, ms_delay)
                macro_f.done()

        
    def save_macro(self):
        #check if we have a macro name
        if self.macro_name_entry.get() != '':

            with open('macros.json', 'r') as configfile:
                json_dict = json.load(configfile)


            with open('macros.json', 'w') as configfile:                       
                instructions_string =self.instructions_entry.get("1.0","end-1c")
                print(instructions_string)
                macro_name=self.macro_name_entry.get()
                # if the macro exist already, we dont want to put it again in the saved macro list
                if macro_name not in json_dict["macros"]:
                    self.macro_listbox.insert(END, macro_name)

                json_dict["macros"][macro_name]=instructions_string
                json.dump(json_dict, configfile)

            #now we update the saved macro list 
            self.saved_macro_list["macros"][macro_name]=instructions_string


        else:
            messagebox.showerror("Error", "Empty Macro Name") 

         
    def delete_macro(self):
        macro_name=self.macro_listbox.get(ANCHOR)
        #ANCHOR is '' if nothing is selected
        if macro_name is not '':
            macro_index = self.macro_listbox.get(0,END).index(macro_name)
            self.macro_listbox.delete(macro_index)
            #This will return my_dict[key] if key exists in the dictionary, and None otherwise. If the second
            self.saved_macro_list.pop(macro_name,None)

            #clen the entrys
            self.macro_name_entry.delete(0, END)
            self.instructions_entry.delete(0,END)


            #for now lets update the macros.json file until i find a reliable way to save the macros file when you close the window
            with open('macros.json', 'r') as configfile:
                json_dict = json.load(configfile)


            with open('macros.json', 'w') as configfile:                       
                json_dict["macros"].pop(macro_name, None)
                json.dump(json_dict, configfile)




    #bind sends an event argument, but we are using self to retrieve values from the widget, i dont think this is a good practice 
    def update_current_macro(self, _):
        #get(ACTIVE) get the item that was active before the click
        macro_name=self.macro_listbox.get(ANCHOR)
        
        if macro_name in self.saved_macro_list["macros"]:
            #delete the contents of the macro name entry and the replace the macro instructions_entry
            self.macro_name_entry.delete(0,END)
            self.macro_name_entry.insert(END, macro_name)

            self.instructions_entry.delete('1.0',"end-1c")
                                          
            instruction_str=  f'{self.saved_macro_list["macros"][macro_name]}'
           
                                        
            self.instructions_entry.insert(END, instruction_str)



    def get_clicks(self, button, clicks):
      
        with ThreadPoolExecutor() as executor:
            click_func=executor.submit(get_click_positions, button, clicks)

            self.instructions_entry.insert(END,'+ '*(':' in self.instructions_entry.get("1.0",END)) + f'{button}:{click_func.result()}')






if __name__ == '__main__':   
    root = Tk()

    root.geometry("500x300")
    app = Window(root)

    root.mainloop()