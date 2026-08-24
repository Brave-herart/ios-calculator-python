# 🧮 iOS-Style Calculator

A personal calculator application for Windows, developed with Python and Tkinter, inspired by the default iPhone Calculator app.

## 📖 About the Project

This project is my first personal project, developed for educational purposes. My goal was both to improve my desktop application development skills in Python and to learn how to translate the design and behavior of a real-world application—the iPhone Calculator—into code without compromising its original design.

## ✨ Features

### Basic Mathematical Operations

* Addition (`+`), subtraction (`−`), multiplication (`×`), and division (`÷`)
* Percentage (`%`) — divides the entered number by 100
* Sign change (`+/−`) — toggles between positive and negative values
* Decimal numbers — supports decimal input using a comma (`,`)
* Chained operations — multiple operations can be performed consecutively (e.g., `5 + 3 × 2`)
* Repeated equals — after obtaining a result, pressing `=` again repeats the last operation, just like the real iPhone Calculator

### Display and Interface

* **Operation history indicator** — displays the previous number and operation symbol at the top (e.g., `8 ×`)
* **Automatic font-size reduction** — automatically decreases the text size so long numbers fit on the display
* **Thousands separator formatting** — large numbers are grouped using periods (e.g., `1.234.567`)
* **Error handling** — invalid operations such as division by zero display an `"Error"` message, which can be cleared using `AC`
* **AC / C behavior** — when the display is zero, the button shows `AC` (clears everything); during an active operation, it changes to `C` (clears the current input)

### iOS-Inspired Design

* **Fully rounded/circular buttons** — buttons are manually drawn as circles and rounded shapes using the Tkinter Canvas
* **Pill-shaped `0` button** — designed like the real iPhone Calculator, spanning two columns
* **Color coding:**

  * Orange buttons → operation keys (`÷`, `×`, `−`, `+`, `=`)
  * Gray buttons → utility keys (`AC`, `+/−`, `%`)
  * Dark gray → number keys
* **Active operator highlighting** — the selected operator button (e.g., `+`) changes to a lighter orange while active
* **Black background and title bar** — the Windows title bar is customized to black using the Windows DWM API through `ctypes`
* **Minimal window appearance** — the title bar displays `"Calculator"`
* **Button press animations** — buttons change color when clicked to provide visual feedback
* **High-DPI support** — automatically adapts to Windows display scaling settings to prevent blurry or pixelated rendering

### Keyboard Support

| Key         | Function                                        |
| ----------- | ----------------------------------------------- |
| `0–9`       | Number input                                    |
| `.` or `,`  | Decimal point/comma                             |
| `+ - * /`   | Addition, subtraction, multiplication, division |
| `Enter`     | Calculate result (`=`)                          |
| `Backspace` | Delete the last entered digit                   |
| `Esc`       | Clear the entire display (`AC`)                 |
| `%`         | Percentage operation                            |

### Additional Features

* **Copy result to clipboard** — holding the display for 500 ms copies the current result directly to the clipboard, accompanied by a brief visual flash effect as confirmation
* **Resizable window** — buttons and display automatically scale according to the window size
* **Up to 15-digit number support** — input longer than 15 digits is automatically restricted

## 🛠️ Technologies Used

* **Python 3** — primary programming language
* **Tkinter** — Python's standard GUI framework
* **Canvas** — used to manually draw circular and rounded buttons
* **ctypes** — used to access Windows API functions for title bar customization and DPI configuration

## 🚀 Installation and Usage

If Python is already installed, no additional libraries are required, as Tkinter is included with Python.

Run the following command:

```bash
python calculator.py
```

## 📂 File Structure

```text
├── calculator.py     # Python (Tkinter) desktop application
└── README.md
```

## 🎯 Concepts Learned

* Window and widget management with Tkinter
* Custom drawing on Canvas, including circles and rounded rectangles
* Event-driven programming, including mouse clicks, keyboard input, and long-press interactions
* State management using calculator state-machine logic
* Accessing the Windows API through `ctypes`
* Implementing visual feedback and micro-interactions in user interfaces

## 📌 Future Plans

* Scientific calculator mode with a side-panel transition
* Full calculation history
* Unit and currency conversion features

## 📄 License

This project is a personal educational project.
