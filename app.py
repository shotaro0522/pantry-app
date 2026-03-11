import streamlit as st
from datetime import date
import db

CATEGORIES = ["キッチン", "お風呂", "洗面所", "トイレ"]

st.set_page_config(
    page_title="パントリー",
    page_icon="🏠",
    layout="centered",
)

st.title("🏠 パントリー")

tab1, tab2, tab3 = st.tabs(["📦 在庫一覧", "⚠️ 在庫少ない", "✏️ 登録・編集"])


# ──────────────────────────────────────────────
# 画面①: 在庫一覧
# ──────────────────────────────────────────────
with tab1:
    st.header("在庫一覧")

    items = db.get_all_items()

    if not items:
        st.info("アイテムが登録されていません。「登録・編集」タブから追加してください。")
    else:
        for category in CATEGORIES:
            cat_items = [i for i in items if i["category"] == category]
            if not cat_items:
                continue

            st.subheader(f"📁 {category}")

            for item in cat_items:
                qty = item["quantity"]
                is_low = item["is_low_stock_alert"]
                item_id = item["id"]
                name = item["name"]

                # 在庫状態に応じた表示
                if qty == 0:
                    label = f"🚨 **{name}**　在庫：**0**"
                elif is_low:
                    label = f"⚠️ {name}　在庫：{qty}"
                else:
                    label = f"{name}　在庫：{qty}"

                col_label, col_minus, col_plus = st.columns([3, 1, 1])

                with col_label:
                    if qty == 0:
                        st.markdown(
                            f"<span style='color:red; font-weight:bold;'>{label}</span>",
                            unsafe_allow_html=True,
                        )
                    elif is_low:
                        st.markdown(
                            f"<span style='color:orange;'>{label}</span>",
                            unsafe_allow_html=True,
                        )
                    else:
                        st.write(label)

                with col_minus:
                    if st.button("➖", key=f"minus_{item_id}", use_container_width=True):
                        new_qty = max(0, qty - 1)
                        db.update_quantity(item_id, new_qty)
                        st.rerun()

                with col_plus:
                    if st.button("➕", key=f"plus_{item_id}", use_container_width=True):
                        db.update_quantity(item_id, qty + 1)
                        st.rerun()

            st.divider()


# ──────────────────────────────────────────────
# 画面②: 在庫少ない一覧
# ──────────────────────────────────────────────
with tab2:
    st.header("在庫少ない一覧")

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
            f"🛒 次回マラソン：{start_dt.month}月{start_dt.day}日（{start_wd}）"
            f"〜 {end_dt.month}月{end_dt.day}日（{end_wd}）"
        )
        st.info(marathon_label)
    else:
        st.warning("次回マラソン日未設定")

    low_items = db.get_low_stock_items()

    if not low_items:
        st.success("在庫少ないアイテムはありません！")
    else:
        for category in CATEGORIES:
            cat_items = [i for i in low_items if i["category"] == category]
            if not cat_items:
                continue

            st.subheader(f"📁 {category}")
            for item in cat_items:
                qty = item["quantity"]
                name = item["name"]
                if qty == 0:
                    st.markdown(
                        f"<span style='color:red; font-weight:bold;'>🚨 {name}　在庫：0</span>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"<span style='color:orange;'>⚠️ {name}　在庫：{qty}</span>",
                        unsafe_allow_html=True,
                    )
            st.divider()


# ──────────────────────────────────────────────
# 画面③: 登録・編集
# ──────────────────────────────────────────────
with tab3:
    st.header("登録・編集")

    # ── 新規登録フォーム ──
    st.subheader("➕ 新規登録")

    with st.form("add_form", clear_on_submit=True):
        new_category = st.selectbox("カテゴリ", CATEGORIES, key="new_category")
        new_name = st.text_input("品目名", key="new_name")
        new_quantity = st.number_input("初期在庫数", min_value=0, value=0, step=1, key="new_quantity")
        new_alert = st.checkbox("在庫少ない一覧に表示", key="new_alert")
        submitted = st.form_submit_button("登録", use_container_width=True)

        if submitted:
            if not new_name.strip():
                st.error("品目名を入力してください。")
            else:
                db.add_item(new_category, new_name.strip(), new_quantity, new_alert)
                st.success(f"「{new_name.strip()}」を登録しました。")
                st.rerun()

    st.divider()

    # ── アイテム一覧（編集・削除） ──
    st.subheader("📝 アイテム編集・削除")

    all_items = db.get_all_items()

    if not all_items:
        st.info("登録済みアイテムはありません。")
    else:
        # 編集対象をセッションで管理
        if "editing_id" not in st.session_state:
            st.session_state.editing_id = None

        for item in all_items:
            item_id = item["id"]
            col_name, col_edit, col_del = st.columns([4, 1, 1])

            with col_name:
                st.write(f"**{item['category']}** / {item['name']}　在庫:{item['quantity']}")

            with col_edit:
                if st.button("編集", key=f"edit_{item_id}", use_container_width=True):
                    st.session_state.editing_id = item_id

            with col_del:
                if st.button("削除", key=f"del_{item_id}", use_container_width=True):
                    db.delete_item(item_id)
                    if st.session_state.editing_id == item_id:
                        st.session_state.editing_id = None
                    st.rerun()

            # 編集フォームをインライン展開
            if st.session_state.editing_id == item_id:
                with st.form(f"edit_form_{item_id}"):
                    st.markdown(f"**「{item['name']}」を編集**")
                    edit_category = st.selectbox(
                        "カテゴリ",
                        CATEGORIES,
                        index=CATEGORIES.index(item["category"]) if item["category"] in CATEGORIES else 0,
                    )
                    edit_name = st.text_input("品目名", value=item["name"])
                    edit_quantity = st.number_input(
                        "在庫数", min_value=0, value=item["quantity"], step=1
                    )
                    edit_alert = st.checkbox(
                        "在庫少ない一覧に表示", value=item["is_low_stock_alert"]
                    )
                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        save = st.form_submit_button("保存", use_container_width=True)
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

        st.divider()

    # ── マラソン日設定 ──
    st.subheader("🛒 マラソン日設定")

    settings = db.get_settings()
    current_start = settings.get("next_marathon_start")
    current_end = settings.get("next_marathon_end")

    default_start = date.fromisoformat(current_start) if current_start else date.today()
    default_end = date.fromisoformat(current_end) if current_end else date.today()

    with st.form("marathon_form"):
        marathon_start = st.date_input("次回マラソン開始日", value=default_start)
        marathon_end = st.date_input("次回マラソン終了日", value=default_end)
        save_marathon = st.form_submit_button("保存", use_container_width=True)

        if save_marathon:
            if marathon_end < marathon_start:
                st.error("終了日は開始日以降を設定してください。")
            else:
                db.update_marathon_dates(marathon_start, marathon_end)
                st.success("マラソン日を保存しました。")
                st.rerun()
