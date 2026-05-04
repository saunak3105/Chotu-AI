# 🏪 Chotu AI: Vernacular Assistant for Kirana Stores

**Chotu** is an offline-first, modular AI assistant specifically designed for Kirana (small grocery) store owners. It enables shopkeepers to manage their business—inventory, billing, and analytics—using voice or text in their local language, all while running on low-cost, offline hardware.

---

## 🚀 Features

### 📦 Smart Inventory Management
- **Voice-Enabled Stock Updates**: "Add 10 Maggi" or "5 bread becha".
- **Low Stock Alerts**: Automatic tracking and highlighting of critical inventory levels.
- **Categorized Tracking**: Organize products for better management.

### 🛒 Modern POS & Billing
- **Quick Billing**: Create bills via voice commands or a touch-friendly UI.
- **Auto-Inventory Sync**: Every sale automatically deducts from the stock.
- **Multi-item support**: Handle complex orders seamlessly.

### 📈 Business Insights & Analytics
- **Daily Dashboard**: Real-time view of revenue, expenses, and net profit.
- **Weekly Trends**: Visual representation of sales performance over the last 7 days.
- **AI-Driven Insights**: Actionable suggestions like "Top selling product is Maggi" or "Stock up on Milk".

### 🗣️ Vernacular NLP & Offline Voice
- **Hindi-English Code-Switching**: Understands how shopkeepers actually speak (e.g., "Add 500 expense for bijli bill").
- **Offline First**: Works without internet using **Vosk** for speech recognition and **pyttsx3** for text-to-speech.
- **Privacy Focused**: No data leaves the device.

### 🔒 Security & Reliability
- **PIN Authentication**: Secure access to business data.
- **Local SQLite DB**: Robust data storage with zero cloud dependency.
- **Automatic Backups**: Keeps your business data safe.

---

## 🛠️ Tech Stack

- **UI Framework**: [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) (Modern Dark-themed GUI)
- **Speech Recognition**: [Vosk](https://alphacephei.com/vosk/) (Offline STT)
- **Speech Synthesis**: [pyttsx3](https://github.com/nateshmbhat/pyttsx3) (Offline TTS)
- **NLP**: Rule-based Entity Extraction & Intent Parsing
- **Database**: SQLite3
- **Language**: Python 3.8+

---

## 💻 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/chotu-ai.git
cd chotu-ai
```

### 2. Set Up Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

> **Note on PyAudio**: If `pyaudio` fails to install, you may need system-level dependencies:
> - **Linux**: `sudo apt-get install python3-pyaudio portaudio19-dev`
> - **macOS**: `brew install portaudio`
> - **Windows**: Usually installs via pip, otherwise download the `.whl` from unofficial sources.

### 4. Download Vosk Model
To enable voice features:
1. Download a small English or Hindi model from [Vosk Models](https://alphacephei.com/vosk/models).
2. Extract the model into a folder named `model` in the root directory.
3. Ensure the path matches `utils/constants.py` (default: `model/vosk-model-small-en-us-0.15`).

---

## 🎮 Usage

Run the main application:
```bash
python main.py
```

### Authentication
- **Default PIN**: `1234` (Configurable in `utils/constants.py`)

### Voice Commands Examples
| Goal | Command (English/Hindi) |
| :--- | :--- |
| **Add Stock** | "Add 10 Maggi" / "10 Maggi stock mein dalo" |
| **Sales** | "Sell 2 Bread" / "2 Bread becha" |
| **Billing** | "Bill 1 Milk and 2 Egg" |
| **Check Stock** | "How much Maggi is left?" / "Maggi kitna hai?" |
| **Expenses** | "Add 200 expense for tea" / "200 kharcha chai ke liye" |
| **Reports** | "Show sales report" / "Aaj ki kamai dikhao" |

---

## 📁 Project Structure

```text
├── main.py             # Entry point & Authentication
├── core/               # Business Logic (DB, Inventory, Billing)
├── ui/                 # GUI Components (CustomTkinter Frames)
├── nlp/                # Natural Language Processing & Intent Parsing
├── speech/             # STT (Vosk) and TTS (pyttsx3) integration
├── analytics/          # Business Intelligence & Reports
├── utils/              # Config, Logger, and Helpers
└── requirements.txt    # Project dependencies
```

---

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
