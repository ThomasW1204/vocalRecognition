
import os
import subprocess
import time
import customtkinter as ctk
import pyautogui
from PIL import Image, ImageTk  # Correct import


class UI(ctk.CTk):
    def __init__(self,ai):
        
        self.ai = ai
        super().__init__()
        self.title("Assistant UI")
        self.geometry("400x600")
        ctk.set_appearance_mode("dark")
    
        ctk.set_default_color_theme("blue")

      

            # === Add Tabview ===
        self.tabview = ctk.CTkTabview(self, corner_radius=10)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)

        # Create tabs
        self.chat_tab = self.tabview.add("Chat")
        self.actions_tab = self.tabview.add("Quick Actions")
        self.logs_tab = self.tabview.add("Logs")



 # --- CHAT PAGE CONTENT ---
        self.chat_frame = ctk.CTkFrame(self.chat_tab, corner_radius=10)
        self.chat_frame.pack(fill="both", expand=True)
        
        self.chat_frame.grid_columnconfigure(0, weight=1)
        self.chat_frame.grid_rowconfigure(1, weight=1)
        
        
        
        # Chat frame with transparent background
       


        self.topLabel()
        self.createScrollFrame()
        self.textBox()
        self.sendButton()

        # --- Quick Actions PAGE CONTENT ---
        self.actions_frame = ctk.CTkFrame(self.actions_tab, corner_radius=10)
        self.actions_frame.pack(fill="both", expand=True, padx=10, pady=10)
        #self.set_tab_bg(self.actions_frame, r"C:\Users\tmarv\Desktop\VocalRecog\vocalRecognition\126008721_p0_master1200.jpg")

        action1 = ctk.CTkButton(self.actions_frame, text="Start Task", command=lambda: self.log("Started Task"))
        action1.pack(pady=5)

        action2 = ctk.CTkButton(self.actions_frame, text="Stop Task", command=lambda: self.log("Stopped Task"))
        action2.pack(pady=5)

        action3 = ctk.CTkButton(self.actions_frame, text="Run Command", command=lambda: self.log("Command executed"))
        action3.pack(pady=5)






        # --- ABOUT PAGE CONTENT ---
        self.logs_textbox = ctk.CTkTextbox(self.logs_tab, width=400, height=500, state="disabled")
        self.logs_textbox.pack(padx=10, pady=10, fill="both", expand=True)

        self.logs_frame = ctk.CTkFrame(self.logs_tab, corner_radius=10)
        self.logs_frame.pack(fill="both", expand=True, padx=10, pady=10)

        

   


    def log(self, message):
        def _append():
            self.logs_textbox.configure(state="normal")
            self.logs_textbox.insert("end", f"{message}\n")
            self.logs_textbox.configure(state="disabled")
            self.logs_textbox.see("end")
        self.after(0, _append)


    

    def force_focus(self):
        self.update()
        self.deiconify()
        self.lift()
        self.wm_attributes("-topmost", 1)
        self.position_right_middle()
        self.after(500, lambda: self.wm_attributes("-topmost", 0))
        self.after(100, lambda: self.entry.focus_force())

    def topLabel(self):
        self.label = ctk.CTkLabel(self.chat_frame, text="Type to the AI!")
        self.label.grid(row=0, column=0, pady=(20, 10), sticky="n")

    def createScrollFrame(self):
        self.scrollable_frame = ctk.CTkScrollableFrame(self.chat_frame, height=450)
        self.scrollable_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
        self.scrollable_frame._parent_canvas.yview_moveto(1.0)

    def textBox(self):
        self.entry = ctk.CTkEntry(self.chat_frame, placeholder_text="Type here...")
        self.entry.grid(row=2, column=0, pady=10, sticky="sew")
        self.entry.bind("<Return>", lambda event: self.send())

    def sendButton(self):
        self.button = ctk.CTkButton(self.chat_frame, text=">", command=self.send)
        self.button.grid(row=2, column=1, pady=10, sticky="sew")

    def send(self):
        input_text = self.entry.get()
        if not input_text.strip():
            return
        print(input_text)
        self.dynamicpanels(input_text)
        self.aireply(input_text)
        self.entry.delete(0, "end")

    def dynamicpanels(self, input_text):
        panel = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)
        panel.pack(fill="x", padx=10, pady=5)

        label = ctk.CTkLabel(panel, text=input_text, anchor="w", wraplength=360)
        label.pack(padx=10, pady=10, fill="x")
        self.after(2, lambda: self.scrollable_frame._parent_canvas.yview_moveto(1.0))

    def aireply(self, input_text):
        panel = ctk.CTkFrame(self.scrollable_frame, corner_radius=10, fg_color="grey")
        panel.pack(fill="x", padx=10, pady=5)
        airesponse = self.ai.askAI(input_text)

        label = ctk.CTkLabel(panel, text=airesponse, anchor="w", wraplength=360)
        label.pack(padx=10, pady=10, fill="x")
        self.after(2, lambda: self.scrollable_frame._parent_canvas.yview_moveto(1.0))

    def position_right_middle(self):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        x = screen_width - window_width
        y = (screen_height // 2) - (window_height // 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")



    '''
        # Create main frame
        self.main_frame = ctk.CTkFrame(master=self, corner_radius=10)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Configure column
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)  # Scrollable frame - expands
        self.main_frame.grid_rowconfigure(2, weight=0)  # Entry - no stretch
       
        # Configure rows to allow vertical stretch
        for i in range(3):
            self.main_frame.grid_rowconfigure(i, weight=1)

        self.topLabel()
        self.createScrollFrame()
        self.textBox()
        self.sendButton()
        self.after(100, self.force_focus)
    
    def force_focus(self):
        self.update()
        self.deiconify()
        self.lift()
       

        self.wm_attributes("-topmost", 1)
        self.position_right_middle()
        self.click_entry_with_mouse()
       
        self.after(500, lambda: self.wm_attributes("-topmost", 0))

        self.after(100, lambda: self.entry.focus_force())

    def click_entry_with_mouse(self): #click into the frame for auto typing
        screen_width, screen_height = pyautogui.size()
        x = screen_width - (self.winfo_width() // 2)  
        y = screen_height // 2

        pyautogui.moveTo(x, y, duration=0.2)
        pyautogui.click()

    def topLabel(self):
        self.label = ctk.CTkLabel(self.main_frame, text="Type to the AI!")
        self.label.grid(row=0, column=0, pady=(20, 10), sticky="n")

    def createScrollFrame(self):
        self.scrollable_frame = ctk.CTkScrollableFrame(self.main_frame, height=450)
        self.scrollable_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
        self.scrollable_frame._parent_canvas.yview_moveto(1.0)
    def textBox(self):
        self.entry = ctk.CTkEntry(self.main_frame, placeholder_text="Type here...")
        self.entry.grid(row=2, column=0, pady=10, sticky="sew")
        self.entry.bind("<Return>", lambda event: self.send()) 

    def sendButton(self):
        self.button = ctk.CTkButton(self.main_frame,text=">", command=self.send)
        self.button.grid(row=2, column=1, pady=10, sticky="sew")

    def send(self):
        input = self.entry.get()
        print(input)
        self.dynamicpanels(input)
        self.aireply(input)
        self.entry.delete(0,"end")

    def dynamicpanels(self,input):
        panel = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)
        panel.pack(fill="x", padx=10, pady=5)

        label = ctk.CTkLabel(panel, text=input, anchor="w", wraplength=360)
        label.pack(padx=10, pady=10, fill="x")
        self.after(2, lambda: self.scrollable_frame._parent_canvas.yview_moveto(1.0))

    def aireply(self,input):
        panel = ctk.CTkFrame(self.scrollable_frame, corner_radius=10,fg_color="grey")
        panel.pack(fill="x", padx=10, pady=5)
        airesponse = self.ai.askAI(input)

        label = ctk.CTkLabel(panel, text=airesponse, anchor="w", wraplength=360) 
        label.pack(padx=10, pady=10, fill="x")
        self.after(2, lambda: self.scrollable_frame._parent_canvas.yview_moveto(1.0))

    def position_right_middle(self): #position the window to the middle right on open
        self.update_idletasks()  

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        window_width = self.winfo_width()
        window_height = self.winfo_height()

        x = screen_width - window_width  
        y = (screen_height // 2) - (window_height // 2)  

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

     '''





