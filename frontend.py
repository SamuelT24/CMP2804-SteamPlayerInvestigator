import customtkinter as ctk
from Main import get_all_user_info_futures

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class UserRow(ctk.CTkFrame):
    def __init__(self, master, user, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.user = user
        self.expanded = False

        # Set row color
        bg_color = "#f7b0b0" if user["classification"] == "Likely Smurf" else "#b6f7b0"
        self.configure(fg_color=bg_color)

        # Header Frame
        self.header = ctk.CTkFrame(self, fg_color=bg_color)
        self.header.pack(fill="x", padx=5, pady=2)

        # Basic Info
        self.label = ctk.CTkLabel(self.header, text=f'{user["steam_id"]}   {user["personaname"]}  |  {user["classification"]}')
        self.label.pack(side="left", padx=10)


        # Toggle Button
        self.toggle_btn = ctk.CTkButton(self.header, text="+", width=30, command=self.toggle_details)
        self.toggle_btn.pack(side="right")

        # Detail Info (hidden by default)
        self.details_frame = ctk.CTkFrame(self, fg_color=bg_color)
        self.details_label = ctk.CTkLabel(self.details_frame, text=self.get_detail_text(), justify="left")
        self.details_label.pack(padx=10, pady=5)

    def toggle_details(self):
        self.expanded = not self.expanded
        if self.expanded:
            self.details_frame.pack(fill="x", padx=5, pady=(0, 5))
            self.toggle_btn.configure(text="-")
        else:
            self.details_frame.pack_forget()
            self.toggle_btn.configure(text="+")

    def get_detail_text(self):
        return (
            f"Account Created: {self.user['creation_date']}\n"
            f"Account Age (days): {self.user['account_age']}\n"
            f"Friend Count: {self.user['friend_count']}\n"
            f"Number of Games Owned: {self.user['games_owned']}\n"
            f"Total Playtime (minutes): {self.user['playtime']}\n"
            f"VAC Banned: {self.user['vac_banned']}\n"
            f"Smurf Score: {self.user['smurf_score']}\n"
            f"Classification: {self.user['classification']}"
        )

class SmurfDetectorApp(ctk.CTk):
    def __init__(self, users):
        super().__init__()
        self.title("Smurf Detector")
        self.geometry("800x600")

        title_label = ctk.CTkLabel(self, text="Smurf Detector", font=("Arial", 24))
        title_label.pack(pady=20)

        self.user_frame = ctk.CTkScrollableFrame(self, width=760, height=500)
        self.user_frame.pack(fill="both", expand=True, padx=200, pady=10)

        self.users = users


        for user in self.users:
            row = UserRow(self.user_frame, user)
            row.pack(fill="x", pady=5, padx=5)

if __name__ == "__main__":
    app = SmurfDetectorApp(get_all_user_info_futures())
    app.mainloop()
