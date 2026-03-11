# パントリー - 家庭用在庫管理アプリ

夫婦2人で使う家庭用日用品の在庫管理Webアプリ。楽天お買い物マラソンのまとめ買いタイミングに合わせて在庫補充を効率化します。

## セットアップ

### 1. Supabaseでテーブルを作成

```sql
create table items (
  id bigserial primary key,
  category text not null,
  name text not null,
  quantity integer not null default 0,
  is_low_stock_alert boolean not null default false,
  created_at timestamptz default now()
);

create table settings (
  id integer primary key default 1,
  next_marathon_start date,
  next_marathon_end date
);

insert into settings (id) values (1);
```

### 2. secrets.toml を設定

`.streamlit/secrets.toml` にSupabaseの接続情報を入力：

```toml
[supabase]
url = "https://xxxxxxxxxx.supabase.co"
key = "your-anon-key"
```

### 3. 依存パッケージをインストール

```bash
pip install -r requirements.txt
```

### 4. 起動

```bash
streamlit run app.py
```

## Streamlit Community Cloud へのデプロイ

1. GitHubリポジトリを作成してpush（`secrets.toml` は `.gitignore` 済み）
2. [share.streamlit.io](https://share.streamlit.io) で「New app」
3. GitHubリポジトリ・ブランチ・`app.py` を指定
4. 「Advanced settings」→ Secrets に `secrets.toml` の内容を貼り付け
5. デプロイ完了
