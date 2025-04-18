import tkinter as tk
import threading
import time
from datetime import datetime, timedelta
import cv2
from PIL import Image, ImageTk


class PomodoroApp:
    def __init__(self, root, show_main_menu):
        self.root = root
        self.show_main_menu = show_main_menu

        for widget in root.winfo_children():
            widget.destroy()

        self.frame = tk.Frame(root, bg="#FFF7F0")
        self.frame.pack(fill="both", expand=True)

        self.back_button = tk.Button(
            self.frame,
            text="⬅ Back",
            font=("Helvetica", 12, "bold"),
            bg="#FFE1E1",
            fg="#333",
            bd=0,
            relief="flat",
            padx=15,
            pady=5,
            command=self.go_back
        )
        self.back_button.place(x=10, y=10)

        self.timer_running = False
        self.time_left = 25 * 60
        self.timer_id = None

        self.timer_label = tk.Label(
            self.frame,
            text="25:00",
            font=("Courier New", 60, "bold"),
            bg="#FFF7F0",
            fg="#FF6B6B"
        )
        self.face_label = tk.Label(
            self.frame,
            text="(｡◕‿◕｡)",
            font=("Courier New", 48),
            bg="#FFF7F0",
            fg="#444444"
        )

        self.button_frame = tk.Frame(self.frame, bg="#FFF7F0")
        self.play_button = self.create_button("▶ Start", self.start_timer)
        self.pause_button = self.create_button("⏸ Pause", self.pause_timer)
        self.reset_button = self.create_button("🔄 Reset", self.reset_timer)

        self.timer_label.pack(pady=40)
        self.button_frame.pack(pady=10)
        self.play_button.grid(row=0, column=0, padx=10)
        self.pause_button.grid(row=0, column=1, padx=10)
        self.reset_button.grid(row=0, column=2, padx=10)
        self.face_label.pack(pady=30)

    def create_button(self, text, command):
        return tk.Button(
            self.button_frame,
            text=text,
            font=("Helvetica", 13, "bold"),
            bg="#FFD6D6",
            fg="#333",
            activebackground="#FFBFBF",
            width=10,
            height=2,
            relief="flat",
            bd=0,
            command=command
        )

    def update_timer(self):
        mins, secs = divmod(self.time_left, 60)
        self.timer_label.config(text=f"{mins:02}:{secs:02}")
        if self.timer_running and self.time_left > 0:
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        elif self.time_left == 0:
            self.timer_label.config(text="Time's up! ✨")
            self.face_label.config(text="(✿◕‿◕)")

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()
            self.face_label.config(text="(｡♥‿♥｡)")

    def pause_timer(self):
        if self.timer_running:
            self.timer_running = False
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
            self.face_label.config(text="(｡•́︿•̀｡)")

    def reset_timer(self):
        self.timer_running = False
        self.time_left = 25 * 60
        self.update_timer()
        self.face_label.config(text="(｡◕‿◕｡)")

    def go_back(self):
        self.frame.destroy()
        self.show_main_menu()


