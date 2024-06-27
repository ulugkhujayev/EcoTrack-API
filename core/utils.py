def normalize_data(source, data):
    if source == "openaq":
        return {
            "value": data["value"],
            "unit": data["unit"],
        }
    elif source == "openweathermap":
        if data["name"] == "temperature":
            return {
                "value": data["value"],
                "unit": "°C",
            }
        elif data["name"] == "humidity":
            return {
                "value": data["value"],
                "unit": "%",
            }
        elif data["name"] == "pressure":
            return {
                "value": data["value"],
                "unit": "hPa",
            }
    return data
