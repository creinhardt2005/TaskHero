import os
import json

class TaskManager:
    """Manages tasks and rewards for user"""

    def __init__(self, file_path="info.txt"):
        """Initializes the TaskManager with the text file"""
        self.file_path = file_path
        self.rewards = [
            {"name": "Fast food", "points": 300},
            {"name": "New book", "points": 1000},
            {"name": "Short trip", "points": 5000},
        ]
        self.goals = {
            "School": [{"name": "Do homework", "points": 500}],
            "Work": [{"name": "Complete project", "points": 1000}],
            "Personal": [{"name": "Workout", "points": 300}],
        }
        self.load_info()

    def get_goals(self, category):
        """Retrieves goals for the category"""
        return self.goals.get(category, [])

    def save_info(self):
        """Saves the current rewards and goals info"""
        data = {
            "rewards": self.rewards,
            "goals": self.goals,
        }
        with open(self.file_path, "w") as file:
            json.dump(data, file)

    def load_info(self):
        """Loads the rewards and goals data"""
        if not os.path.exists(self.file_path) or os.stat(self.file_path).st_size == 0:
            self.save_info()
            return
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
                self.rewards = data.get("rewards", self.rewards)
                self.goals = data.get("goals", self.goals)
        except json.JSONDecodeError:
            self.save_info()
            return

    def modify_reward(self, reward_name, new_name, new_points):
        """Modifies name and point value of a reward"""
        for reward in self.rewards:
            if reward["name"] == reward_name:
                reward["name"] = new_name
                reward["points"] = new_points
                break
        self.save_info()


class UserProfile:
    """Represents user profile (points and level)"""

    def __init__(self, file_path="info.txt"):
        """Initializes the UserProfile with the provided file path. Loads or initializes the user's data"""
        self.file_path = file_path
        self.points = 0
        self.points_for_level = 0
        self.level = 1
        self.load_info()

    def add_points(self, points):
        """Adds points to the user profile and checks for level up"""
        self.points += points
        self.points_for_level += points
        self.level_up()

    def minus_points(self, points):
        """Deducts points from the user profile, checking count"""
        if points > self.points:
            raise ValueError("Not enough points")
        self.points -= points

    def level_up(self):
        """Sees if the user has enough points to level up"""
        while self.points_for_level >= 5000:
            self.level += 1
            self.points_for_level -= 5000

    def save_info(self):
        """Saves the user's points and level data"""
        data = {
            "points": self.points,
            "points_for_level": self.points_for_level,
            "level": self.level,
        }
        with open(self.file_path, "r+") as file:
            existing_data = {}
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                pass
            existing_data.update({"user_profile": data})
            file.seek(0)
            json.dump(existing_data, file)
            file.truncate()

    def load_info(self):
        """Loads the user's profile info"""
        if not os.path.exists(self.file_path) or os.stat(self.file_path).st_size == 0:
            return
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
                user_data = data.get("user_profile", {})
                self.points = user_data.get("points", 0)
                self.points_for_level = user_data.get("points_for_level", 0)
                self.level = user_data.get("level", 1)
        except json.JSONDecodeError:
            pass
