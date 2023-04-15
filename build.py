import PyInstaller.__main__

"""PyInstaller build script for Fitnate."""
# Run this script with `python build.py` to build the executable.
# Full documentation: https://pyinstaller.org/en/stable/usage.html

PyInstaller.__main__.run([
    '--name', 'Fitnate', # Name of the executable file
    '-i', 'assets/icon.ico', # Installer icon
    '--add-data', 'assets/icon.ico;assets', # Add app icon to the executable
    '--add-data', 'c:/users/mehdi/appdata/local/programs/python/python310/lib/site-packages/customtkinter;customtkinter', # Add customtkinter folder to the executable
    '--onefile', # Pack all files into one executable (alternative: '--onedir', recommended for customtkinter apps)
    '--windowed', # Hide console window
    '--noconfirm', # Replace output directory (default: SPECPATH/dist/SPECNAME) without asking for confirmation
    '--clean', # Clean PyInstaller cache and remove temporary files before building
    'main.py', # main script
])
