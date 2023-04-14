import customtkinter

### Sidebar of the app ###
class Sidebar(customtkinter.CTkFrame):
    def __init__(self, master, participate,raid_active,feed_frame, seeds_frame ,**kwargs):
        super().__init__(master, **kwargs)
        # self.change_theme_event = change_theme
        self.participate_event = participate
        self.is_raiding = raid_active
        self.feed_frame = feed_frame
        self.seeds_frame = seeds_frame
        
        # Sidebar Title
        self.logo_label = customtkinter.CTkLabel(self, text="Fitnate", font=customtkinter.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Sidebar Main Button (Participate)
        self.sidebar_button_1 = customtkinter.CTkButton(
                                        self, 
                                        text='Participate' if not self.is_raiding else 'Stop',
                                        command=self.main_event,
                                        fg_color='#30E399' if not self.is_raiding else 'red',
                                        text_color='black',
                                        hover=False
                                    )
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        
        # Sidebar Discovery Label
        self.discovery_label = customtkinter.CTkLabel(self, text="Sending seeds..." if self.is_raiding else "Raid is stopped", 
                                                      anchor="w",font=customtkinter.CTkFont(size=13, weight="bold")
                                                      )
        self.discovery_label.grid(row=2, column=0, padx=20, pady=(10, 0))
        
        # Sidebar Discovery loader
        self.discovery_loader = customtkinter.CTkProgressBar(self)
        self.discovery_loader.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.discovery_loader.configure(mode="indeterminnate")
        if self.is_raiding:
            self.discovery_loader.start()
            
        # Sidebar Clear Buttons
        self.clear_seeds = customtkinter.CTkButton(self, text="Clear Logs", command=self.clear_seeds_event)
        self.clear_seeds.grid(row=4, column=0, padx=20, pady=(10, 0))
        
        self.clear_feed = customtkinter.CTkButton(self, text="Clear Anouncements", fg_color='#2f614c', command=self.clear_feed_event)
        self.clear_feed.grid(row=5, column=0, padx=20, pady=(10, 0))
        
        # Sidebar Settings for Theme
        self.appearance_mode_label = customtkinter.CTkLabel(self, text="Theme:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionmenu = customtkinter.CTkOptionMenu(self, values=["Dark", "Light", "System"],
                                                                       command=self.change_theme_event)
        self.appearance_mode_optionmenu.grid(row=7, column=0, padx=20, pady=(10, 10))
        

    def change_theme_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
    
    def clear_seeds_event(self):
        for widget in self.seeds_frame.winfo_children():
            widget.destroy()
            
        cleared_label = customtkinter.CTkLabel(self.seeds_frame, text="Logs cleared", text_color="gray")
        cleared_label.pack()
            
    def clear_feed_event(self):
        for widget in self.feed_frame.winfo_children():
            widget.destroy()
            
        cleared_label = customtkinter.CTkLabel(self.feed_frame, text="cleared", text_color="gray")
        cleared_label.pack()
            
    
    def main_event(self):
        self.is_raiding = not self.is_raiding
        if self.is_raiding:
            self.sidebar_button_1.configure(text="Stop",fg_color='red',text_color='white')
            self.discovery_label.configure(text="Sending seeds...")
            self.discovery_loader.start()
        else:
            self.sidebar_button_1.configure(text="Participate",fg_color='#30E399',text_color='black')
            self.discovery_loader.stop()
            self.discovery_label.configure(text="Raid stopped")
        self.participate_event()
