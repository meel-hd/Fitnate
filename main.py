import customtkinter

from server.announcements import  start_the_feed
from widgets.check_network import check_network
from widgets.sidebar import Sidebar
from server.send import start_requests, stop_requests

from config import color_theme, mode,raid_title, raid_description

"""Main file of the app"""

customtkinter.set_appearance_mode(mode)  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(color_theme)  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        # SECTION: Config fo the app
        self.is_raiding = False
        self.sleep_time = 0
        self.clear_at_seed = 40

        # configure window
        self.title("Fitnate")
        self.geometry(f"{1000}x{580}")
        self.minsize(870, 500)
        
        
        # Excluded because it produces an error when running the executable
        # Current fix: change the default icon of customtkinter in its source code (pip show customtkinter)
        # self.iconbitmap("assets/icon.ico")
        

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1,), weight=1)

        # SECTION: Control Tabs
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=1, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Settings") # First tab: we added to it more controls later
        # configure grid of individual tabs
        self.tabview.tab("Settings").grid_columnconfigure(0, weight=1)
        
        # Controls of Settings tab
        self.sleep_label = customtkinter.CTkLabel(self.tabview.tab("Settings"), text="Sleep time (seconds):")
        self.sleep_label.grid(row=0, column=0, padx=20, sticky="w")
        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("Settings"), dynamic_resizing=False,
                                                        values=["0", "1", "3"],
                                                        command=self.change_sleep_time_event
                                                        ) # First control
        self.optionmenu_1.grid(row=1, column=0, padx=20, )
        self.seeds_clear_label = customtkinter.CTkLabel(self.tabview.tab("Settings"), text="Clear at seed number: (hidden after starting)", text_color="red")
        self.seeds_clear_label.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")
        self.combobox_1 = customtkinter.CTkOptionMenu(
                                        self.tabview.tab("Settings"),
                                        values=["40","100","200", "400", "20", "10"],
                                        command=self.change_clear_at_seed_event
                                    ) # Second control
        self.combobox_1.grid(row=3, column=0, padx=20, pady=(0, 10))
        
        self.settings_note_label = customtkinter.CTkLabel(
                    self.tabview.tab("Settings"), 
                    text="Note: For changes to take effect, you should restart the Raid.",
                    font=customtkinter.CTkFont(size=12)
                )
        self.settings_note_label.grid(row=100, column=0, padx=20, pady=(10, 10))

        # SECTION: Stats of the raid
        self.raid_frame = customtkinter.CTkFrame(self)
        self.raid_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.label_radio_group = customtkinter.CTkLabel(master=self.raid_frame, text=raid_title, text_color='orange', font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="w")
        
        self.description_label = customtkinter.CTkLabel(master=self.raid_frame, text=raid_description,font=customtkinter.CTkFont(size=14))
        self.description_label.grid(row=1, column=2, columnspan=1, padx=10, pady=10, sticky="w")

        
        self.seed_count = customtkinter.CTkLabel(master=self.raid_frame, text="0", text_color='#30E399', font=customtkinter.CTkFont(size=34, weight="bold"))
        self.seed_count.grid(row=4, column=2, columnspan=1, padx=10, pady=10, sticky="w")

        # SECTION Live Announcements
        self.announcements_frame = customtkinter.CTkScrollableFrame(self, label_text="Anouncements")
        self.announcements_frame.grid(row=0, column=1, rowspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.announcements_frame.grid_columnconfigure(0, weight=2)
        self.announcements_frame.grid_rowconfigure(4, weight=1)


        # SECTION: Seeds Sent
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Seeds Sent Logs")
        self.scrollable_frame.grid(row=0, column=2, rowspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=0)
        
        # SECTION: create sidebar frame for widgets
        self.sidebar_frame = Sidebar(
                        self,
                        participate=self.participate_event,
                        raid_active= self.is_raiding,
                        width=140,
                        corner_radius=0,
                        feed_frame=self.announcements_frame,
                        seeds_frame=self.scrollable_frame
                    )
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        
        # Set default values
        self.combobox_1.set("40")
        self.stop_feed = start_the_feed(self.announcements_frame)

    def change_sleep_time_event(self,choice):
        self.sleep_time = int(choice)
    
    def change_clear_at_seed_event(self,choice):
        self.clear_at_seed = int(choice)
        
    def participate_event(self):
        # Toggle participation
        self.is_raiding = not self.is_raiding
        if self.is_raiding:
            start_requests(self.scrollable_frame, self.sleep_time, self.clear_at_seed,self.seed_count)
            # Prevent changing seed clear value after starting the raid 
            self.combobox_1.destroy()
            self.seeds_clear_label.destroy()
        else:
            stop_requests()
            
    def stop_feed(self): # This is called when the app is closed to stop the feed thread (announcements)
        print('Not initialized, initialize with return value of start_messages')


if __name__ == "__main__":
    # Check if network is available
    network_available = check_network()
    # Start App if network is available
    if network_available:
        app = App()
        app.mainloop()
        # stop messages after app is closed
        app.stop_feed()