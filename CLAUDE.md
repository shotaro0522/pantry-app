# パントリー（家庭用在庫管理アプリ）実装指示書

## プロジェクト概要

夫婦2人で使う家庭用日用品の在庫管理Webアプリ。
スマートフォンのブラウザで使用し、楽天お買い物マラソンのまとめ買いタイミングに合わせて在庫補充を効率化する。

---

## 技術スタック

| 項目 | 内容 |
|------|------|
| フレームワーク | Streamlit |
| DB | Supabase（PostgreSQL） |
| デプロイ先 | Streamlit Community Cloud |
| ソース管理 | GitHub |
| 対象端末 | スマートフォン（ブラウザ） |
| 認証 | なし（認証不要） |

---

## ディレクトリ構成

```
pantry/
├── .streamlit/
│   └── secrets.toml        # Supabase接続情報（ローカル用、gitignore対象）
├── app.py                  # メインアプリ
├── db.py                   # Supabase接続・CRUD処理
├── requirements.txt
└── README.md
```

---

## Supabase テーブル設計

### テーブル①: `items`（在庫アイテム）

```sql
create table items (
  id bigserial primary key,
  category text not null,         -- 分類
  name text not null,             -- 品目名
  quantity integer not null default 0,  -- 在庫数
  is_low_stock_alert boolean not null default false,  -- 在庫少ない一覧に表示するか
  created_at timestamptz default now()
);
```

### テーブル②: `settings`（アプリ設定）

```sql
create table settings (
  id integer primary key default 1,   -- 常に1行のみ
  next_marathon_start date,           -- 次回マラソン開始日
  next_marathon_end date              -- 次回マラソン終了日
);

-- 初期データ挿入
insert into settings (id) values (1);
```

---

## ビジネスロジック

### 在庫アラート自動判定
- `quantity` が **1以下** になった場合、`is_low_stock_alert` を **自動でtrue** にする
- それ以外は **手動でON/OFFを切り替え** できる
- 更新時に毎回チェックして自動反映する

### カテゴリ一覧（固定値）
```python
CATEGORIES = ["キッチン", "お風呂", "洗面所", "トイレ"]
```

---

## 画面構成

Streamlitのサイドバー or タブで以下3画面を切り替える。

### 画面①: 在庫一覧

- カテゴリごとにセクション分けして全アイテムを表示
- 各アイテムに `➕` / `➖` ボタンで在庫数を1ずつ増減
- `is_low_stock_alert = true` のアイテムは ⚠️ アイコンや赤文字で強調表示
- 在庫数が0のアイテムは特に目立つ表示にする

### 画面②: 在庫少ない一覧

- `is_low_stock_alert = true` のアイテムのみ表示
- カテゴリ別にグループ化
- 画面上部に次回マラソン日を表示
  ```
  🛒 次回マラソン：3月21日（土）〜 3月27日（金）
  ```
  未設定の場合は「次回マラソン日未設定」と表示

### 画面③: 登録・編集

**新規登録フォーム**
- カテゴリ（セレクトボックス）
- 品目名（テキスト入力）
- 初期在庫数（数値入力、デフォルト:0）
- 在庫少ない一覧に表示（チェックボックス）
- 「登録」ボタン

**アイテム一覧（編集・削除）**
- 全アイテムをリスト表示
- 各アイテムに「編集」「削除」ボタン
- 編集時はフォームに現在値を展開して更新

**マラソン日設定**
- 次回マラソン開始日・終了日の日付入力
- 「保存」ボタン

---

## db.py の実装方針

```python
from supabase import create_client
import streamlit as st

def get_client():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

# 実装すべき関数
def get_all_items() -> list[dict]
def get_low_stock_items() -> list[dict]
def add_item(category, name, quantity, is_low_stock_alert) -> None
def update_quantity(item_id, new_quantity) -> None
    # quantity <= 1 の場合は is_low_stock_alert を True に自動設定
def update_item(item_id, category, name, quantity, is_low_stock_alert) -> None
    # quantity <= 1 の場合は is_low_stock_alert を True に強制
def delete_item(item_id) -> None
def get_settings() -> dict
def update_marathon_dates(start_date, end_date) -> None
```

---

## .streamlit/secrets.toml（ローカル開発用）

```toml
[supabase]
url = "https://xxxxxxxxxx.supabase.co"
key = "your-anon-key"
```

Streamlit Community Cloud へのデプロイ時は、管理画面の「Secrets」に同内容を設定する。

---

## requirements.txt

```
streamlit>=1.32.0
supabase>=2.3.0
```

---

## スマートフォン対応の注意点

- ボタンは十分な大きさにする（`use_container_width=True` を活用）
- `st.columns` で ➕/➖ ボタンを横並びにする
- テキストは読みやすいサイズを意識する
- ページ幅は `st.set_page_config(layout="centered")` を使用

---

## 実装の順番（推奨）

1. Supabaseでテーブルを作成・初期データ投入
2. `db.py` を実装してSupabase接続を確認
3. 画面③（登録・編集）を実装してデータ登録できる状態に
4. 画面①（在庫一覧）を実装
5. 画面②（在庫少ない一覧）を実装
6. GitHubにpushしてStreamlit Community Cloudにデプロイ

---

## デプロイ手順メモ

1. GitHubリポジトリを作成（`pantry` など）
2. 上記ファイルをpush（`secrets.toml` は `.gitignore` に追加）
3. [share.streamlit.io](https://share.streamlit.io) にアクセス
4. 「New app」→ GitHubリポジトリ・ブランチ・`app.py` を指定
5. 「Advanced settings」→ Secrets に `secrets.toml` の内容を貼り付け
6. デプロイ完了
