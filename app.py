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
    page_title="pantry-app",
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
.block-container {
    padding-top: 0.6rem !important;
}

/* ── タイトル ── */
.app-title {
    text-align: center;
    font-size: 1.5rem;
    font-weight: 700;
    color: #3d3530;
    padding: 0 0 0.6rem;
    letter-spacing: 0.02em;
}

/* ── タブ：均等幅 ── */
[data-testid="stTabs"] [role="tablist"] {
    gap: 0 !important;
}
[data-testid="stTabs"] button {
    flex: 1 !important;
    text-align: center !important;
    font-size: 0.88rem !important;
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

/* ── アイテム行 ── */
.item-row {
    background: #ffffff;
    border-radius: 10px;
    padding: 0.55rem 0.8rem;
    margin-bottom: 0.3rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.07);
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.item-name       { font-size: 0.95rem; font-weight: 600; color: #3d3530; }
.item-name-low   { font-size: 0.95rem; font-weight: 600; color: #e67e22; }
.item-name-zero  { font-size: 0.95rem; font-weight: 700; color: #c0392b; }

/* ── 在庫バッジ ── */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 700;
    white-space: nowrap;
}
.badge-ok   { background: #eafaf1; color: #27ae60; }
.badge-low  { background: #fef9e7; color: #e67e22; }
.badge-zero { background: #fdecea; color: #c0392b; }

/* ── カラム：モバイルでも必ず横並び ── */
[data-testid="stHorizontalBlock"] {
    flex-wrap: nowrap !important;
    gap: 4px !important;
}
[data-testid="stColumn"] {
    min-width: 0 !important;
    overflow: hidden !important;
}

/* ── ボタン共通 ── */
button[kind="secondary"] {
    border-radius: 8px !important;
    font-size: 0.85rem !important;
    padding: 0.25rem 0.1rem !important;
    border: 1px solid #e0dbd7 !important;
    background: #faf9f7 !important;
    color: #3d3530 !important;
    width: 100% !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
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

/* ── 買い物マラソンバナー ── */
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

/* ── 購入リストカード ── */
.purchase-card {
    background: #ffffff;
    border-radius: 10px;
    padding: 0.55rem 0.8rem;
    margin-bottom: 0.3rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.07);
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.95rem;
    font-weight: 600;
    color: #3d3530;
}

hr {
    border-color: #e8e4e0 !important;
    margin: 0.8rem 0 !important;
}
[data-testid="stAlert"] {
    border-radius: 10px !important;
    font-size: 0.9rem !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="app-title">🏠pantry-app</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📦 在庫管理", "🛒 購入リスト", "✏️ 登録"])


# ──────────────────────────────────────────────
# タブ①: 在庫管理
# ──────────────────────────────────────────────
with tab1:
    items = db.get_all_items()

    if not items:
        st.info("アイテムが登録されていません。「登録」タブから追加してください。")
    else:
        for category in CATEGORIES:
            cat_items = [i for i in items if i["category"] == category]
            if not cat_items:
                continue

            icon = CATEGORY_ICONS.get(category, "📁")
            st.markdown(f'<div class="cat-header">{icon} {category}</div>', unsafe_allow_html=True)

            for item in cat_items:
                qty = item["quantity"]
                is_in_list = item.get("is_low_stock_alert", False)
                item_id = item["id"]
                name = item["name"]

                if qty == 0:
                    badge = '<span class="badge badge-zero">在庫切れ</span>'
                    name_cls = "item-name-zero"
                elif is_in_list:
                    badge = f'<span class="badge badge-low">残り {qty}</span>'
                    name_cls = "item-name-low"
                else:
                    badge = f'<span class="badge badge-ok">残り {qty}</span>'
                    name_cls = "item-name"

                # 1行目：名前 + バッジ
                st.markdown(
                    f'<div class="item-row">'
                    f'<span class="{name_cls}">{name}</span>'
                    f'{badge}'
                    f'</div>',
                    unsafe_allow_html=True,
                )

                # 2行目：3等分ボタン（モバイルでも横並び保証）
                col_plus, col_minus, col_buy = st.columns(3)

                with col_plus:
                    if st.button("➕", key=f"plus_{item_id}", use_container_width=True):
                        db.update_quantity(item_id, qty + 1)
                        st.rerun()

                with col_minus:
                    if st.button("➖", key=f"minus_{item_id}", use_container_width=True):
                        db.update_quantity(item_id, max(0, qty - 1))
                        st.rerun()

                with col_buy:
                    buy_label = "✅ 済" if is_in_list else "🛒 リスト"
                    if st.button(buy_label, key=f"buy_{item_id}", use_container_width=True):
                        db.toggle_purchase_list(item_id, not is_in_list)
                        st.rerun()

                st.markdown("<div style='margin-bottom:0.6rem'></div>", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# タブ②: 購入リスト
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
        st.markdown(
            f'<div class="marathon-banner">'
            f'🛒 次回の買い物マラソン<br>'
            f'{start_dt.month}月{start_dt.day}日（{start_wd}）〜{end_dt.month}月{end_dt.day}日（{end_wd}）'
            f'</div>',
            unsafe_allow_html=True,
        )
    else:
        st.warning("次回買い物マラソン日未設定")

    purchase_items = db.get_purchase_list_items()

    if not purchase_items:
        st.success("✅ 購入リストは空です！")
    else:
        for category in CATEGORIES:
            cat_items = [i for i in purchase_items if i["category"] == category]
            if not cat_items:
                continue

            icon = CATEGORY_ICONS.get(category, "📁")
            st.markdown(f'<div class="cat-header">{icon} {category}</div>', unsafe_allow_html=True)

            for item in cat_items:
                qty = item["quantity"]
                name = item["name"]
                item_id = item["id"]

                if qty == 0:
                    badge = '<span class="badge badge-zero">在庫切れ</span>'
                else:
                    badge = f'<span class="badge badge-low">残り {qty}</span>'

                st.markdown(
                    f'<div class="purchase-card">'
                    f'<span>{name}</span>'
                    f'{badge}'
                    f'</div>',
                    unsafe_allow_html=True,
                )


# ──────────────────────────────────────────────
# タブ③: 登録
# ──────────────────────────────────────────────
with tab3:

    # ── 新規登録フォーム ──
    st.markdown('<div class="cat-header">➕ 新規登録</div>', unsafe_allow_html=True)

    with st.form("add_form", clear_on_submit=True):
        new_category = st.selectbox("カテゴリ", CATEGORIES, key="new_category")
        new_name = st.text_input("品目名", key="new_name")
        new_quantity = st.number_input("初期在庫数", min_value=0, value=0, step=1, key="new_quantity")
        submitted = st.form_submit_button("登録する", use_container_width=True, type="primary")

        if submitted:
            if not new_name.strip():
                st.error("品目名を入力してください。")
            else:
                db.add_item(new_category, new_name.strip(), new_quantity)
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
            col_name, col_edit, col_del = st.columns([6, 1, 1])

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
                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        save = st.form_submit_button("保存", use_container_width=True, type="primary")
                    with col_cancel:
                        cancel = st.form_submit_button("キャンセル", use_container_width=True)

                    if save:
                        if not edit_name.strip():
                            st.error("品目名を入力してください。")
                        else:
                            db.update_item(item_id, edit_category, edit_name.strip(), edit_quantity)
                            st.session_state.editing_id = None
                            st.rerun()
                    if cancel:
                        st.session_state.editing_id = None
                        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── 買い物マラソン日設定 ──
    st.markdown('<div class="cat-header">🛒 買い物マラソン日設定</div>', unsafe_allow_html=True)

    settings = db.get_settings()
    current_start = settings.get("next_marathon_start")
    current_end = settings.get("next_marathon_end")

    default_start = date.fromisoformat(current_start) if current_start else date.today()
    default_end = date.fromisoformat(current_end) if current_end else date.today()

    with st.form("marathon_form"):
        marathon_start = st.date_input("買い物マラソン開始日", value=default_start)
        marathon_end = st.date_input("買い物マラソン終了日", value=default_end)
        save_marathon = st.form_submit_button("保存する", use_container_width=True, type="primary")

        if save_marathon:
            if marathon_end < marathon_start:
                st.error("終了日は開始日以降を設定してください。")
            else:
                db.update_marathon_dates(marathon_start, marathon_end)
                st.success("買い物マラソン日を保存しました。")
                st.rerun()
