"""
Main entry point for MyTempo application.
"""

from src.app.mytempo_app import MyTempoApp


def main():
    """Main function to start the application."""
    app = MyTempoApp()
    app.run()


if __name__ == '__main__':
    main() 