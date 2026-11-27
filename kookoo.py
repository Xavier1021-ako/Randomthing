import ctypes
import random
import tkinter as tk
from tkinter import ttk

TITLE = "kookoo.exe"
BLUE = "#0808f5"

def visible_other_windows():
    """Return titles of visible, non-minimized app windows other than this process."""
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32
    own_pid = kernel32.GetCurrentProcessId()
    ignored = {"Progman", "WorkerW", "Shell_TrayWnd", "Shell_SecondaryTrayWnd"}
    titles = []
    callback_type = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)

    def visit(hwnd, _):
        if not user32.IsWindowVisible(hwnd) or user32.IsIconic(hwnd):
            return True
        cls = ctypes.create_unicode_buffer(256)
        user32.GetClassNameW(hwnd, cls, 256)
        if cls.value in ignored:
            return True
        pid = ctypes.c_ulong()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        if pid.value == own_pid:
            return True
        n = user32.GetWindowTextLengthW(hwnd)
        if n:
            title = ctypes.create_unicode_buffer(n + 1)
            user32.GetWindowTextW(hwnd, title, n + 1)
            if title.value.strip():
                titles.append(title.value)
        return True

    user32.EnumWindows(callback_type(visit), 0)
    return titles

class KooKoo:
    def __init__(self, root):
        self.root = root
        root.title(TITLE)
        root.geometry("560x650")
        root.minsize(480, 560)
        root.configure(bg="#050516")
        root.attributes("-topmost", True)
        root.protocol("WM_DELETE_WINDOW", root.destroy)

        top = tk.Frame(root, bg="#10105b", height=42)
        top.pack(fill="x")
        tk.Label(top, text="●  kookoo.exe", bg="#10105b", fg="white",
                 font=("Segoe UI", 12, "bold")).pack(side="left", padx=14, pady=9)
        tk.Button(top, text="×", command=root.destroy, bg="#10105b", fg="white",
                  bd=0, font=("Segoe UI", 16), activebackground="#d00035"
                  ).pack(side="right", padx=8)

        self.canvas = tk.Canvas(root, width=500, height=370, bg="#050516",
                                highlightthickness=0)
        self.canvas.pack(padx=12, pady=(12, 0))
        self.draw_kookoo()

        self.status = tk.Label(root, text="MINIMIZE ALL YOUR WINDOWS",
                               bg="#050516", fg="#bfc4ff",
                               font=("Segoe UI", 13, "bold"))
        self.status.pack(pady=(8, 2))
        self.number = tk.Label(root, text="READY", bg="#050516", fg="white",
                               font=("Consolas", 42, "bold"))
        self.number.pack()
        self.info = tk.Label(root, text="A random target from 1 to 15 will be chosen.",
                             bg="#050516", fg="#9298d6", font=("Segoe UI", 10))
        self.info.pack(pady=4)
        self.start_btn = tk.Button(root, text="START", command=self.start,
                                   bg="#1717ed", fg="white", activebackground="#3838ff",
                                   activeforeground="white", bd=0,
                                   font=("Segoe UI", 12, "bold"), padx=32, pady=11)
        self.start_btn.pack(pady=12)
        tk.Label(root, text="Minimize every other app window before the counter reaches your target.",
                 bg="#050516", fg="#737bb8", font=("Segoe UI", 9),
                 wraplength=490).pack(pady=(0, 12))

        self.target = 0
        self.tick_no = 0
        self.after_id = None
        self.active = False

    def draw_kookoo(self):
        c = self.canvas
        # Blue static halo and vertical glitch streaks; no white image background.
        random.seed(17)
        for _ in range(2100):
            angle = random.random() * 6.283
            radius = random.uniform(145, 185)
            x, y = 250 + radius * __import__("math").cos(angle), 180 + radius * __import__("math").sin(angle)
            c.create_rectangle(x, y, x + 2, y + 2, fill="#2525ff", outline="")
        for _ in range(95):
            x = random.randint(75, 425)
            y1 = random.randint(5, 125)
            y2 = random.randint(245, 365)
            c.create_line(x, y1, x + random.randint(-4, 4), 180, fill="#2020ff", width=random.choice([1, 2]))
            c.create_line(x, 180, x + random.randint(-4, 4), y2, fill="#2020ff", width=1)
        c.create_oval(105, 35, 395, 325, fill=BLUE, outline="#eeeeff", width=2)
        # X eyes and curved smile, rendered as crisp white strokes.
        c.create_line(175, 105, 235, 205, fill="white", width=4)
        c.create_line(225, 105, 175, 205, fill="white", width=4)
        c.create_line(275, 105, 335, 205, fill="white", width=4)
        c.create_line(325, 105, 275, 205, fill="white", width=4)
        c.create_arc(135, 130, 365, 290, start=200, extent=140,
                     style="arc", outline="white", width=3)
        # Pixel-like flecks around the face.
        for _ in range(500):
            x = random.randint(55, 445)
            y = random.randint(5, 360)
            if (x - 250) ** 2 + (y - 180) ** 2 > 150 ** 2:
                c.create_rectangle(x, y, x + 1, y + 1, fill="#3030ff", outline="")

    def start(self):
        if self.active:
            return
        self.target = random.randint(1, 15)
        self.tick_no = 0
        self.active = True
        self.start_btn.config(state="disabled", text="SURVIVE")
        self.status.config(text="HIDE YOUR WINDOWS")
        self.number.config(text=f"0 / {self.target}")
        self.info.config(text=f"Your target is {self.target}. Minimize every other window!")
        self.after_id = self.root.after(1000, self.tick)

    def tick(self):
        if not self.active:
            return
        if not visible_other_windows():
            self.finish(True)
            return
        self.tick_no += 1
        self.number.config(text=f"{self.tick_no} / {self.target}")
        if self.tick_no >= self.target:
            if visible_other_windows():
                self.finish(False)
            else:
                self.finish(True)
            return
        self.after_id = self.root.after(1000, self.tick)

    def finish(self, survived):
        self.active = False
        if survived:
            self.status.config(text="YOU SURVIVED")
            self.number.config(text="✓")
            self.info.config(text="All other windows are minimized. KooKoo missed you.")
        else:
            self.status.config(text="KOOKOO GOT YOU")
            self.number.config(text="✕")
            self.info.config(text="The target arrived while another window was still visible.")
        self.start_btn.config(state="normal", text="PLAY AGAIN")
        self.root.bell()

if __name__ == "__main__":
    if __import__("os").name != "nt":
        raise SystemExit("kookoo.exe is a Windows-only game.")
    window = tk.Tk()
    KooKoo(window)
    window.mainloop()
