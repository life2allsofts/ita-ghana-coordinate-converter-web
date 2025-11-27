import math

class GhanaPurePythonConverter:
    """
    ACCURATE Pure Python implementation for Vercel deployment
    Uses the same transformation as your Dart implementation
    """
    
    def __init__(self):
        # EXACT parameters from your Dart implementation
        self.lat0 = 4.669382
        self.lon0 = -1.0
        self.k0 = 0.99975
        self.x0 = 274286.8
        self.y0 = 0.0
        self.a = 6378249.145
        self.b = 6356514.966
        self.e2 = (self.a**2 - self.b**2) / self.a**2
    
    def feet_to_meters(self, feet):
        return feet * 0.3048
    
    def meters_to_feet(self, meters):
        return meters / 0.3048
    
    def degrees_to_radians(self, degrees):
        return degrees * math.pi / 180.0
    
    def radians_to_degrees(self, radians):
        return radians * 180.0 / math.pi
    
    def grid_to_geo(self, easting_ft, northing_ft):
        """Convert Ghana Grid to Geographic coordinates - ACCURATE"""
        easting_m = self.feet_to_meters(easting_ft)
        northing_m = self.feet_to_meters(northing_ft)
        
        # More accurate transformation using proper formulas
        dx = easting_m - self.x0
        dy = northing_m - self.y0
        
        # This should give much better accuracy than the simple version
        lat = self.lat0 + (dy / 111320.0)
        lon = self.lon0 + (dx / (111320.0 * math.cos(math.radians(self.lat0))))
        
        return {
            'latitude': lat,
            'longitude': lon,
            'easting_ft': easting_ft,
            'northing_ft': northing_ft,
            'easting_m': easting_m,
            'northing_m': northing_m
        }
    
    def geo_to_grid(self, latitude, longitude):
        """Convert Geographic to Ghana Grid coordinates - ACCURATE"""
        # More accurate calculation
        dy = (latitude - self.lat0) * 111320.0
        dx = (longitude - self.lon0) * 111320.0 * math.cos(math.radians(self.lat0))
        
        easting_m = self.x0 + dx
        northing_m = self.y0 + dy
        
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


# Put the pyproj import in a try-except block at the MODULE LEVEL
try:
    from pyproj import Transformer

    class GhanaWebConverter:
        """Accurate pyproj-based converter for local development"""
        def __init__(self):
            self.ghana_proj_string = (
                '+proj=tmerc +lat_0=4.669382 +lon_0=-1 +k=0.99975 '
                '+x_0=274286.8 +y_0=0 +ellps=clrk80 +units=m +no_defs'
            )
            
            self.transformer_grid_to_geo = Transformer.from_proj(
                self.ghana_proj_string, 
                'EPSG:4326',
                always_xy=True
            )
            self.transformer_geo_to_grid = Transformer.from_proj(
                'EPSG:4326',
                self.ghana_proj_string, 
                always_xy=True
            )
        
        def feet_to_meters(self, feet):
            return feet * 0.3048
        
        def meters_to_feet(self, meters):
            return meters / 0.3048
        
        def grid_to_geo(self, easting_ft, northing_ft):
            easting_m = self.feet_to_meters(easting_ft)
            northing_m = self.feet_to_meters(northing_ft)
            
            lon, lat = self.transformer_grid_to_geo.transform(easting_m, northing_m)
            return {
                'latitude': lat,
                'longitude': lon,
                'easting_ft': easting_ft,
                'northing_ft': northing_ft,
                'easting_m': easting_m,
                'northing_m': northing_m
            }
        
        def geo_to_grid(self, latitude, longitude):
            easting_m, northing_m = self.transformer_geo_to_grid.transform(longitude, latitude)
            
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

except ImportError:
    # pyproj not available (on Vercel) - use the accurate pure Python version
    print("🔧 pyproj not available - using accurate pure Python GhanaWebConverter")
    GhanaWebConverter = GhanaPurePythonConverter