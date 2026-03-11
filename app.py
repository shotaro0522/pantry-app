import streamlit as st
from datetime import date
import db

CATEGORIES = ["キッチン", "お風呂", "洗面所", "トイレ"]

CATEGORY_ICONS = {
    "キッチン": "🍳",
    "お風呂": "🛁",
    "洗面所": "🪥",
    "トイレ": "🚽",
}

st.set_page_config(
    page_title="パントリー",
    page_icon="🏠",
    layout="centered",
)

st.markdown("""
<style>
/* ── ベース ── */
[data-testid="stAppViewContainer"] {
    background: #f8f7f4;
}
[data-testid="stHeader"] {
    background: transparent;
}

/* ── タイトル ── */
.app-title {
    text-align: center;
    font-size: 1.6rem;
    font-weight: 700;
    color: #3d3530;
    padding: 0.6rem 0 0.2rem;
    letter-spacing: 0.04em;
}
.app-subtitle {
    text-align: center;
    font-size: 0.8rem;
    color: #9e9189;
    margin-bottom: 1rem;
}

/* ── タブ ── */
[data-testid="stTabs"] button {
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    color: #9e9189 !important;
    border-radius: 8px 8px 0 0 !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #c0392b !important;
    border-bottom: 3px solid #c0392b !important;
}

/* ── カテゴリヘッダー ── */
.cat-header {
    background: #ffffff;
    border-left: 4px solid #c0392b;
    padding: 0.45rem 0.8rem;
    border-radius: 0 8px 8px 0;
    font-size: 1rem;
    font-weight: 700;
    color: #3d3530;
    margin: 1.2rem 0 0.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

/* ── アイテムカード ── */
.item-card {
    background: #ffffff;
    border-radius: 10px;
    padding: 0.55rem 0.8rem;
    margin-bottom: 0.4rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.07);
    display: flex;
    align-items: center;
}
.item-name {
    font-size: 0.95rem;
    font-weight: 600;
    color: #3d3530;
}
.item-qty {
    font-size: 0.85rem;
    color: #7a6f68;
    margin-top: 1px;
}
.item-low {
    color: #e67e22;
}
.item-zero {
    color: #c0392b;
}

/* ── 在庫バッジ ── */
.badge {
    display: inline-block;
    padding: 2px 9px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 700;
}
.badge-ok   { background: #eafaf1; color: #27ae60; }
.badge-low  { background: #fef9e7; color: #e67e22; }
.badge-zero { background: #fdecea; color: #c0392b; }

/* ── ➕ ➖ ボタン ── */
button[kind="secondary"] {
    border-radius: 8px !important;
    font-size: 1.05rem !important;
    padding: 0.25rem !important;
    border: 1px solid #e0dbd7 !important;
    background: #faf9f7 !important;
    color: #3d3530 !important;
}
button[kind="secondary"]:hover {
    background: #f0ece8 !important;
    border-color: #c0392b !important;
}

/* ── プライマリボタン ── */
button[kind="primary"],
[data-testid="baseButton-primary"] {
    background: #c0392b !important;
    border: none !important;
    border-radius: 10px !important;
    color: white !important;
    font-weight: 700 !important;
}
button[kind="primary"]:hover {
    background: #a93226 !important;
}

/* ── フォーム ── */
[data-testid="stForm"] {
    background: #ffffff;
    border-radius: 12px;
    padding: 1rem 1rem 0.5rem;
    box-shadow: 0 1px 6px rgba(0,0,0,0.07);
    border: none !important;
}

/* ── divider ── */
hr {
    border-color: #e8e4e0 !important;
    margin: 0.8rem 0 !important;
}

/* ── info / success / warning ── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    font-size: 0.9rem !important;
}

/* ── マラソンバナー ── */
.marathon-banner {
    background: linear-gradient(135deg, #c0392b 0%, #e74c3c 100%);
    color: white;
    border-radius: 12px;
    padding: 0.8rem 1.1rem;
    font-size: 0.95rem;
    font-weight: 600;
    margin-bottom: 1rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(192,57,43,0.25);
}

/* ── 在庫少ないカード ── */
.low-card {
    background: #fff8f7;
    border: 1px solid #f5c6c2;
    border-radius: 10px;
    padding: 0.55rem 0.8rem;
    margin-bottom: 0.4rem;
    font-size: 0.95rem;
}
.low-card-zero {
    background: #fdecea;
    border-color: #e9a19c;
    font-weight: 700;
}

/* ── 編集・削除ボタン ── */
.edit-btn button, .del-btn button {
    font-size: 0.78rem !important;
    padding: 0.2rem 0.4rem !important;
    border-radius: 7px !important;
}
</style>
""", unsafe_allow_html=True)

