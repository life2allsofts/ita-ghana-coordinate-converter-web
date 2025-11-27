import math

class GhanaPurePythonConverter:
    """
    Pure Python implementation of Ghana coordinate conversion
    No external dependencies - works on Vercel
    """
    
    def __init__(self):
        # Ghana projection parameters (from our Dart implementation)
        self.lat0 = 4.669382  # latitude of origin
        self.lon0 = -1.0      # central meridian  
        self.k0 = 0.99975     # scale factor
        self.x0 = 274286.8    # false easting (meters)
        self.y0 = 0.0         # false northing
        self.a = 6378249.145  # Clarke 1880 ellipsoid (meters)
        self.b = 6356514.966  # Clarke 1880 ellipsoid (meters)
        self.e2 = (self.a**2 - self.b**2) / self.a**2  # eccentricity squared
    
    def feet_to_meters(self, feet):
        return feet * 0.3048
    
    def meters_to_feet(self, meters):
        return meters / 0.3048
    
    def grid_to_geo(self, easting_ft, northing_ft):
        """Convert Ghana Grid to Geographic coordinates (simplified)"""
        easting_m = self.feet_to_meters(easting_ft)
        northing_m = self.feet_to_meters(northing_ft)
        
        # Simplified transformation (for demo - use exact params from your Dart code)
        # In production, you'd implement the full PROJ4 transformation
        lat = self.lat0 + (northing_m - self.y0) / 111320.0
        lon = self.lon0 + (easting_m - self.x0) / (111320.0 * math.cos(math.radians(self.lat0)))
        
        return {
            'latitude': lat,
            'longitude': lon,
            'easting_ft': easting_ft,
            'northing_ft': northing_ft,
            'easting_m': easting_m,
            'northing_m': northing_m
        }
    
    def geo_to_grid(self, latitude, longitude):
        """Convert Geographic to Ghana Grid coordinates (simplified)"""
        # Simplified transformation (for demo - use exact params from your Dart code)
        easting_m = self.x0 + (longitude - self.lon0) * 111320.0 * math.cos(math.radians(self.lat0))
        northing_m = self.y0 + (latitude - self.lat0) * 111320.0
        
        easting_ft = self.meters_to_feet(easting_m)
        northing_ft = self.meters_to_feet(northing_m)
        
        return {
            'easting_ft': easting_ft,
            'northing_ft': northing_ft,
            'easting_m': easting_m,
            'northing_m': northing_m,
            'latitude': latitude,
            'longitude': longitude
        }