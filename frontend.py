import customtkinter as ctk
from config import Classifications

#sets up window appearance
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class UserRow(ctk.CTkFrame):
    def __init__(self, master, user, *args, **kwargs):
        """creates a row for each steam account and stores the widgets inside a frame
        and also allows for extra customisation such as bg colour"""
        super().__init__(master, *args, **kwargs)
        self.user = user
        self.expanded = False

        #sets the row colour to red if steam profile is likely a smurf
        bg_color = "#f7b0b0" if user["classification"] == Classifications.LIKELY_SMURF else "#b6f7b0"

        if user["classification"] != Classifications.LIKELY_SMURF and user["vac_banned"]:
            bg_color = "#f7efb0"
        self.configure(fg_color=bg_color)

        #header frame
        self.header = ctk.CTkFrame(self, fg_color=bg_color)
        self.header.pack(fill="x", padx=5, pady=2)

        #displays the basic information of each steam account
        self.label = ctk.CTkLabel(self.header, text=f"{user["steam_id"]}   {user["personaname"]}  |  {user["classification"]} {("(Vac Banned)" if user["vac_banned"] else "")}", text_color="#000000")
        self.label.pack(side="left", padx=10)


        #toggle button is used to expand each dropdown menu
        self.toggle_button = ctk.CTkButton(self.header, text="+", width=30, command=self.toggle_details)
        self.toggle_button.pack(side="right")

        #extra information hidden by default
        self.details_frame = ctk.CTkFrame(self, fg_color=bg_color)
        self.details_label = ctk.CTkLabel(self.details_frame, text=self.get_detail_text(), justify="left", text_color="#000000")
        self.details_label.pack(padx=10, pady=5)

    def toggle_details(self):
        """toggles between the two states of having more or less info
        displayed for each user"""
        self.expanded = not self.expanded
        if self.expanded:
            self.details_frame.pack(fill="x", padx=5, pady=(0, 5))
            self.toggle_button.configure(text="-")
        else:
            self.details_frame.pack_forget()
            self.toggle_button.configure(text="+")

    def get_detail_text(self):
        """returns a formatted string displaying steam account info"""
        return (
            f"Account Created: {self.user["creation_date"]}\n"
            f"Account Age (days): {self.user["account_age"]}\n"
            f"Friend Count: {self.user["friend_count"]}\n"
            f"Number of Games Owned: {self.user["games_owned"]}\n"
            f"Total Playtime (minutes): {self.user["playtime"]}\n"
            f"VAC Banned: {self.user["vac_banned"]}\n"
            f"Smurf Score: {self.user["smurf_score"]}\n"
            f"Classification: {self.user["classification"]}"
        )

class SmurfDetectorApp(ctk.CTk):
    def __init__(self, users):
        """initializes the parent class and sets up the UI screen"""
        super().__init__()
        self.title("Smurf Detector")
        self.geometry("800x600")

        title_label = ctk.CTkLabel(self, text="Users:", font=("Arial", 24))
        title_label.pack(pady=20)

        self.user_frame = ctk.CTkScrollableFrame(self, width=760, height=500)
        self.user_frame.pack(fill="both", expand=True, padx=200, pady=10)

        self.users = users

        """goes through each of the users information and creates various
        buttons and labels for each user in the window"""
        for user in self.users:
            row = UserRow(self.user_frame, user)
            row.pack(fill="x", pady=5, padx=5)