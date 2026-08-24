"""
iPhone tarzi Hesap Makinesi - Python / tkinter
Calistirmak icin: python calculator.py
"""

import tkinter as tk
import sys
import ctypes


def enable_dpi_awareness():
    """Windows'ta DPI farkindaligini acar; bulanik/pikselli gorunumu duzeltir."""
    if sys.platform != "win32":
        return
    try:
        # Windows 8.1+ : per-monitor DPI awareness (en net sonuc)
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            # Eski Windows surumleri icin yedek
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


enable_dpi_awareness()

# ---------- Renkler (iOS temasi) ----------
BG = "#000000"
DISPLAY_FG = "#ffffff"
HISTORY_FG = "#767676"
FN_BG = "#a5a5a5"
FN_BG_ACTIVE = "#d4d4d2"
FN_FG = "#000000"
NUM_BG = "#333333"
NUM_BG_ACTIVE = "#5a5a5a"
NUM_FG = "#ffffff"
OP_BG = "#ff9f0a"
OP_BG_ACTIVE = "#ffc46b"
OP_FG = "#ffffff"
OP_ACTIVE_BG = "#ffd8a6"
OP_ACTIVE_FG = "#ff9f0a"


def set_dark_titlebar(root):
    """Windows'ta baslik cubugunu siyaha yaklastirir (Windows 10 1809+ / 11)."""
    if sys.platform != "win32":
        return
    try:
        root.update_idletasks()
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        value = ctypes.c_int(1)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE,
            ctypes.byref(value), ctypes.sizeof(value)
        )
        # Windows 11 22H2+ : baslik cubugunu tam siyaha boyar
        DWMWA_CAPTION_COLOR = 35
        black = ctypes.c_int(0x00000000)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, DWMWA_CAPTION_COLOR,
            ctypes.byref(black), ctypes.sizeof(black)
        )
        DWMWA_TEXT_COLOR = 36
        white = ctypes.c_int(0x00FFFFFF)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, DWMWA_TEXT_COLOR,
            ctypes.byref(white), ctypes.sizeof(white)
        )
    except Exception:
        pass


