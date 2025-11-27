import re

def dms_to_decimal(dms_string):
    """Convert DMS string to decimal degrees"""
    # Handle formats like: "5° 35' 18.09\" N" or "5 35 18.09 N"
    dms_string = dms_string.strip().upper()
    
    # Regex to parse DMS components
    pattern = r'([NSWE]?)\s*([-]?\d+)[°\s]?\s*(\d+)[\'\s]?\s*([\d.]+)[\"\s]?\s*([NSWE]?)'
    match = re.match(pattern, dms_string)
    
    if not match:
        raise ValueError(f"Invalid DMS format: {dms_string}")
    
    hemisphere1 = match.group(1) or ''
    degrees = int(match.group(2))
    minutes = int(match.group(3))
    seconds = float(match.group(4))
    hemisphere2 = match.group(5) or ''
    
    hemisphere = hemisphere1 or hemisphere2
    
    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    
    if hemisphere in ['S', 'W']:
        decimal = -decimal
    
    return decimal

def decimal_to_dms(decimal, is_latitude=True):
    """Convert decimal degrees to DMS string"""
    abs_decimal = abs(decimal)
    degrees = int(abs_decimal)
    minutes_decimal = (abs_decimal - degrees) * 60
    minutes = int(minutes_decimal)
    seconds = (minutes_decimal - minutes) * 60
    
    hemisphere = 'N' if decimal >= 0 else 'S' if is_latitude else 'E' if decimal >= 0 else 'W'
    
    return f"{degrees}° {minutes}' {seconds:.2f}\" {hemisphere}"

def is_valid_ghana_latitude(lat):
    return 4.0 <= lat <= 11.5

def is_valid_ghana_longitude(lon):
    return -3.5 <= lon <= 1.5