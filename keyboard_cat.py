import tkinter as tk
from tkinter import messagebox, simpledialog
import keyboard
import time
import os
import json
from threading import Thread, Lock
import sys
import socket
import pystray
from PIL import Image
from constants import CAT_FRAMES, COLORS, RARITY_TEXT_COLORS, RARITY_WEIGHTS
import random

class DesktopPet:
    _lock_socket = None

    @classmethod
    def _acquire_lock(cls):
        cls._lock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for port in range(29269, 29279):  # 尝试多个端口
            try:
                cls._lock_socket.bind(('127.0.0.1', port))
                return True
            except socket.error:
                continue
        return False

    def __init__(self):
        if not self._acquire_lock():
            messagebox.showwarning("猫猫警告", "人, 拥有我就不能再有其他🐱了!")
            raise RuntimeError("Application already running")
        
        # Initialize data
        self._count_lock = Lock()
        self.key_count = 0
        self.total_key_count = 0
        self.owned_colors = ['#333333']  # Initially own deep gray
        self.load_datas()
        self.reminder_interval = 60 * 30
        self.last_reminder_time = time.time()
        self.running = True
        self.current_color = '#333333'  # Initial color is deep gray
        self.animating = False
        self.current_frame = 0
        self.key_since_last_anim = 0
        self.drag_data = {"x": 0, "y": 0, "dragging": False}
        
        # Create main window
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-transparentcolor', 'white')
        
        # Content frame
        self.frame = tk.Frame(self.root, bg='#E6F3FF')
        self.frame.pack()
        
        # Pet label
        self.pet_label = tk.Label(
            self.frame,
            text=CAT_FRAMES[0], 
            font=("Arial", 24),
            bg='#E6F3FF',
            fg=self.current_color
        )
        self.pet_label.pack(side=tk.LEFT)
        
        # Keyboard count display
        self.count_label = tk.Label(
            self.frame,
            text=f"已敲击键盘:{self.key_count}次",
            font=("Arial", 10),
            bg='#E6F3FF',
            fg=RARITY_TEXT_COLORS[COLORS[self.current_color]['rarity']]
        )
        self.count_label.pack(side=tk.LEFT, padx=5)
        
        # Prevent sub-components from intercepting events
        self.pet_label.configure(takefocus=False)
        self.count_label.configure(takefocus=False)
        
        # Bind events
        self.setup_event_bindings()

        # System tray
        self.setup_system_tray()
        
        # Start threads
        self.keyboard_thread = Thread(target=self._keyboard_hook)
        self.keyboard_thread.daemon = True
        self.keyboard_thread.start()
        
        self.reminder_thread = Thread(target=self.reminder_checker)
        self.reminder_thread.daemon = True
        self.reminder_thread.start()
        
        # Initial window position
        self.root.geometry("+100+100")
        self.animate_cat()

    def setup_system_tray(self):
        icon_path = os.path.join(
            getattr(sys, '_MEIPASS', os.path.dirname(__file__)), 
            'cat_icon.ico'
        )
        try:
            image = Image.open(icon_path)
        except Exception as e:
            print(f"加载托盘图标失败: {e}")
            image = Image.new('RGB', (64, 64), color='black')
        
        self.tray_icon = pystray.Icon(
            "DesktopPet",
            image,
            "Desktop Pet",
            menu=self.create_tray_menu()
        )
        
        self.tray_thread = Thread(target=self.tray_icon.run)
        self.tray_thread.daemon = True
        self.tray_thread.start()

    def create_tray_menu(self):
        menu = []
        color_menu = []
        for color in self.owned_colors:
            color_info = COLORS[color]
            color_menu.append(
                pystray.MenuItem(
                    f"{color_info['name']} ({color_info['rarity']})",
                    lambda c=color: self.change_color(c)
                )
            )
        menu.append(pystray.MenuItem("选择颜色", pystray.Menu(*color_menu)))
        menu.append(pystray.MenuItem("设置提醒间隔", self.set_interval))
        menu.append(pystray.MenuItem("关闭", self.close_app))
        return pystray.Menu(*menu)

    def setup_event_bindings(self):
        for widget in (self.frame, self.pet_label, self.count_label):
            widget.bind("<ButtonPress-1>", self.start_move)
            widget.bind("<ButtonRelease-1>", self.stop_move)
            widget.bind("<B1-Motion>", self.on_move)
        self.root.bind("<Button-3>", self.show_menu)

        self.pet_label.bindtags((self.pet_label, self.frame, self.root, "all"))
        self.count_label.bindtags((self.count_label, self.frame, self.root, "all"))

    def animate_cat(self):
        if self.animating and self.key_since_last_anim >= 50:
            self.current_frame = (self.current_frame + 1) % len(CAT_FRAMES)
            self.pet_label.config(text=CAT_FRAMES[self.current_frame])
            self.key_since_last_anim = 0
        elif self.pet_label['text'] != CAT_FRAMES[0]:
            self.pet_label.config(text=CAT_FRAMES[0])
        self.root.after(200, self.animate_cat)

    def get_data_path(self):
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(__file__)
        return os.path.join(base_path, 'data', 'pet_data.json')

    def load_datas(self):
        try:
            data_path = self.get_data_path()
            if os.path.exists(data_path):
                with open(data_path, 'r') as f:
                    data = json.load(f)
                    self.key_count = data.get('key_count', 0)
                    self.total_key_count = data.get('total_key_count', 0)
                    self.owned_colors = data.get('owned_colors', ['#333333'])
        except Exception as e:
            print(f"加载数据失败: {e}")

    def save_total_count(self):
        try:
            data_path = self.get_data_path()
            os.makedirs(os.path.dirname(data_path), exist_ok=True)
            with open(data_path, 'w') as f:
                json.dump({
                    'key_count': self.key_count,
                    'total_key_count': self.total_key_count,
                    'owned_colors': self.owned_colors
                }, f)
        except Exception as e:
            print(f"保存数据失败: {e}")

    def start_move(self, event):
        self.drag_data["x"] = event.x_root - self.root.winfo_x()
        self.drag_data["y"] = event.y_root - self.root.winfo_y()
        self.drag_data["dragging"] = True

    def stop_move(self, event):
        self.drag_data["dragging"] = False

    def on_move(self, event):
        if self.drag_data["dragging"]:
            x = event.x_root - self.drag_data["x"]
            y = event.y_root - self.drag_data["y"]
            self.root.geometry(f"+{x}+{y}")

    def show_menu(self, event):
        menu = tk.Menu(self.root, tearoff=0)
        # Add color selection submenu
        color_menu = tk.Menu(menu, tearoff=0)
        for color in self.owned_colors:
            color_info = COLORS[color]
            color_menu.add_command(
                label=f"{color_info['name']} ({color_info['rarity']})",
                command=lambda c=color: self.change_color(c),
                foreground=RARITY_TEXT_COLORS[color_info['rarity']]
            )
        menu.add_cascade(label="选择颜色", menu=color_menu)
        menu.add_command(label="设置提醒间隔", command=self.set_interval)
        menu.add_command(label="关闭", command=self.close_app)
        menu.tk_popup(event.x_root, event.y_root)

    def change_color(self, color):
        self.current_color = color
        self.pet_label.config(fg=self.current_color)
        self.count_label.config(fg=RARITY_TEXT_COLORS[COLORS[color]['rarity']])

    def set_interval(self):
        interval = simpledialog.askinteger(
            "桌面宠物", 
            "输入提醒间隔(分钟):", 
            parent=self.root,
            minvalue=1,
            initialvalue=self.reminder_interval//60
        )
        if interval:
            self.reminder_interval = interval * 60

    def close_app(self):
        self.save_total_count()
        self.running = False
        if self._lock_socket:
            self._lock_socket.close()
        self.tray_icon.stop()
        self.root.destroy()

    def _keyboard_hook(self):
        try:
            keyboard.hook(self.count_keys)
        except Exception as e:
            print(f"键盘监听失败: {e}")

    def count_keys(self, event):
        if event.event_type == keyboard.KEY_UP:
            with self._count_lock:
                self.key_count += 1
                self.total_key_count += 1
                self.key_since_last_anim += 1
            self.animating = True
            self.root.after(1000, lambda: setattr(self, 'animating', False))
            self.count_label.config(
                text=f"已敲击键盘:{self.key_count}次",
                fg=RARITY_TEXT_COLORS[COLORS[self.current_color]['rarity']]
            )
            if self.total_key_count % 10000 == 0:
                # Select rarity based on weights
                rarity = random.choices(
                    list(RARITY_WEIGHTS.keys()),
                    weights=list(RARITY_WEIGHTS.values()),
                    k=1
                )[0]
                # Get all colors of the selected rarity
                rarity_colors = [color for color, info in COLORS.items() if info['rarity'] == rarity]
                # Randomly select a color from the rarity
                new_color = random.choice(rarity_colors)
                # Add to owned_colors if not already owned
                if new_color not in self.owned_colors:
                    self.owned_colors.append(new_color)
                    self.save_total_count()
                    messagebox.showinfo(
                        "新颜色解锁",
                        f"恭喜！你获得了新颜色：{COLORS[new_color]['name']} ({COLORS[new_color]['rarity']})",
                        parent=self.root
                    )
                self.current_color = new_color
                self.pet_label.config(fg=self.current_color)
                self.count_label.config(fg=RARITY_TEXT_COLORS[COLORS[self.current_color]['rarity']])

    def reminder_checker(self):
        while self.running:
            current_time = time.time()
            if current_time - self.last_reminder_time > self.reminder_interval:
                self.show_reminder()
                self.last_reminder_time = current_time
                with self._count_lock:
                    self.key_count = 0
            time.sleep(1)

    def show_reminder(self):
        messagebox.showinfo(
            "桌面宠物", 
            f"本次已敲击:{self.key_count}次\n总计敲击:{self.total_key_count}次\n该休息一下了!",
            parent=self.root
        )

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    try:
        pet = DesktopPet()
        pet.run()
    except RuntimeError:
        sys.exit(1)