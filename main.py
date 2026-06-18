import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui import GIFStudioApp


def main():
    """
    Main entry point for GIF Studio Pro.
    """
    try:
        app = GIFStudioApp()
        app.mainloop()
    except Exception as e:
        print(f'CRITICAL ERROR: Failed to start application: {e}')
        input('Press Enter to exit...')


if __name__ == '__main__':
    main()
