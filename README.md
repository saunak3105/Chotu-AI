# Chotu: Offline Vernacular AI for Kirana Stores

Chotu is a modular, offline-first AI assistant designed for low-cost hardware to help kirana store owners manage their business using voice or text in their local language.

## Features
- **Inventory Management**: Add, update, and track stock levels.
- **Billing**: Create bills and automatically update inventory.
- **Expense Tracking**: Log and categorize business expenses.
- **Business Insights**: Daily sales summaries and top-selling product reports.
- **Vernacular NLP**: Rule-based parsing of Hindi/English commands (e.g., "3 maggi add karo").
- **Offline Speech**: Integrated with Vosk (STT) and pyttsx3 (TTS) for offline interaction.
- **Security**: PIN-based authentication.
- **Reliability**: Local database with automatic backup system.

## Project Structure
```
/core
    db.py           # Database connection and schema
    inventory.py    # Inventory logic
    billing.py      # Billing logic
    expense.py      # Expense tracking
    seed.py         # Initial data seeding
/nlp
    intent_parser.py   # Intent classification
    entity_extractor.py # Quantity and item extraction
/speech
    stt.py          # Speech-to-Text (Vosk/Fallback)
    tts.py          # Text-to-Speech (pyttsx3/Fallback)
/analytics
    insights.py     # Business intelligence
/utils
    constants.py    # Configuration and constants
    helpers.py      # Backup and formatting utilities
main.py             # System integration and UI loop
```

## Setup Instructions

### 1. Requirements
- Python 3.8+
- SQLite3 (built-in)

### 2. Install Dependencies
```bash
pip install pyttsx3 vosk pyaudio
```
*Note: If `pyaudio` or `vosk` fail to install due to missing system headers, the system will automatically fall back to text-based input.*

### 3. Vosk Model (Optional for Voice)
To enable offline voice recognition:
1. Download a small Vosk model (e.g., `vosk-model-small-en-us-0.15` or Hindi model).
2. Extract it to a folder named `model` in the project root.

### 4. Run the Application
```bash
python main.py
```
- **Default PIN**: `1234`
- **Example Commands**:
    - "Add 10 maggi"
    - "3 bread becha" (Sell 3 bread)
    - "Stock check karo"
    - "Show sales report"
    - "Add 500 expense for electricity"

## Technical Highlights
- **No Internet Required**: Everything runs locally on the device.
- **Memory Efficient**: Uses SQLite and rule-based NLP to keep RAM usage < 2GB.
- **Vernacular Support**: Understands common Hindi/English code-switching used by shopkeepers.
