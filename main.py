
import win32api, time, os, json


from concurrent.futures.thread import ThreadPoolExecutor


from tkinter import Frame, Button, Entry, Spinbox, Listbox, Toplevel, Checkbutton, BOTH, Tk, IntVar, StringVar, END, SINGLE, ACTIVE, RIGHT, ANCHOR

from functions import keyboard_keys,  execute_macro, get_click_positions



class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.number_of_clicks= IntVar()
      

        #   although we run the macro instructions from a string in the entry box, we are going to load the current saved macros
        #   so we can use the already saved macros
        with open('macros.json', 'r') as macros:

            self.saved_macro_list= json.load(macros)
 
        self.init_window()
              
        

    def init_window(self):
        self.master.title("Metin2 Trash remover")

        self.pack(fill=BOTH, expand=1)



       

        self.key_listbox= Listbox(self, selectmode=SINGLE)
        self.key_listbox.pack()
        #we initialize the listbox with the valid keycodes provided by pydirectinput
        for key in keyboard_keys:
            self.key_listbox.insert(END, key)

        #saved macros list
        self.macro_listbox= Listbox(self, selectmode=SINGLE)

        self.macro_listbox.bind("<<ListboxSelect>>", self.update_current_macro)
        self.macro_listbox.pack()
        for macro in self.saved_macro_list["macros"]:
            self.macro_listbox.insert(END, macro)


        #macro instructions entry
        self.instructions= Entry(self)
        self.instructions.pack(side="top", expand=True)
        

        self.macro_name_entry=Entry(self)
        self.macro_name_entry.pack()



        self.run_button= Button(self,text="Run", command=self.save_macro)
        self.run_button.pack()

        self.delete_macro_button= Button(self,text="Delete Macro", command=self.delete_macro)
        self.delete_macro_button.pack()

                                                    #i need the coma only show up when there is something in the instructions entry
                                                    # we can do this multiplying the comma by an TRUE or FALSE statement, lets check if ':' is in the entry box
        self.key_down= Button(self,text="key_down", command= lambda: self.instructions.insert(END,','*(':' in self.instructions.get()) + f'"key_down":"{self.key_listbox.get(ANCHOR)}"'))
        self.key_down.pack()
                                                   
        self.key_up= Button(self,text="key_up", command= lambda: self.instructions.insert(END,','*(':' in self.instructions.get()) + f'"key_up":"{self.key_listbox.get(ANCHOR)}"'))
        self.key_up.pack()


        self.press= Button(self,text="press", command= lambda: self.instructions.insert(END,','*(':' in self.instructions.get()) + f'"press":"{self.key_listbox.get(ANCHOR)}"'))
        self.press.pack(side=RIGHT)



        self.number_of_clicks_spinbox= Spinbox(self,from_=1, to=100, width=3, textvariable=self.number_of_clicks)
        self.number_of_clicks_spinbox.place(x=21, y=52)

        self.left_click= Button(self, text="Left Click", command= lambda: self.get_clicks("left_button", int(self.number_of_clicks.get())))
        self.left_click.pack(side="left")


        self.middle_click= Button(self, text="Middle Click", command= lambda: self.get_clicks("right_button", int(self.number_of_clicks.get())))
        self.middle_click.pack(side="left")
               
        self.right_click= Button(self, text="Right Click", command= lambda: self.get_clicks("right_button", int(self.number_of_clicks.get())))
        self.right_click.pack(side="left")


        
 
               
 
        #self.trash_button= Button(self,text="Items to delete", command=self.selector_popup)
     


    

    def execute_m(self):
        with ThreadPoolExecutor(max_workers=1) as executor:
     
            instructions_dict= json.loads(f"{{{self.instructions.get()}}}".lower().strip())
       
            macro_f= executor.submit(execute_macro, instructions_dict)
            macro_f.done()

        
    def save_macro(self):

        with open('macros.json', 'r') as configfile:
            json_dict = json.load(configfile)


        with open('macros.json', 'w') as configfile:                        #json expects doublequoted keys
            macro_instructions =json.loads(f'{{{self.instructions.get()}}}'.replace("\'","\""))
            macro_name=self.macro_name_entry.get()
            json_dict["macros"][macro_name]=macro_instructions
            json.dump(json_dict, configfile)

        #now we insert the macro name in the list and update the saved macro list 
        self.macro_listbox.insert(END, macro_name)
        self.saved_macro_list["macros"][macro_name]=macro_instructions

         
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
            self.instructions.delete(0,END)


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
            #delete the contents of the macro name entry and the replace the macro instructions
            self.macro_name_entry.delete(0, END)
            self.macro_name_entry.insert(END, macro_name)

            self.instructions.delete(0,END)
                                          
            instruction_str=  f'{self.saved_macro_list["macros"][macro_name]}'
           
                                        #remove curly braces so it fits the instructions format
            self.instructions.insert(END, instruction_str[1:-1])



    def get_clicks(self, button, clicks):
        print(button,clicks)
        with ThreadPoolExecutor() as executor:
            click_func=executor.submit(get_click_positions, button, clicks)

            self.instructions.insert(END,','*(':' in self.instructions.get()) + f'"click":"{click_func.result()}"')






if __name__ == '__main__':   
    root = Tk()

    root.geometry("500x300")
    app = Window(root)

    root.mainloop()