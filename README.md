# Rei Notion RSS Feed Generator

LifeHacker JapanのRSSフィードからRei Notionの著者の記事だけをフィルタリングして配信するRSSフィードジェネレーターです。

## 概要

このアプリケーションは、LifeHacker Japan全体のRSSフィードを取得し、著者「Rei丨暮らしとNotion。」の記事のみをフィルタリングして、新しいRSSフィードとして配信します。

## 機能

- ✅ LifeHacker Japanの全記事から自動フィルタリング
- ✅ Rei Notionの記事のみを配信
- ✅ MEE6などのDiscordボットに対応
- ✅ リアルタイム更新
- ✅ 標準的なRSS 2.0形式

## エンドポイント

### RSSフィード
```
GET /feed/author/rei_notion/index.xml
```

Rei Notionの記事のみを含むRSSフィード

**Content-Type**: `application/rss+xml; charset=utf-8`

### ヘルスチェック
```
GET /health
```

サーバーの稼働状況を確認

**レスポンス**: `{"status":"ok"}`

### ホームページ
```
GET /
```

アプリケーションの情報ページ

## 使い方

### RSSリーダーで購読

以下のURLをRSSリーダーに登録してください：

```
https://your-render-url.onrender.com/feed/author/rei_notion/index.xml
```

### MEE6で使用

1. MEE6ダッシュボードにアクセス
2. Feedプラグインを有効化
3. 上記のURLを登録

### ローカルで実行

```bash
# 依存パッケージをインストール
pip install -r requirements.txt

# サーバーを起動
python app.py
```

サーバーは `http://localhost:5000` で起動します。

## 技術スタック

- **フレームワーク**: Flask
- **言語**: Python 3.11
- **ホスティング**: Render
- **データソース**: LifeHacker Japan RSS Feed

## 環境変数

| 変数 | 説明 | デフォルト |
|------|------|----------|
| `PORT` | サーバーのポート番号 | 5000 |

## 著者情報

**Rei丨暮らしとNotion。**

- 公式サイト: https://kurashi-notion.com/
- YouTube: https://www.youtube.com/@rei_notion
- X（Twitter）: https://x.com/rei_notion
- Instagram: http://instagram.com/rei_notion

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 注記

このRSSフィードはLifeHacker Japanの公開情報を基に生成されています。LifeHacker Japanの利用規約に従ってください。

## サポート

問題が発生した場合は、GitHubのIssueを作成してください。

---

**最終更新**: 2025年12月7日
