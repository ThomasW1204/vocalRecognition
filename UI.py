import customtkinter as ctk
import pyautogui



class UI(ctk.CTk):
    def __init__(self,ai):
        
        self.ai = ai
        super().__init__()
        self.title("Assistant UI")
        self.geometry("400x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

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

 





