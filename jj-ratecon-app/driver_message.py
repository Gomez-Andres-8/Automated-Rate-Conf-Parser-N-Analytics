def generate_driver_message(load: dict) -> str:
    driver_name = load.get("driver_name") or "N/A"
    truck_number = load.get("truck_number") or "N/A"
    trailer_number = load.get("trailer_number") or "N/A"
    
    broker_name = load.get("broker_name") or "N/A"
    broker_load_number = load.get("broker_load_number") or "N/A"
    
    pickup_name = load.get("pickup_name") or "N/A"
    pickup_address = load.get("pickup_address") or "N/A"
    pickup_city = load.get("pickup_city") or "City"
    pickup_state = load.get("pickup_state") or "State"
    pickup_zip = load.get("pickup_zip") or "00000"
    pickup_date = load.get("pickup_date") or "01 JAN 1900"
    pickup_time = load.get("pickup_time") or "##:##"

    delivery_name = load.get("delivery_name") or "N/A"
    delivery_address = load.get("delivery_address") or "N/A"
    delivery_city = load.get("delivery_city") or "City"
    delivery_state = load.get("delivery_state") or "State"
    delivery_zip = load.get("delivery_zip") or "00000"
    delivery_date = load.get("delivery_date") or "01 JAN 1900"
    delivery_time = load.get("delivery_time") or "##:##"

    commodity = load.get("commodity") or "N/A"
    weight_lbs = load.get("weight_lbs") or "N/A"

    return f"""Load Info

Driver: {driver_name}
Truck: {truck_number}
Trailer: {trailer_number}

Broker: {broker_name}
Load #: {broker_load_number}

Pickup:
    {pickup_name}
    {pickup_address}
    {pickup_city}, {pickup_state} {pickup_zip}
    {pickup_date} at {pickup_time}
    
Delivery:
    {delivery_name}
    {delivery_address}
    {delivery_city}, {delivery_state} {delivery_zip}
    {delivery_date} at {delivery_time}

Commodity: {commodity}
Weight: {weight_lbs} lbs

Instructions:
    Por favor confirmar una vez cargado y enviar BOL cuando esté disponible.

    """