class RoundButton(tk.Canvas):
    """Oval / hap seklinde tiklanabilir tus (tkinter Canvas tabanli)."""

    def __init__(self, parent, text, bg, fg, active_bg,
                 command=None, font=("Helvetica", 22), shape="oval"):
        super().__init__(parent, bg=parent["bg"], highlightthickness=0, bd=0)
        self.command = command
        self.bg_color = bg
        self.active_bg = active_bg
        self.fg_color = fg
        self.font = font
        self.text = text
        self.shape = shape  # "oval" (daire) veya "pill" (uzun hap)
        self.item_shape = None
        self.item_text = None

        self.bind("<Configure>", self._draw)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<Enter>", self._on_hover)
        self.bind("<Leave>", self._on_leave)

    def _draw(self, event=None):
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        if w <= 1 or h <= 1:
            return
        pad = 3
        if self.shape == "pill":
            self.item_shape = self._rounded_rect(
                pad, pad, w - pad, h - pad, radius=(h - 2 * pad) / 2,
                fill=self.bg_color
            )
        else:
            side = min(w, h) - 2 * pad
            x0 = (w - side) / 2
            y0 = (h - side) / 2
            self.item_shape = self.create_oval(
                x0, y0, x0 + side, y0 + side, fill=self.bg_color, outline=""
            )
        self.item_text = self.create_text(
            w / 2, h / 2, text=self.text, fill=self.fg_color, font=self.font
        )

    def _rounded_rect(self, x1, y1, x2, y2, radius, fill):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1,
        ]
        return self.create_polygon(points, fill=fill, smooth=True, outline="")

    def _on_press(self, event):
        if self.item_shape:
            self.itemconfig(self.item_shape, fill=self.active_bg)

    def _on_release(self, event):
        if self.item_shape:
            self.itemconfig(self.item_shape, fill=self.bg_color)
        if self.command:
            self.command()

    def _on_hover(self, event):
        self.configure(cursor="hand2")

    def _on_leave(self, event):
        pass

    def set_colors(self, bg=None, fg=None):
        if bg is not None:
            self.bg_color = bg
            if self.item_shape:
                self.itemconfig(self.item_shape, fill=bg)
        if fg is not None:
            self.fg_color = fg
            if self.item_text:
                self.itemconfig(self.item_text, fill=fg)

    def set_text(self, text):
        self.text = text
        if self.item_text:
            self.itemconfig(self.item_text, text=text)


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("")  # baslik yazisini kaldir
        self.configure(bg=BG)

        # Ekran DPI'sina gore tkinter olcegini ayarla (netlik icin)
        try:
            dpi = self.winfo_fpixels('1i')
            self.tk.call('tk', 'scaling', dpi / 72.0)
        except Exception:
            pass

        self.geometry("320x560")
        self.minsize(300, 520)

        # Durum
        self.current = "0"
        self.previous = None
        self.operator = None
        self.overwrite = True
        self.last_operator = None
        self.last_operand = None

        self.op_buttons = {}  # action -> RoundButton
        self.clear_btn = None

        self._build_display()
        self._build_pad()
        self._bind_keys()
        self._update_display()

        # Baslik cubugunu siyaha cek (Windows)
        self.after(10, lambda: set_dark_titlebar(self))

    # ---------------- UI ----------------
    def _build_display(self):
        frame = tk.Frame(self, bg=BG)
        frame.pack(fill="x", padx=14, pady=(20, 6))

        self.history_var = tk.StringVar(value=" ")
        self.history_label = tk.Label(
            frame, textvariable=self.history_var, bg=BG, fg=HISTORY_FG,
            font=("Helvetica", 14), anchor="e", justify="right"
        )
        self.history_label.pack(fill="x")

        self.display_var = tk.StringVar(value="0")
        self.display_label = tk.Label(
            frame, textvariable=self.display_var, bg=BG, fg=DISPLAY_FG,
            font=("Helvetica", 48), anchor="e", justify="right"
        )
        self.display_label.pack(fill="x")

        # basili tutunca kopyala
        self.display_label.bind("<ButtonPress-1>", self._start_hold)
        self.display_label.bind("<ButtonRelease-1>", self._cancel_hold)
        self._hold_id = None

    def _build_pad(self):
        pad = tk.Frame(self, bg=BG)
        pad.pack(fill="both", expand=True, padx=10, pady=10)

        for i in range(4):
            pad.columnconfigure(i, weight=1)
        for i in range(5):
            pad.rowconfigure(i, weight=1)

        rows = [
            [("AC", "fn", "clear"), ("+/-", "fn", "negate"),
             ("%", "fn", "percent"), ("÷", "op", "divide")],
            [("7", "num", None), ("8", "num", None),
             ("9", "num", None), ("×", "op", "multiply")],
            [("4", "num", None), ("5", "num", None),
             ("6", "num", None), ("−", "op", "subtract")],
            [("1", "num", None), ("2", "num", None),
             ("3", "num", None), ("+", "op", "add")],
            [("0", "num", None), (",", "num", "decimal"),
             ("=", "op", "equals")],
        ]

        for r, row in enumerate(rows):
            c = 0
            for item in row:
                text, kind, action = item
                colspan = 1
                shape = "oval"
                if r == 4 and text == "0":
                    colspan = 2
                    shape = "pill"
                btn = self._make_button(pad, text, kind, action, shape)
                btn.grid(row=r, column=c, columnspan=colspan,
                         sticky="nsew", padx=6, pady=6)
                c += colspan

    def _make_button(self, parent, text, kind, action, shape):
        if kind == "fn":
            bg, active_bg, fg = FN_BG, FN_BG_ACTIVE, FN_FG
            font_size = 20
        elif kind == "op":
            bg, active_bg, fg = OP_BG, OP_BG_ACTIVE, OP_FG
            font_size = 26
        else:
            bg, active_bg, fg = NUM_BG, NUM_BG_ACTIVE, NUM_FG
            font_size = 22

        command = None
        if kind == "num" and action != "decimal":
            digit = text
            command = lambda d=digit: self.input_digit(d)
        elif action == "decimal":
            command = self.input_decimal
        elif action == "clear":
            command = self.reset_all
        elif action == "negate":
            command = self.negate
        elif action == "percent":
            command = self.percent
        elif action == "equals":
            command = self.equals
        elif kind == "op":
            command = lambda a=action: self.choose_operator(a)

        btn = RoundButton(
            parent, text=text, bg=bg, fg=fg, active_bg=active_bg,
            command=command, font=("Helvetica", font_size), shape=shape
        )

        if action == "clear":
            self.clear_btn = btn
        if kind == "op":
            self.op_buttons[action] = btn

        return btn

    def _bind_keys(self):
        self.bind("<Key>", self._on_key)

    # ---------------- Klavye ----------------
    def _on_key(self, event):
        ch = event.char
        if ch and ch.isdigit():
            self.input_digit(ch)
        elif ch in (".", ","):
            self.input_decimal()
        elif ch == "+":
            self.choose_operator("add")
        elif ch == "-":
            self.choose_operator("subtract")
        elif ch == "*":
            self.choose_operator("multiply")
        elif ch == "/":
            self.choose_operator("divide")
        elif event.keysym in ("Return", "KP_Enter"):
            self.equals()
        elif event.keysym == "BackSpace":
            self.backspace()
        elif event.keysym == "Escape":
            self.reset_all()
        elif ch == "%":
            self.percent()

    # ---------------- Yardimcilar ----------------
    def format_number(self, num_str):
        if num_str == "Hata":
            return num_str
        negative = num_str.startswith("-")
        if negative:
            num_str = num_str[1:]
        if "." in num_str:
            int_part, dec_part = num_str.split(".", 1)
        else:
            int_part, dec_part = num_str, None
        if len(int_part) > 15:
            int_part = int_part[:15]
        try:
            int_formatted = f"{int(int_part or '0'):,}".replace(",", ".")
        except ValueError:
            int_formatted = int_part
        result = int_formatted
        if dec_part is not None:
            result += "," + dec_part
        return ("-" if negative else "") + result

    def _update_display(self):
        text = self.format_number(self.current)
        self.display_var.set(text)
        length = len(text)
        size = 48
        if length > 9:
            size = max(20, 48 - (length - 9) * 3)
        self.display_label.configure(font=("Helvetica", size))

        if self.operator and self.previous is not None:
            symbols = {"add": "+", "subtract": "−", "multiply": "×", "divide": "÷"}
            self.history_var.set(f"{self.format_number(self.previous)} {symbols[self.operator]}")
        else:
            self.history_var.set(" ")

        if self.clear_btn:
            self.clear_btn.set_text("AC" if self.current == "0" and self.overwrite else "C")

        self._highlight_operator()

    def _highlight_operator(self):
        for action, btn in self.op_buttons.items():
            if action == self.operator and not self.overwrite:
                btn.set_colors(bg=OP_ACTIVE_BG, fg=OP_ACTIVE_FG)
            else:
                btn.set_colors(bg=OP_BG, fg=OP_FG)

    # ---------------- Islemler ----------------
    def input_digit(self, d):
        if self.current == "Hata":
            self.reset_all()
        if self.overwrite:
            self.current = d if d != "0" else "0"
            self.overwrite = False
        else:
            if self.current == "0":
                self.current = d
            elif len(self.current.replace("-", "").replace(".", "")) < 15:
                self.current += d
        self._update_display()

    def input_decimal(self):
        if self.current == "Hata":
            self.reset_all()
        if self.overwrite:
            self.current = "0."
            self.overwrite = False
        elif "." not in self.current:
            self.current += "."
        self._update_display()

    def negate(self):
        if self.current in ("Hata", "0"):
            return
        self.current = self.current[1:] if self.current.startswith("-") else "-" + self.current
        self._update_display()

    def percent(self):
        if self.current == "Hata":
            return
        val = float(self.current)
        self.current = self._trim(val / 100)
        self.overwrite = True
        self._update_display()

    def backspace(self):
        if self.current == "Hata":
            self.reset_all()
            return
        if not self.overwrite and len(self.current) > 1:
            self.current = self.current[:-1]
            if self.current == "-":
                self.current = "0"
        else:
            self.current = "0"
            self.overwrite = True
        self._update_display()

    def _compute(self, a, op, b):
        a, b = float(a), float(b)
        if op == "add":
            return a + b
        if op == "subtract":
            return a - b
        if op == "multiply":
            return a * b
        if op == "divide":
            if b == 0:
                return None
            return a / b
        return b

    def _trim(self, num):
        if num is None:
            return "Hata"
        s = f"{num:.12g}"
        return s

    def choose_operator(self, action):
        if self.current == "Hata":
            return
        if self.operator and not self.overwrite:
            result = self._compute(self.previous, self.operator, self.current)
            self.previous = self._trim(result)
            self.current = self.previous
            if self.current == "Hata":
                self._finish_error()
                return
        else:
            self.previous = self.current
        self.operator = action
        self.overwrite = True
        self._update_display()

    def _finish_error(self):
        self.current = "Hata"
        self.previous = None
        self.operator = None
        self.overwrite = True
        self._update_display()

    def equals(self):
        if self.current == "Hata":
            return
        if self.operator and not self.overwrite:
            a, op, b = self.previous, self.operator, self.current
            self.last_operator, self.last_operand = op, b
        elif self.last_operator and self.overwrite:
            a, op, b = self.current, self.last_operator, self.last_operand
        else:
            return
        result = self._compute(a, op, b)
        result_str = self._trim(result)
        if result_str == "Hata":
            self._finish_error()
            return
        self.current = result_str
        self.previous = None
        self.operator = None
        self.overwrite = True
        self._update_display()

    def reset_all(self):
        self.current = "0"
        self.previous = None
        self.operator = None
        self.overwrite = True
        self.last_operator = None
        self.last_operand = None
        self._update_display()

    # ---------------- Kopyalama ----------------
    def _start_hold(self, event):
        self._hold_id = self.after(500, self._copy_result)

    def _cancel_hold(self, event):
        if self._hold_id:
            self.after_cancel(self._hold_id)
            self._hold_id = None

    def _copy_result(self):
        text = self.format_number(self.current)
        self.clipboard_clear()
        self.clipboard_append(text)
        self._flash_copied()

    def _flash_copied(self):
        original_fg = self.display_label.cget("fg")
        self.display_label.configure(fg="#767676")
        self.after(150, lambda: self.display_label.configure(fg=original_fg))


if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
