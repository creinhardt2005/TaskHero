from tkinter import *
from logic import TaskManager, UserProfile

class TaskHero:
    """Contains all functions for the app"""

    def __init__(self, root: Tk):
        """Initializes TaskHero with basic window"""
        self.window = root
        self.window.title("TaskHero")
        self.task_manager = TaskManager()
        self.user_profile = UserProfile()
        self.current_frame = None
        self.message_label = None
        self.start_page()

    def clear_frame(self):
        """Clears current frame and message label"""
        if self.current_frame is not None:
            self.current_frame.pack_forget()
            self.current_frame = None
            if self.message_label:
                self.message_label.pack_forget()

    def start_page(self):
        """Displays the start page with options and welcome text"""
        self.clear_frame()
        start_frame = Frame(self.window)
        start_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_frame = start_frame

        Label(start_frame, text="Welcome to TaskHero", font=("Arial", 16)).pack(pady=20)
        Button(start_frame, text="Submit Activity", command=self.view_activities).pack(pady=5)
        Button(start_frame, text="Manage Rewards", command=self.manage_rewards).pack(pady=5)
        Button(start_frame, text="View Current Level", command=self.view_profile).pack(pady=5)
        Button(start_frame, text="Exit", command=self.exit_app).pack(pady=20)

    def view_activities(self):
        """Displays activity submission page"""
        self.clear_frame()
        activities_frame = Frame(self.window)
        activities_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.current_frame = activities_frame
        Label(activities_frame, text="Daily Goals", font=("Arial", 14)).pack(pady=10)
        categories = ["School", "Work", "Personal"]
        selected_goals = {}

        for category in categories:
            Label(activities_frame, text=f"{category} Goals", font=("Arial", 12)).pack(anchor="w", pady=5)
            goals = self.task_manager.get_goals(category)
            for goal in goals:
                var = IntVar()
                Checkbutton(activities_frame, text=f"{goal['name']} ({goal['points']} pts)", variable=var).pack(
                    anchor="w", padx=20
                )
                selected_goals[goal['name']] = (var, goal['points'])

        def submit_points():
            """Submits selected goals and adds points"""
            selected = [points for goal, (var, points) in selected_goals.items() if var.get() == 1]
            if not selected:
                self.show_message("Please select an option")
                return
            total_points = sum(selected)
            self.user_profile.add_points(total_points)
            self.user_profile.save_info()
            self.show_message(f"Points added: {total_points}")

        Button(activities_frame, text="Submit", command=submit_points).pack(pady=10)
        Button(activities_frame, text="Modify Goals", command=self.modify_goals).pack(pady=20)
        Button(activities_frame, text="Back", command=self.start_page).pack()

    def manage_rewards(self):
        """Displays the rewards page"""
        self.clear_frame()
        rewards_frame = Frame(self.window)
        rewards_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.current_frame = rewards_frame

        points_label = Label(rewards_frame, text=f"Points available: {self.user_profile.points}", font=("Arial", 14))
        points_label.pack(pady=10)
        selected_rewards = {}

        for reward in self.task_manager.rewards:
            var = IntVar()
            Checkbutton(rewards_frame, text=f"{reward['name']} ({reward['points']} pts)", variable=var).pack(anchor="w")
            selected_rewards[reward['name']] = (var, reward['points'])

        def redeem_rewards():
            """Redeems selected rewards and deducts them"""
            selected = [points for reward, (var, points) in selected_rewards.items() if var.get() == 1]
            if not selected:
                self.show_message("Please select an option")
                return
            try:
                total_cost = sum(selected)
                self.user_profile.minus_points(total_cost)
                points_label.config(text=f"Points available: {self.user_profile.points}")
                self.user_profile.save_info()
                self.show_message(f"Rewards redeemed. Points deducted: {total_cost}")
            except ValueError as e:
                self.show_message(str(e))

        Button(rewards_frame, text="Redeem", command=redeem_rewards).pack(pady=20)
        Button(rewards_frame, text="Modify Rewards", command=self.modify_rewards).pack(pady=10)
        Button(rewards_frame, text="Back", command=self.start_page).pack()

    def modify_rewards(self):
        """Allows the user to modify existing rewards"""

        self.clear_frame()
        modify_frame = Frame(self.window)
        modify_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.current_frame = modify_frame
        Label(modify_frame, text="Modify Rewards", font=("Arial", 14)).pack(pady=10)
        modify_rewards_entries = {}

        for reward in self.task_manager.rewards:
            Label(modify_frame, text=f"Reward: {reward['name']}", font=("Arial", 12)).pack(anchor="w", pady=5)
            name_entry = Entry(modify_frame)
            name_entry.insert(0, reward["name"])
            name_entry.pack(anchor="w", padx=20)
            points_entry = Entry(modify_frame)
            points_entry.insert(0, str(reward["points"]))
            points_entry.pack(anchor="w", padx=20)
            modify_rewards_entries[reward["name"]] = (name_entry, points_entry)

        def save_rewards():
            """Saves the modified reward names and point values"""
            for reward_name, (name_entry, points_entry) in modify_rewards_entries.items():
                new_name = name_entry.get()
                new_points = int(points_entry.get())
                for reward in self.task_manager.rewards:
                    if reward["name"] == reward_name:
                        reward["name"] = new_name
                        reward["points"] = new_points
            self.task_manager.save_info()
            self.show_message("Rewards updated successfully!")

        Button(modify_frame, text="Save Changes", command=save_rewards).pack(pady=20)
        Button(modify_frame, text="Back", command=self.start_page).pack()

    def view_profile(self):
        """Displays user profile, including current level and points"""
        self.clear_frame()
        profile_frame = Frame(self.window)
        profile_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.current_frame = profile_frame

        level = self.user_profile.level
        points_progress = self.user_profile.points_for_level % 5000
        Label(profile_frame, text=f"User Level: {level}", font=("Arial", 14)).pack(pady=10)
        Label(profile_frame, text=f"Points: {points_progress}/5000", font=("Arial", 12)).pack()
        Button(profile_frame, text="Back", command=self.start_page).pack()

    def modify_goals(self):
        """Lets the user modify goals"""
        self.clear_frame()
        modify_frame = Frame(self.window)
        modify_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.current_frame = modify_frame
        Label(modify_frame, text="Modify Goals", font=("Arial", 14)).pack(pady=10)
        categories = ["School", "Work", "Personal"]
        modify_goals_entries = {}

        for category in categories:
            Label(modify_frame, text=f"{category} Goals", font=("Arial", 12)).pack(anchor="w", pady=5)
            goals = self.task_manager.get_goals(category)
            for goal in goals:
                name_entry = Entry(modify_frame)
                name_entry.insert(0, goal["name"])
                name_entry.pack(anchor="w", padx=20)
                points_entry = Entry(modify_frame)
                points_entry.insert(0, str(goal["points"]))
                points_entry.pack(anchor="w", padx=20)
                modify_goals_entries[goal["name"]] = (name_entry, points_entry)

        def save_modified_goals():
            """Saves modified goal names"""
            for goal_name, (name_entry, points_entry) in modify_goals_entries.items():
                new_name = name_entry.get()
                new_points = int(points_entry.get())
                for category in categories:
                    goals = self.task_manager.get_goals(category)
                    for goal in goals:
                        if goal["name"] == goal_name:
                            goal["name"] = new_name
                            goal["points"] = new_points
            self.task_manager.save_info()
            self.show_message("Goals updated successfully!")
        Button(modify_frame, text="Save Changes", command=save_modified_goals).pack(pady=20)
        Button(modify_frame, text="Back", command=self.start_page).pack()

    def show_message(self, message: str):
        """Displays message on the screen"""
        if self.message_label:
            self.message_label.pack_forget()
        self.message_label = Label(self.window, text=message, font=("Arial", 12), fg="black")
        self.message_label.pack(pady=10)
        self.message_label.after(3000, lambda: self.message_label.config(text=""))

    def clear_message(self):
        """Clears the message displayed"""
        if self.message_label:
            self.message_label.pack_forget()
            self.message_label = None

    def exit_app(self):
        """Exits the app"""
        self.window.quit()
