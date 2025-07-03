# MyTempo

A modern, elegant Markdown reader application with smooth scrolling and beautiful typography.

## Features

- **Beautiful Typography**: Dual-font system with Noto Sans SC for Chinese and Inter for English
- **Smooth Scrolling**: Adjustable scroll speed with keyboard controls
- **Opacity Control**: Adjustable window transparency
- **Font Size Control**: Dynamic font size adjustment
- **Drag & Drop**: Easy file loading with drag and drop support
- **Markdown Support**: Full Markdown syntax support including headings, quotes, and formatting
- **Settings Persistence**: User preferences are automatically saved

## Project Structure

```
MyTempo/
├── src/                          # Source code directory
│   ├── main.py                   # Application entry point
│   ├── app/                      # Application components
│   │   ├── mytempo_app.py        # Main application class
│   │   └── document_viewer.py    # Document viewer component
│   ├── ui/                       # User interface components
│   │   ├── loading_window.py     # Loading window
│   │   ├── upload_interface.py   # File upload interface
│   │   └── styles.py             # UI styles and themes
│   ├── core/                     # Core functionality
│   │   ├── config.py             # Configuration management
│   │   ├── text_processor.py     # Markdown text processing
│   │   └── scroll_manager.py     # Scroll management
│   └── utils/                    # Utilities
│       ├── constants.py          # Application constants
│       └── font_loader.py        # Font loading utilities
├── fonts/                        # Font files
├── run.py                        # Launch script
├── main.py                       # Legacy entry point (deprecated)
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── LICENSE                       # License file
└── user_settings.json            # User settings (auto-generated)
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/XujunNoahWang/mytempo.git
cd mytempo
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python run.py
```

## Usage

### File Loading
- Drag and drop Markdown files onto the application window
- Click "Browse Files" to select files manually
- Only `.md` and `.markdown` files are supported

### Keyboard Controls

#### Document Navigation
- **Up/Down Arrow**: Scroll up/down
- **Page Up/Page Down**: Scroll by page
- **Home/End**: Jump to start/end of document
- **Hold Down Arrow**: Start smooth scrolling
- **Release Down Arrow**: Stop smooth scrolling

#### Display Settings
- **Left/Right Arrow**: Decrease/increase font size
- **+/-**: Increase/decrease scroll speed
- ***/**: Increase/decrease window opacity
- **Escape** or **Ctrl+W**: Close document viewer

### Features

#### Typography
- Automatic font selection based on character type
- Chinese characters use Noto Sans SC
- English characters use Inter
- Support for bold, italic, and highlight formatting

#### Markdown Support
- Headings (H1-H6)
- Bold text (`**text**`)
- Italic text (`*text*` or `_text_`)
- Highlighted text (`==text==`)
- Quoted text (`> text`)
- Horizontal lines (`---`)

#### Settings
- Font size (20px to 72px)
- Scroll speed (1x to 5x)
- Window opacity (10% to 100%)
- Window size and position

## Development

### Code Structure

The application follows clean architecture principles:

- **Separation of Concerns**: Each module has a single responsibility
- **Dependency Injection**: Components are loosely coupled
- **Configuration Management**: Centralized settings management
- **Error Handling**: Comprehensive error handling throughout

### Key Components

- **MyTempoApp**: Main application coordinator
- **DocumentViewer**: Document display and interaction
- **UploadInterface**: File selection and drag-drop
- **TextProcessor**: Markdown parsing and formatting
- **ScrollManager**: Scroll behavior management
- **StyleManager**: UI styling and theming

### Adding Features

1. **New UI Components**: Add to `src/ui/`
2. **Core Functionality**: Add to `src/core/`
3. **Utilities**: Add to `src/utils/`
4. **Constants**: Update `src/utils/constants.py`

## Requirements

- Python 3.7+
- tkinter (usually included with Python)
- tkinterdnd2

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Version History

- **v0.4.3**: Complete code refactoring with modular architecture
- **v0.4.2**: Fixed horizontal line rendering
- **v0.4.1**: Improved text processing
- **v0.4.0**: Added opacity control
- **v0.3.0**: Added scroll speed control
- **v0.2.0**: Added font size control
- **v0.1.0**: Initial release with basic functionality 