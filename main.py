from pynput import mouse
import time
import tkinter as tk
import threading

class Timer:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration
        self.start_time = None
        self.running = False

    def start(self):
        self.start_time = time.time()
        self.running = True

    def stop(self):
        self.running = False

    def get_time_left(self):
        if not self.running:
            return 0
        elapsed_time = time.time() - self.start_time
        return self.duration - elapsed_time

    def __str__(self):
        time_left = self.get_time_left()
        if time_left <= 0:
            return f"{self.name}: Время вышло!"
        else:
            minutes, seconds = divmod(time_left, 60)
            return f"{self.name}: {int(minutes):02d}:{int(seconds):02d}"

class TimerManager:
    def __init__(self):
        self.timers = {}
        self.listener = mouse.Listener(on_click=self.on_click)
        self.listener.start()
        self.root = tk.Tk()
        self.root.title("Таймеры")
        self.label = tk.Label(self.root, text="", font=("Arial", 24), fg="red", bg="#fcfcfc", padx=10, pady=10)
        self.label.pack()

    def add_timer(self, name, duration):
        self.timers[name] = Timer(name, duration)

    def start_timer(self, name):
        if name in self.timers:
            self.timers[name].start()

    def stop_timer(self, name):
        if name in self.timers:
            self.timers[name].stop()

    def on_click(self, x, y, button, pressed):
        if pressed:
            if button == mouse.Button.left:
                self.start_timer("mouse4")
            elif button == mouse.Button.right:
                self.start_timer("mouse5")

    def print_timers(self):
        while True:
            text = ""
            for timer in self.timers.values():
                text += str(timer) + "\n"
            self.label.config(text=text)
            self.root.update()
            time.sleep(1)

def main():
    manager = TimerManager()
    manager.add_timer("mouse4", 60)  # 1 минута
    manager.add_timer("mouse5", 60)  # 30 секунд

    threading.Thread(target=manager.print_timers).start()
    manager.root.mainloop()

if __name__ == "__main__":
    main()