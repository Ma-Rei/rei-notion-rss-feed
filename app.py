#!/usr/bin/env python3
"""
Rei Notionの記事をフィルタリングしたRSSフィードを配信するFlaskサーバー
Render用バージョン
"""

from flask import Flask, Response
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import logging
import os

app = Flask(__name__)

# ロギング設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_and_filter_rss():
    """LifeHacker JapanのRSSフィードを取得してRei Notionの記事をフィルタリング"""
    try:
        # LifeHacker JapanのRSSフィードを取得
        url = "https://www.lifehacker.jp/feed/index.xml"
        response = requests.get(url, timeout=10)
        response.encoding = 'utf-8'
        rss_content = response.text
        
        # 名前空間を定義
        namespaces = {
            'dc': 'http://purl.org/dc/elements/1.1/',
            'content': 'http://purl.org/rss/1.0/modules/content/',
            'atom': 'http://www.w3.org/2005/Atom'
        }
        
        root = ET.fromstring(rss_content)
        
        # チャンネル情報を取得
        channel = root.find('channel')
        
        # Rei Notionの記事をフィルタリング
        items = root.findall('.//item')
        rei_notion_items = []
        
        for item in items:
            creator = item.find('{%s}creator' % namespaces['dc'])
            if creator is not None and creator.text == 'Rei丨暮らしとNotion。':
                rei_notion_items.append(item)
        
        # 手動でXMLを構築（重複属性を避ける）
        xml_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:atom="http://www.w3.org/2005/Atom">',
            '<channel>'
        ]
        
        # チャンネル情報を追加
        title = channel.find('title')
        if title is not None and title.text:
            xml_lines.append(f'<title>{escape_xml(title.text)} - Rei丨暮らしとNotion。</title>')
        
        xml_lines.append('<description>Rei丨暮らしとNotion。の記事のみを配信します。</description>')
        xml_lines.append('<link>https://www.lifehacker.jp/author/rei_notion/</link>')
        xml_lines.append(f'<lastBuildDate>{datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")}</lastBuildDate>')
        xml_lines.append('<atom:link href="https://www.lifehacker.jp/feed/author/rei_notion/index.xml" rel="self" type="application/rss+xml" />')
        xml_lines.append('<language>ja</language>')
        
        # 記事を追加（URLのみを含める）
        for item in rei_notion_items:
            xml_lines.append('<item>')
            
            # タイトル（URLのみなので、URLを説明として使用）
            link_elem = item.find('link')
            if link_elem is not None and link_elem.text:
                # タイトルはURLのみ
                xml_lines.append(f'<title>{escape_xml(link_elem.text)}</title>')
                # 説明は空
                xml_lines.append('<description></description>')
                # リンク
                xml_lines.append(f'<link>{escape_xml(link_elem.text)}</link>')
                
                # GUID
                guid_elem = item.find('guid')
                if guid_elem is not None and guid_elem.text:
                    is_perma = guid_elem.get('isPermaLink', 'true')
                    xml_lines.append(f'<guid isPermaLink="{is_perma}">{escape_xml(guid_elem.text)}</guid>')
                
                # 公開日
                pubdate_elem = item.find('pubDate')
                if pubdate_elem is not None and pubdate_elem.text:
                    xml_lines.append(f'<pubDate>{escape_xml(pubdate_elem.text)}</pubDate>')
            
            xml_lines.append('</item>')
        
        xml_lines.append('</channel>')
        xml_lines.append('</rss>')
        
        return '\n'.join(xml_lines)
        
    except Exception as e:
        logger.error(f"Error fetching or filtering RSS: {e}")
        raise

def escape_xml(text):
    """XMLの特殊文字をエスケープ"""
    if text is None:
        return ''
    text = str(text)
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&apos;')
    return text

@app.route('/feed/author/rei_notion/index.xml')
def rei_notion_feed():
    """Rei Notionの記事をフィルタリングしたRSSフィードを配信"""
    try:
        rss_content = fetch_and_filter_rss()
        return Response(rss_content, mimetype='application/rss+xml; charset=utf-8')
    except Exception as e:
        logger.error(f"Error in feed endpoint: {e}")
        return Response("Error generating feed", status=500, mimetype='text/plain')

@app.route('/health')
def health():
    """ヘルスチェックエンドポイント"""
    return {'status': 'ok'}, 200

@app.route('/')
def index():
    """ルートエンドポイント"""
    return '''
    <html>
    <head>
        <title>Rei Notion RSS Feed</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>Rei Notion RSS Feed Generator</h1>
        <p>LifeHacker JapanのRSSフィードからRei Notionの著者の記事だけをフィルタリングして配信します。</p>
        
        <h2>RSSフィードURL</h2>
        <p><code>/feed/author/rei_notion/index.xml</code></p>
        
        <h2>著者情報</h2>
        <ul>
            <li>著者名: Rei丨暮らしとNotion。</li>
            <li>公式サイト: <a href="https://kurashi-notion.com/">https://kurashi-notion.com/</a></li>
            <li>YouTube: <a href="https://www.youtube.com/@rei_notion">https://www.youtube.com/@rei_notion</a></li>
            <li>X: <a href="https://x.com/rei_notion">https://x.com/rei_notion</a></li>
            <li>Instagram: <a href="http://instagram.com/rei_notion">http://instagram.com/rei_notion</a></li>
        </ul>
        
        <h2>使い方</h2>
        <p>RSSリーダーに以下のURLを登録してください:</p>
        <pre>/feed/author/rei_notion/index.xml</pre>
    </body>
    </html>
    '''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
