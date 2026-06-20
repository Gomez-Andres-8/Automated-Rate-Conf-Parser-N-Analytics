import streamlit as st
from supabase import create_client, Client

# @st.cashe_resources
def get_supabase_client() -> Client:
	url = st.secrets["SUPABASE_URL"]
	key = st.secrets["SUPABASE_KEY"]

	return create_client(url, key)

def insert_load(load_data: dict) -> dict:
	supabase = get_supabase_client()

	response = (
		supabase
		.table("loads")
		.insert(load_data)
		.execute()
	)

	if not response_data:
		raise RuntimeError("Load was not saved to Supabase.")

	return response.data[0]