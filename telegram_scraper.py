#!/usr/bin/env python3
"""
Telegram Group File Scraper
============================
Scrapes files from Telegram groups and exports to CSV/JSON.

Requirements:
    pip install -r requirements.txt

Setup:
    1. Get API credentials from https://my.telegram.org/apps
    2. Copy config.example.py to config.py
    3. Add your API credentials to config.py
    4. Run: python telegram_scraper.py

Usage:
    python telegram_scraper.py --group mtforexeafree --limit 10000
    python telegram_scraper.py --group https://t.me/mtforexeafree --output my_files.csv
"""

import asyncio
import argparse
import csv
import json
import os
from datetime import datetime
from telethon import TelegramClient
from telethon.tl.types import MessageMediaDocument, DocumentAttributeFilename

# Try to import config, use defaults if not found
try:
    from config import API_ID, API_HASH, PHONE_NUMBER
except ImportError:
    print("⚠️  config.py not found. Copy config.example.py to config.py and add your credentials.")
    API_ID = None
    API_HASH = None
    PHONE_NUMBER = None


class TelegramFileScraper:
    """Scrape files from Telegram groups."""
    
    def __init__(self, session_name='scraper_session'):
        if not API_ID or not API_HASH:
            raise ValueError("API credentials not configured. Check config.py")
        
        self.client = TelegramClient(session_name, API_ID, API_HASH)
        self.files = []
        
    async def connect(self):
        """Connect to Telegram."""
        print("🔌 Connecting to Telegram...")
        await self.client.connect()
        
        if not await self.client.is_user_authorized():
            print("📱 Authorization required. Sending code to your phone...")
            await self.client.start(phone=PHONE_NUMBER)
            print("✅ Authorized!")
        else:
            print("✅ Connected!")
    
    def is_target_file(self, filename, file_types=None):
        """Check if file matches target types."""
        if not filename:
            return False
        
        if file_types is None:
            # Default: all common file types
            file_types = [
                '.ex4', '.ex5', '.mq4', '.mq5',  # MT4/MT5 EAs
                '.zip', '.rar', '.7z',  # Archives
                '.pdf', '.doc', '.docx', '.txt',  # Documents
                '.jpg', '.jpeg', '.png', '.gif',  # Images
                '.mp4', '.avi', '.mkv',  # Videos
                '.py', '.js', '.html',  # Code
            ]
        
        filename_lower = filename.lower()
        return any(filename_lower.endswith(ext) for ext in file_types)
    
    async def scrape_group(self, group_identifier, limit=10000, file_types=None):
        """
        Scrape files from a Telegram group.
        
        Args:
            group_identifier: Group username, ID, or URL (e.g., 'mtforexeafree' or 'https://t.me/mtforexeafree')
            limit: Maximum number of messages to scan
            file_types: List of file extensions to filter (None = all files)
        """
        print(f"\n📂 Scraping group: {group_identifier}")
        print(f"📊 Scanning last {limit} messages...\n")
        
        try:
            entity = await self.client.get_entity(group_identifier)
            group_title = entity.title
            print(f"📢 Group: {group_title}")
        except Exception as e:
            print(f"❌ Error getting group: {e}")
            return
        
        count = 0
        
        async for message in self.client.iter_messages(entity, limit=limit):
            # Check for document attachments
            if message.media and isinstance(message.media, MessageMediaDocument):
                doc = message.media.document
                filename = None
                
                # Get filename from attributes
                for attr in doc.attributes:
                    if isinstance(attr, DocumentAttributeFilename):
                        filename = attr.file_name
                        break
                
                # If no filename, try from document
                if not filename and hasattr(doc, 'name'):
                    filename = doc.name
                
                if filename and self.is_target_file(filename, file_types):
                    file_info = {
                        'filename': filename,
                        'message_id': message.id,
                        'date': message.date.strftime('%Y-%m-%d %H:%M:%S') if message.date else '',
                        'sender': self._get_sender_name(message),
                        'caption': (message.text or '')[:500],
                        'file_size_mb': round(doc.size / (1024 * 1024), 2) if doc.size else 0,
                        'message_url': f'https://t.me/{group_identifier}/{message.id}' if isinstance(group_identifier, str) and not group_identifier.startswith('http') else str(message.id)
                    }
                    self.files.append(file_info)
                    count += 1
                    print(f"  📄 [{count}] {filename} ({file_info['file_size_mb']} MB)")
        
        print(f"\n✅ Found {count} files")
    
    def _get_sender_name(self, message):
        """Extract sender name from message."""
        if not message.sender:
            return 'Unknown'
        
        if hasattr(message.sender, 'first_name'):
            if hasattr(message.sender, 'last_name') and message.sender.last_name:
                return f"{message.sender.first_name} {message.sender.last_name}"
            return message.sender.first_name
        
        if hasattr(message.sender, 'username') and message.sender.username:
            return f"@{message.sender.username}"
        
        return 'Unknown'
    
    def export_csv(self, output_path='scraped_files.csv'):
        """Export results to CSV."""
        if not self.files:
            print("⚠️  No files to export")
            return
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['filename', 'message_id', 'date', 'sender', 'caption', 'file_size_mb', 'message_url']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(self.files)
        
        print(f"\n📊 Exported to: {os.path.abspath(output_path)}")
    
    def export_json(self, output_path='scraped_files.json'):
        """Export results to JSON."""
        if not self.files:
            print("⚠️  No files to export")
            return
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.files, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Exported to: {os.path.abspath(output_path)}")
    
    def print_summary(self):
        """Print summary of scraped files."""
        if not self.files:
            return
        
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        
        # Count by extension
        extensions = {}
        total_size = 0
        
        for f in self.files:
            ext = os.path.splitext(f['filename'])[1].lower()
            extensions[ext] = extensions.get(ext, 0) + 1
            total_size += f['file_size_mb']
        
        print(f"\nTotal Files: {len(self.files)}")
        print(f"Total Size: {round(total_size, 2)} MB")
        
        print("\nBy Extension:")
        for ext, count in sorted(extensions.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {ext or 'no extension'}: {count}")
        
        # Top 10 largest
        print("\nTop 10 Largest Files:")
        sorted_files = sorted(self.files, key=lambda x: x['file_size_mb'], reverse=True)[:10]
        for i, f in enumerate(sorted_files, 1):
            print(f"  {i}. {f['filename']} ({f['file_size_mb']} MB)")
        
        print("\n" + "="*60)
    
    async def close(self):
        """Disconnect from Telegram."""
        await self.client.disconnect()
        print("\n👋 Disconnected")


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Scrape files from Telegram groups',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python telegram_scraper.py --group mtforexeafree --limit 10000
  python telegram_scraper.py --group https://t.me/mygroup --output files.csv
  python telegram_scraper.py --group mygroup --types .ex4 .ex5 .zip
        """
    )
    
    parser.add_argument('--group', '-g', required=True, 
                        help='Group username, ID, or URL (e.g., mtforexeafree)')
    parser.add_argument('--limit', '-l', type=int, default=10000,
                        help='Max messages to scan (default: 10000)')
    parser.add_argument('--output', '-o', default='scraped_files.csv',
                        help='Output CSV file (default: scraped_files.csv)')
    parser.add_argument('--types', '-t', nargs='+', default=None,
                        help='File types to filter (e.g., .ex4 .ex5 .zip)')
    parser.add_argument('--json', action='store_true',
                        help='Also export to JSON format')
    
    args = parser.parse_args()
    
    print("="*60)
    print("TELEGRAM GROUP FILE SCRAPER")
    print("="*60)
    
    try:
        scraper = TelegramFileScraper()
        await scraper.connect()
        await scraper.scrape_group(args.group, args.limit, args.types)
        scraper.export_csv(args.output)
        
        if args.json:
            scraper.export_json(args.output.replace('.csv', '.json'))
        
        scraper.print_summary()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await scraper.close()


if __name__ == '__main__':
    asyncio.run(main())