class AlarmApp:
    def __init__(self, root, show_main_menu):
        self.root = root
        self.show_main_menu = show_main_menu

        for widget in root.winfo_children():
            widget.destroy()

        self.frame = tk.Frame(root, bg="#FFF7F0")
        self.frame.pack(fill="both", expand=True)

        self.back_button = tk.Button(
            self.frame,
            text="⬅ Back",
            font=("Helvetica", 12, "bold"),
            bg="#FFE1E1",
            fg="#333",
            bd=0,
            relief="flat",
            padx=15,
            pady=5,
            command=self.go_back
        )
        self.back_button.place(x=10, y=10)

        self.alarm_hour = tk.StringVar(value="0")
        self.alarm_minute = tk.StringVar(value="30")

        selector_frame = tk.Frame(self.frame, bg="#FFF7F0")
        selector_frame.pack(pady=40)

        self.create_dropdown(selector_frame, self.alarm_hour, range(0, 24))
        self.create_dropdown(selector_frame, self.alarm_minute, range(0, 60))

        self.start_button = tk.Button(
            self.frame,
            text="Start Alarm",
            font=("Helvetica", 13, "bold"),
            bg="#FFD6D6",
            fg="#333",
            activebackground="#FFBFBF",
            width=15,
            height=2,
            relief="flat",
            bd=0,
            command=self.start_alarm
        )
        self.start_button.pack(pady=20)

        self.alarm_label = tk.Label(
            self.frame,
            text="00:30:00",
            font=("Courier New", 50, "bold"),
            bg="#FFF7F0",
            fg="#FF6B6B"
        )
        self.face_label = tk.Label(
            self.frame,
            text="(｡◕‿◕｡)",
            font=("Courier New", 42),
            bg="#FFF7F0",
            fg="#444444"
        )

        self.alarm_label.pack(pady=35)
        self.face_label.pack(pady=30)

        self.alarm_started = False

    def create_dropdown(self, parent, variable, options):
        opt = [str(i).zfill(2) for i in options]
        dropdown = tk.OptionMenu(parent, variable, *opt)
        dropdown.config(font=("Helvetica", 12), bg="#FFD6D6", fg="#333", width=5, relief="flat")
        dropdown.pack(side="left", padx=10)

    def start_alarm(self):
        if not self.alarm_started:
            hour = int(self.alarm_hour.get())
            minute = int(self.alarm_minute.get())
            self.time_left = timedelta(hours=hour, minutes=minute)
            self.alarm_started = True
            self.update_alarm()

    def update_alarm(self):
        if self.time_left > timedelta(0):
            hours, remainder = divmod(self.time_left.seconds, 3600)
            mins, secs = divmod(remainder, 60)
            self.alarm_label.config(text=f"{hours:02}:{mins:02}:{secs:02}")
            self.time_left -= timedelta(seconds=1)
            self.root.after(1000, self.update_alarm)
        else:
            self.alarm_label.config(text="Time's up! ✨")
            self.face_label.config(text="(✿◕‿◕)")

    def go_back(self):
        self.frame.destroy()
        self.show_main_menu()


class MainMenu:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root, bg="#FFF7F0")
        self.frame.pack(fill="both", expand=True)

        self.title = tk.Label(
            self.frame,
            text="(｡◕‿◕｡)",
            font=("Courier New", 56),
            bg="#FFF7F0",
            fg="#444"
        )
        self.title.pack(pady=(40, 20))
        self.title.bind("<Button-1>", self.show_menu)

        self.menu_frame = tk.Frame(self.frame, bg="#FFF7F0")

        self.pomodoro_btn = self.create_button("🍅 Pomodoro", self.launch_pomodoro)
        self.alarm_btn = self.create_button("⏰ Alarm", self.launch_alarm)
        self.todo_btn = self.create_button("📝 To-Do List", self.launch_todo)

    def show_menu(self, event=None):
        self.menu_frame.pack()
        self.pomodoro_btn.pack(pady=8)
        self.alarm_btn.pack(pady=8)
        self.todo_btn.pack(pady=8)

    def create_button(self, text, command):
        return tk.Button(
            self.menu_frame,
            text=text,
            font=("Helvetica", 14, "bold"),
            bg="#FFD6D6",
            fg="#333",
            activebackground="#FFBFBF",
            width=22,
            height=2,
            relief="flat",
            bd=0,
            command=command
        )

    def launch_pomodoro(self):
        self.frame.destroy()
        PomodoroApp(self.root, self.launch_main_menu)

    def launch_alarm(self):
        self.frame.destroy()
        AlarmApp(self.root, self.launch_main_menu)

    def launch_todo(self):
        print("To-Do clicked")

    def launch_main_menu(self):
        # We can call `root.after()` to ensure that the menu is refreshed after the frame is destroyed
        self.frame.destroy()
        self.root.after(0, self.show_main_menu)


def main():
    root = tk.Tk()
    root.title("Bot UI")
    root.geometry("800x480")  # Set window size to fit the 7.5-inch screen
    root.resizable(False, False)

    # Function to launch the main menu
    def launch_main_menu():
        menu = MainMenu(root)
        menu.show_menu()  # Show the buttons after the animation

    # Start with the animation screen
    AnimationScreen(root, "black.mp4", launch_main_menu)

    root.mainloop()


if __name__ == "__main__":
    main()
