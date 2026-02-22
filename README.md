# 📥 Telegram Group File Scraper

A powerful Python tool to scrape and export files from Telegram groups.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Telethon](https://img.shields.io/badge/Telethon-1.34+-green.svg)](https://docs.telethon.dev/)

---

## ✨ Features

- 🔍 **Scrape files** from any public/private Telegram group
- 📊 **Export to CSV/JSON** with full metadata
- 🎯 **Filter by file type** (.ex4, .ex5, .zip, .pdf, etc.)
- ⚡ **Fast async scraping** with Telethon
- 🔐 **Secure authentication** with Telegram API
- 📈 **Detailed summaries** and statistics
- 🎨 **Beautiful CLI output** with progress tracking

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Credentials

```bash
# Copy the example config
cp config.example.py config.py

# Edit config.py with your credentials
# Get them from: https://my.telegram.org/apps
```

### 3. Run the Scraper

```bash
# Basic usage
python telegram_scraper.py --group mtforexeafree --limit 10000

# With custom output
python telegram_scraper.py --group mygroup --output my_files.csv

# Filter specific file types
python telegram_scraper.py --group mygroup --types .ex4 .ex5 .zip

# Export to both CSV and JSON
python telegram_scraper.py --group mygroup --json
```

---

## 📖 Documentation

### Getting Telegram API Credentials

1. Go to https://my.telegram.org/apps
2. Log in with your phone number
3. Click "API development tools"
4. Create a new application
5. Copy **API ID** and **API Hash** to `config.py`

### Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--group` | `-g` | Group username, ID, or URL | **Required** |
| `--limit` | `-l` | Max messages to scan | 10000 |
| `--output` | `-o` | Output CSV file | scraped_files.csv |
| `--types` | `-t` | File types to filter | All files |
| `--json` | | Also export to JSON | False |

### Examples

```bash
# Scrape last 5000 messages
python telegram_scraper.py -g mygroup -l 5000

# Get only EA files
python telegram_scraper.py -g forexgroup -t .ex4 .ex5 .mq4 .mq5

# Scrape and export to custom file
python telegram_scraper.py -g tradinggroup -o trading_files.csv

# Use full group URL
python telegram_scraper.py -g https://t.me/mygroup
```

---

## 📊 Output Format

### CSV Columns

| Column | Description |
|--------|-------------|
| `filename` | File name |
| `message_id` | Telegram message ID |
| `date` | Message timestamp |
| `sender` | Who shared the file |
| `caption` | Message text (first 500 chars) |
| `file_size_mb` | File size in MB |
| `message_url` | Direct link to message |

### Example Output

```csv
filename,message_id,date,sender,caption,file_size_mb,message_url
Ninja_Bot_v13.ex4,51509,2026-02-18 15:40:05,Mr,Check this bot!,0.14,https://t.me/mygroup/51509
Strategy.zip,51486,2026-02-18 08:46:07,Brian,My trading strategy,2.45,https://t.me/mygroup/51486
```

---

## 🛠️ Advanced Usage

### Filter by File Type

```bash
# Only MT4/MT5 EAs
python telegram_scraper.py -g forexgroup -t .ex4 .ex5 .mq4 .mq5

# Only documents
python telegram_scraper.py -g group -t .pdf .doc .docx

# Only archives
python telegram_scraper.py -g group -t .zip .rar .7z
```

### Programmatic Usage

```python
import asyncio
from telegram_scraper import TelegramFileScraper

async def main():
    scraper = TelegramFileScraper()
    await scraper.connect()
    await scraper.scrape_group('mygroup', limit=5000)
    scraper.export_csv('output.csv')
    scraper.print_summary()
    await scraper.close()

asyncio.run(main())
```

---

## ⚠️ Important Notes

### Rate Limits
- Telegram has API rate limits
- Don't scrape too many messages too quickly
- The scraper handles this automatically

### Privacy
- Respect group rules and privacy
- Don't share private data without permission
- Some groups may ban bots

### Authentication
- Your session file (`*.session`) contains auth tokens
- **Never share your session file**
- Keep `config.py` private (it's in .gitignore)

---

## 🐛 Troubleshooting

### "config.py not found"
```bash
cp config.example.py config.py
# Edit config.py with your credentials
```

### "Phone number code invalid"
- Make sure format is correct: `+1234567890`
- Check the SMS/code from Telegram
- Codes expire quickly - use fresh ones

### "No files found"
- Check if group has files
- Try increasing the limit
- Verify you're a group member (for private groups)

### "Flood wait error"
- Telegram rate limit
- Wait a few minutes and try again
- Reduce the limit parameter

---

## 📁 Project Structure

```
telegram-group-file-scraper/
├── telegram_scraper.py      # Main scraper script
├── config.example.py        # Configuration template
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── LICENSE                 # MIT License
├── .gitignore             # Git ignore rules
└── docs/                  # Website (GitHub Pages)
    ├── index.html
    ├── styles.css
    └── script.js
```

---

## 🌐 Website

Check out the interactive website:  
**https://siraj637909.github.io/telegram-group-file-scraper/**

---

## 🤝 Contributing

Contributions welcome! Here's how:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Telethon](https://github.com/LonamiWebs/Telethon) - Amazing Telegram library
- [Telegram](https://telegram.org/) - For the API
- Community contributors and testers

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/Siraj637909/telegram-group-file-scraper/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Siraj637909/telegram-group-file-scraper/discussions)

---

**Made with ❤️ by Shaokh Shaikh**

[![Star this repo](https://img.shields.io/github/stars/Siraj637909/telegram-group-file-scraper?style=social)](https://github.com/Siraj637909/telegram-group-file-scraper)
