def get_temp_input_data_reqs():
    temporal_input_data_req = [
    {"name": "Albedo",
    "unit": "[-]",
    "quantity": "Albedo",
    "level": "surface",
    "time": "instanteneous",
    "filepath": "{input_folder}/{year}{month}{day}/ALBEDO_{year}{month}{day}.tif"},

    {"name": "Land Surface Temperature",
    "unit": "[K]",
    "quantity": "Temperature",
    "level": "surface",
    "time": "instanteneous",
    "filepath": "{input_folder}/{year}{month}{day}/LST_{year}{month}{day}.tif"},

    {"name": "Normalized Difference Vegetation Index",
    "unit": "[-]",
    "quantity": "Normalized Difference Vegetation Index",
    "level": "surface",
    "time": "instanteneous",
    "filepath": "{input_folder}/{year}{month}{day}/NDVI_{year}{month}{day}.tif"},

    {"name": "Air Pressure at sea level (daily average)",
    "unit": "[kPa]",
    "quantity": "Air Pressure",
    "level": "sea",
    "time": "daily average",
    "filepath": "{input_folder}/{year}{month}{day}/Pair_24_0_{year}{month}{day}.tif"},

    {"name": "Air Pressure at sea level (instanteneous)", 
    "unit": "[kPa]",
    "quantity": "Air Pressure",
    "level": "sea",
    "time": "instanteneous",
    "filepath": "{input_folder}/{year}{month}{day}/Pair_inst_0_{year}{month}{day}.tif"},

    {"name": "Air Pressure at surface level (instanteneous)",
    "unit": "[kPa]",
    "quantity": "Air Pressure",
    "level": "surface",
    "time": "instanteneous",
    "filepath": "{input_folder}/{year}{month}{day}/Pair_inst_{year}{month}{day}.tif"},

    {"name": "Precipitation",
    "unit": "[mm/day]",
    "quantity": "Precipitation",
    "level": "surface",
    "time": "instanteneous",
    "filepath": "{input_folder}/{year}{month}{day}/Precipitation_{year}{month}{day}.tif"},

    {"name": "Specific Humidity (daily average)", 
    "unit": "[kg/kg]",
    "quantity": "Specific Humidity",
    "level": "surface",
    "time": "daily average",
    "filepath": "{input_folder}/{year}{month}{day}/qv_24_{year}{month}{day}.tif"},

    {"name": "Specific Humidity (instanteneous)", "unit": "[kg/kg]",
    "quantity": "Specific Humidity",
    "level": "surface",
    "time": "instanteneous",
    "filepath": "{input_folder}/{year}{month}{day}/qv_inst_{year}{month}{day}.tif"},

    {"name": "Air Temperature (daily average)", "unit": "[K]",
    "quantity": "Temperature",
    "level": "surface",
    "time": "daily average",
    "filepath": "{input_folder}/{year}{month}{day}/tair_24_{year}{month}{day}.tif"},

    {"name": "Air Temperature (instanteneous)", "unit": "[K]",
    "quantity": "Temperature",
    "level": "surface",
    "time": "instanteneous",
    "filepath": "{input_folder}/{year}{month}{day}/tair_inst_{year}{month}{day}.tif"},

    {"name": "Air Temperature (daily maximum)", "unit": "[K]",
    "quantity": "Temperature",
    "level": "surface",
    "time": "daily maximum",
    "filepath": "{input_folder}/{year}{month}{day}/tair_max_24_{year}{month}{day}.tif"},

    {"name": "Air Temperature (daily minimum)", "unit": "[K]",
    "quantity": "Temperature",
    "level": "surface",
    "time": "daily minimum",
    "filepath": "{input_folder}/{year}{month}{day}/tair_min_24_{year}{month}{day}.tif"},

    {"name": "Transmissivity", "unit": "[-]",
    "quantity": "Transmissivity",
    "level": "column",
    "time": "daily average",
    "filepath": "{input_folder}/{year}{month}{day}/Trans_24_{year}{month}{day}.tif"},

    {"name": "Windspeed (daily average)", "unit": "[m/s]",
    "quantity": "Windspeed",
    "level": "surface",
    "time": "daily average",
    "filepath": "{input_folder}/{year}{month}{day}/wind_24_{year}{month}{day}.tif"},

    {"name": "Windspeed (instanteneous)", "unit": "[m/s]",
    "quantity": "Windspeed",
    "level": "surface",
    "time": "instanteneous",
    "filepath": "{input_folder}/{year}{month}{day}/wind_inst_{year}{month}{day}.tif"},

    {"name": "Total Precipitable Water Vapout", "unit": "[mm]",
    "quantity": "Total Precipitable Water Vapour",
    "level": "column",
    "time": "instanteneous",
    "filepath": "{input_folder}/{year}{month}{day}/wv_inst_{year}{month}{day}.tif"},

    {"name": "Instantaneous Data Time", "unit": "[hour]",
    "quantity": "Time",
    "level": "surface",
    "time": "instanteneous",
    "filepath": "{input_folder}/{year}{month}{day}/Time_{year}{month}{day}.tif"},
    ]

    return temporal_input_data_req

test = "{input_folder}/{year}{month}{day}/Time_{year}{month}{day}.tif"
test2 = "{input_folder}/{year}{month}{day}/Time_{year}{month}{day}.tif"
