import tempfile
from datetime import date, time

from pathlib import Path
import streamlit as st
from st_copy_button import st_copy_button

import extract_text
from supabase_client import insert_load
from driver_message import generate_driver_message

st.set_page_config(
	page_title = "JJ Transport Rate Confirmation Parser",
	page_icon = "COMPANY_LOGO",
	layout = "wide"
)


st.title("JJ Transport Rate Confirmation Parser")

uploaded_file = st.file_uploader(
	"Upload a rate confirmation PDF",
	type = ["pdf"]
)

if uploaded_file is not None:
	pdf_bytes = uploaded_file.getvalue()
	
	st.write(f"Uploaded file size: {len(pdf_bytes)} bytes") # Debug checker

	if not pdf_bytes.startswith(b"%PDF"):
		st.error("Uploaded file is not a valid PDF.")
		st.stop()

	with tempfile.NamedTemporaryFile(delete = False, suffix = ".pdf") as tmp:
		tmp.write(pdf_bytes)
		tmp_path = tmp.name

	with st.spinner("Extracting and parsing rate confirmation..."):

		parsed_result =  extract_text.extract_and_parse_pdf(tmp_path)

		extracted = parsed_result.get("fields", {})
		raw_text = parsed_result.get("raw_text", "")
		extraction_method = parsed_result.get("extraction_method", "unknown")

		st.success(f"PDF extracted successfully using: {extraction_method}")

		with st.expander("View raw extracted text"):
			st.text_area("Raw text", raw_text, height = 300)

		# Need to figure out how to properly get fields
		st.subheader("Review Load Details")

		col1, col2 = st.columns(2)

		with col1:
			broker_name = st.text_input(
				"Broker Name",
				value = extracted.get("broker_name", "")
			)

			broker_load_number = st.text_input(
				"Broker Load Number",
				value = extracted.get("broker_load_number", "")
			)

			rate_total = st.number_input(
				"Rate Total",
				min_value = 0.0,
				# value = float(extracted.get("rate_total", 0.0)),
				value = extracted.get("rate_total", 0.0),
				step = 50.0
			)

			miles = st.number_input(
				"Miles",
				min_value = 0.0,
				# value = float(extracted.get("miles", 0.0)),
				value = extracted.get("miles", 0.0),
				step = 10.0
			)

			commodity = st.text_input(
				"Commodity",
				value = extracted.get("commodity", "")
			)

			weight_lbs = st.number_input(
				"Weight (lbs)",
				min_value = 0.0,
				# value = float(extracted.get("weight_lbs", 0.0)),
				value = extracted.get("weight_lbs", 0.0),
				step = 10.0
			)

		with col2:
			driver_name = st.text_input("Driver Name")
			truck_number = st.text_input("Truck Number")
			trailer_number = st.text_input("Trailer Number")
			trailer_type = st.text_input(
				"Trailer Type",
				value = extracted.get("trailer_type", "")
				)
		
		st.divider()

		st.subheader("Pickup")

		pcol1, pcol2 = st.columns(2) # p for pickup

		with pcol1:
			pickup_name = st.text_input(
				"Pickup Name",
				value = extracted.get("pickup_name", "")
			)

			pickup_address = st.text_input(
				"Pickup Address",
				value = extracted.get("pickup_address", "")
			)

			pickup_city = st.text_input(
				"Pickup City",
				value = extracted.get("pickup_city", "")
			)

		with pcol2:
			pickup_state = st.text_input(
				"Pickup State",
				value = extracted.get("pickup_state", "")
			)

			pickup_zip = st.text_input(
				"Pickup ZIP",
				value = extracted.get("pickup_zip", "")
			)

			pickup_date = st.text_input(
				"Pickup Date",
				value = extracted.get("pickup_date", "")
			)

			pickup_time = st.text_input(
				"Pickup Time",
				value = extracted.get("pickup_time", "")
			)

		st.subheader("Delivery")

		dcol1, dcol2 = st.columns(2) # d for delivery

		with dcol1:
			delivery_name = st.text_input(
				"Delivery Name",
				value = extracted.get("delivery_name", "")
			)

			delivery_address = st.text_input(
				"Delivery Address",
				value = extracted.get("delivery_address", "")
			)

			delivery_city = st.text_input(
				"Delivery City",
				value = extracted.get("delivery_city", "")
			)

		with dcol2:
			delivery_state = st.text_input(
				"Delivery State",
				value = extracted.get("delivery_state", "")
			)

			delivery_zip = st.text_input(
				"Delivery ZIP",
				value = extracted.get("delivery_zip", "")
			)

			delivery_date = st.text_input(
				"Delivery Date",
				value = extracted.get("delivery_date", "")
			)

			delivery_time = st.text_input(
				"Delivery Time",
				value = extracted.get("delivery_time", "")
			)
		
		rate_per_mile = None
		if miles > 0:
			rate_per_mile = round(rate_total / miles, 2)
		
		load_data = {
			"broker_name": broker_name,
			"broker_load_number": broker_load_number,
			"rate_total": rate_total,
			"miles": miles,
			"rate_per_mile": rate_per_mile,

			"pickup_name": pickup_name,
			"pickup_address": pickup_address,
			"pickup_city": pickup_city,
			"pickup_state": pickup_state,
			"pickup_zip": pickup_zip,
			"pickup_date": pickup_date,
			"pickup_time": pickup_time,

			"delivery_name": delivery_name,
			"delivery_address": delivery_address,
			"delivery_city": delivery_city,
			"delivery_state": delivery_state,
			"delivery_zip": delivery_zip,
			"delivery_date": delivery_date,
			"delivery_time": delivery_time,

			"commodity": commodity,
			"weight_lbs": weight_lbs,
			"trailer_type": trailer_type,

			"driver_name": driver_name,
			"truck_number": truck_number,
			"trailer_number": trailer_number,

			"extraction_method": extraction_method,
			"raw_text": raw_text,
			"parser_status" : "reviewed"
		}

		driver_message = generate_driver_message(load_data)
		load_data["driver_message"] = driver_message

		st.subheader("Driver Message Review")
		copyable_text = st.text_area("Copyable Driver Message", driver_message, height = 575)
		# copy_button(copyable_text)
		
		st_copy_button(
			copyable_text,
			before_copy_label = "Copy Message For Driver",
			after_copy_label = "Copied! Make Sure to Save to Database"
		)

		# st.text_area("Copyable Driver Message", driver_message, height = 650)

		if st.button("Save Load To Database"):
			# Here you might want to save the load_data to a database or a file
			try:
				saved_load = insert_load(load_data)
				st.success(f"Load saved successfully. Internal ID: {saved_load['id']}")
			except Exception as e:
				st.error(f"Could not save load: {e}")
			


