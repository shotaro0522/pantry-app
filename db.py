from supabase import create_client
import streamlit as st


def get_client():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)


def get_all_items() -> list[dict]:
    client = get_client()
    response = client.table("items").select("*").order("category").order("name").execute()
    return response.data


def get_low_stock_items() -> list[dict]:
    client = get_client()
    response = (
        client.table("items")
        .select("*")
        .eq("is_low_stock_alert", True)
        .order("category")
        .order("name")
        .execute()
    )
    return response.data


def add_item(category: str, name: str, quantity: int, is_low_stock_alert: bool) -> None:
    client = get_client()
    # quantity <= 1 の場合は自動でアラートON
    if quantity <= 1:
        is_low_stock_alert = True
    client.table("items").insert(
        {
            "category": category,
            "name": name,
            "quantity": quantity,
            "is_low_stock_alert": is_low_stock_alert,
        }
    ).execute()


def update_quantity(item_id: int, new_quantity: int) -> None:
    client = get_client()
    # quantity <= 1 の場合は is_low_stock_alert を自動でTrue
    is_low_stock_alert = new_quantity <= 1
    client.table("items").update(
        {"quantity": new_quantity, "is_low_stock_alert": is_low_stock_alert}
    ).eq("id", item_id).execute()


def update_item(
    item_id: int,
    category: str,
    name: str,
    quantity: int,
    is_low_stock_alert: bool,
) -> None:
    client = get_client()
    # quantity <= 1 の場合は is_low_stock_alert を強制True
    if quantity <= 1:
        is_low_stock_alert = True
    client.table("items").update(
        {
            "category": category,
            "name": name,
            "quantity": quantity,
            "is_low_stock_alert": is_low_stock_alert,
        }
    ).eq("id", item_id).execute()


def delete_item(item_id: int) -> None:
    client = get_client()
    client.table("items").delete().eq("id", item_id).execute()


def get_settings() -> dict:
    client = get_client()
    response = client.table("settings").select("*").eq("id", 1).execute()
    if response.data:
        return response.data[0]
    return {}


def update_marathon_dates(start_date, end_date) -> None:
    client = get_client()
    client.table("settings").update(
        {
            "next_marathon_start": start_date.isoformat() if start_date else None,
            "next_marathon_end": end_date.isoformat() if end_date else None,
        }
    ).eq("id", 1).execute()
