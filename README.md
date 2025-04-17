# KeyboardCat

KeyboardCat is a desktop pet application inspired by Bongo Cat. It tracks your keyboard activity, reminds you to take breaks, and rewards you with new cat colors as you reach milestones.

## Features

- **Keyboard Tracking**: Records the number of keyboard presses over time.
- **Rest Reminders**: Prompts you to take a break at regular intervals.
- **Color Unlocks**: Unlock new cat colors every 10,000 key presses.

## Prerequisites

- Python >= 3.12.0

## Installation

### 1. Set Up a Virtual Environment (Recommended)

To avoid dependency conflicts, create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 2. Install Dependencies

Install the required Python packages listed in requirements.txt:

```bash
pip install -r requirements.txt
```

### 3. Run the Application

Execute the main script to start KeyboardCat:

```bash
python keyboard_cat.py
```

## Packaging

To create a standalone executable, use PyInstaller. Ensure you have the necessary files (e.g., cat_icon.ico) in the project directory.

### Without UPX

```bash
pyinstaller --noconsole --name KeyboardCat --icon=cat_icon.ico --add-data "cat_icon.ico;." --hidden-import=pystray --hidden-import=PIL.Image --hidden-import=keyboard keyboard_cat.py
```

### With UPX (Optional)

If UPX is installed, use the following command to reduce the executable size. Replace your\path\to\upx with the actual path to the UPX directory:

```bash
pyinstaller --noconsole --name KeyboardCat --icon=cat_icon.ico --add-data "cat_icon.ico;." --hidden-import=pystray --hidden-import=PIL.Image --hidden-import=keyboard --upx-dir your\path\to\upx --upx-exclude keyboard.pyd keyboard_cat.py
```

### Output

The packaged executable will be located in the dist directory and can be run directly.

## Notes

- Ensure cat_icon.ico is in the project directory for the icon to work correctly.

- The keyboard library may require administrator privileges on some systems.

- If you encounter issues with dependencies, verify that your Python version is >= 3.12.0 and that pip is up to date:

  ```bash
  pip install --upgrade pip
  ```

## License

This project is licensed under the MIT License (or specify your preferred license).