# ── タイトル ──
st.markdown('<div class="app-title">🏠 パントリー</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">日用品 在庫管理</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📦 在庫一覧", "⚠️ 在庫少ない", "✏️ 登録・編集"])


# ──────────────────────────────────────────────
# 画面①: 在庫一覧
# ──────────────────────────────────────────────
with tab1:
    items = db.get_all_items()

    if not items:
        st.info("アイテムが登録されていません。「登録・編集」タブから追加してください。")
    else:
        for category in CATEGORIES:
            cat_items = [i for i in items if i["category"] == category]
            if not cat_items:
                continue

            icon = CATEGORY_ICONS.get(category, "📁")
            st.markdown(f'<div class="cat-header">{icon} {category}</div>', unsafe_allow_html=True)

            for item in cat_items:
                qty = item["quantity"]
                is_low = item["is_low_stock_alert"]
                item_id = item["id"]
                name = item["name"]

                if qty == 0:
                    badge = '<span class="badge badge-zero">在庫切れ</span>'
                    name_cls = "item-zero"
                elif is_low:
                    badge = f'<span class="badge badge-low">残り {qty}</span>'
                    name_cls = "item-low"
                else:
                    badge = f'<span class="badge badge-ok">残り {qty}</span>'
                    name_cls = "item-name"

                col_label, col_minus, col_plus = st.columns([4, 1, 1])

                with col_label:
                    st.markdown(
                        f'<div class="item-card">'
                        f'<div><div class="{name_cls}" style="font-size:0.95rem;font-weight:600;">{name}</div>'
                        f'<div style="margin-top:3px;">{badge}</div></div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

                with col_minus:
                    st.write("")
                    if st.button("➖", key=f"minus_{item_id}", use_container_width=True):
                        db.update_quantity(item_id, max(0, qty - 1))
                        st.rerun()

                with col_plus:
                    st.write("")
                    if st.button("➕", key=f"plus_{item_id}", use_container_width=True):
                        db.update_quantity(item_id, qty + 1)
                        st.rerun()


# ──────────────────────────────────────────────
# 画面②: 在庫少ない一覧
# ──────────────────────────────────────────────
with tab2:
    settings = db.get_settings()
    start = settings.get("next_marathon_start")
    end = settings.get("next_marathon_end")

    if start and end:
        start_dt = date.fromisoformat(start)
        end_dt = date.fromisoformat(end)
        WEEKDAYS_JP = ["月", "火", "水", "木", "金", "土", "日"]
        start_wd = WEEKDAYS_JP[start_dt.weekday()]
        end_wd = WEEKDAYS_JP[end_dt.weekday()]
        marathon_label = (
            f"🛒 次回マラソン　"
            f"{start_dt.month}月{start_dt.day}日（{start_wd}）〜 "
            f"{end_dt.month}月{end_dt.day}日（{end_wd}）"
        )
        st.markdown(f'<div class="marathon-banner">{marathon_label}</div>', unsafe_allow_html=True)
    else:
        st.warning("次回マラソン日未設定")

    low_items = db.get_low_stock_items()

    if not low_items:
        st.success("✅ 在庫少ないアイテムはありません！")
    else:
        for category in CATEGORIES:
            cat_items = [i for i in low_items if i["category"] == category]
            if not cat_items:
                continue

            icon = CATEGORY_ICONS.get(category, "📁")
            st.markdown(f'<div class="cat-header">{icon} {category}</div>', unsafe_allow_html=True)

            for item in cat_items:
                qty = item["quantity"]
                name = item["name"]
                if qty == 0:
                    st.markdown(
                        f'<div class="low-card low-card-zero">🚨 {name}　<span style="color:#c0392b;">在庫切れ</span></div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f'<div class="low-card">⚠️ {name}　<span style="color:#e67e22;font-weight:600;">残り {qty}</span></div>',
                        unsafe_allow_html=True,
                    )


# ──────────────────────────────────────────────
# 画面③: 登録・編集
# ──────────────────────────────────────────────
with tab3:

    # ── 新規登録フォーム ──
    st.markdown('<div class="cat-header">➕ 新規登録</div>', unsafe_allow_html=True)

    with st.form("add_form", clear_on_submit=True):
        new_category = st.selectbox("カテゴリ", CATEGORIES, key="new_category")
        new_name = st.text_input("品目名", key="new_name")
        new_quantity = st.number_input("初期在庫数", min_value=0, value=0, step=1, key="new_quantity")
        new_alert = st.checkbox("在庫少ない一覧に表示", key="new_alert")
        submitted = st.form_submit_button("登録する", use_container_width=True, type="primary")

        if submitted:
            if not new_name.strip():
                st.error("品目名を入力してください。")
            else:
                db.add_item(new_category, new_name.strip(), new_quantity, new_alert)
                st.success(f"「{new_name.strip()}」を登録しました。")
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── アイテム一覧（編集・削除） ──
    st.markdown('<div class="cat-header">📝 アイテム編集・削除</div>', unsafe_allow_html=True)

    all_items = db.get_all_items()

    if not all_items:
        st.info("登録済みアイテムはありません。")
    else:
        if "editing_id" not in st.session_state:
            st.session_state.editing_id = None

        for item in all_items:
            item_id = item["id"]
            col_name, col_edit, col_del = st.columns([4, 1, 1])

            with col_name:
                icon = CATEGORY_ICONS.get(item["category"], "📁")
                st.markdown(
                    f'<div style="padding:0.45rem 0.2rem;font-size:0.9rem;">'
                    f'<span style="color:#9e9189;font-size:0.8rem;">{icon} {item["category"]}</span><br>'
                    f'<strong>{item["name"]}</strong>　在庫：{item["quantity"]}'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            with col_edit:
                st.write("")
                if st.button("編集", key=f"edit_{item_id}", use_container_width=True):
                    st.session_state.editing_id = item_id

            with col_del:
                st.write("")
                if st.button("削除", key=f"del_{item_id}", use_container_width=True):
                    db.delete_item(item_id)
                    if st.session_state.editing_id == item_id:
                        st.session_state.editing_id = None
                    st.rerun()

            if st.session_state.editing_id == item_id:
                with st.form(f"edit_form_{item_id}"):
                    st.markdown(f"**「{item['name']}」を編集**")
                    edit_category = st.selectbox(
                        "カテゴリ",
                        CATEGORIES,
                        index=CATEGORIES.index(item["category"]) if item["category"] in CATEGORIES else 0,
                    )
                    edit_name = st.text_input("品目名", value=item["name"])
                    edit_quantity = st.number_input("在庫数", min_value=0, value=item["quantity"], step=1)
                    edit_alert = st.checkbox("在庫少ない一覧に表示", value=item["is_low_stock_alert"])
                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        save = st.form_submit_button("保存", use_container_width=True, type="primary")
                    with col_cancel:
                        cancel = st.form_submit_button("キャンセル", use_container_width=True)

                    if save:
                        if not edit_name.strip():
                            st.error("品目名を入力してください。")
                        else:
                            db.update_item(item_id, edit_category, edit_name.strip(), edit_quantity, edit_alert)
                            st.session_state.editing_id = None
                            st.rerun()
                    if cancel:
                        st.session_state.editing_id = None
                        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── マラソン日設定 ──
    st.markdown('<div class="cat-header">🛒 マラソン日設定</div>', unsafe_allow_html=True)

    settings = db.get_settings()
    current_start = settings.get("next_marathon_start")
    current_end = settings.get("next_marathon_end")

    default_start = date.fromisoformat(current_start) if current_start else date.today()
    default_end = date.fromisoformat(current_end) if current_end else date.today()

    with st.form("marathon_form"):
        marathon_start = st.date_input("次回マラソン開始日", value=default_start)
        marathon_end = st.date_input("次回マラソン終了日", value=default_end)
        save_marathon = st.form_submit_button("保存する", use_container_width=True, type="primary")

        if save_marathon:
            if marathon_end < marathon_start:
                st.error("終了日は開始日以降を設定してください。")
            else:
                db.update_marathon_dates(marathon_start, marathon_end)
                st.success("マラソン日を保存しました。")
                st.rerun()
