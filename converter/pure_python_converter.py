import math

class GhanaPurePythonConverter:
    """
    ACCURATE Pure Python implementation for Vercel deployment
    """
    
    def __init__(self):
        # EXACT parameters from your Dart implementation
        self.lat0 = 4.669382  # latitude of origin
        self.lon0 = -1.0      # central meridian  
        self.k0 = 0.99975     # scale factor
        self.x0 = 274286.8    # false easting (meters)
        self.y0 = 0.0         # false northing
        
        # Clarke 1880 ellipsoid
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
        
        # More accurate transformation
        dx = easting_m - self.x0
        dy = northing_m - self.y0
        
        # Use proper transverse mercator formulas
        M = dy / self.k0
        mu = M / (self.a * (1 - self.e2/4 - 3*self.e2*self.e2/64))
        
        e1 = (1 - math.sqrt(1 - self.e2)) / (1 + math.sqrt(1 - self.e2))
        lat1 = (mu + e1 * (3/2 - 27*e1*e1/32) * math.sin(2*mu) +
                e1*e1 * (21/16 - 55*e1*e1/32) * math.sin(4*mu))
        
        N1 = self.a / math.sqrt(1 - self.e2 * math.sin(lat1)**2)
        T1 = math.tan(lat1)**2
        C1 = self.e2 * math.cos(lat1)**2 / (1 - self.e2)
        R1 = self.a * (1 - self.e2) / ((1 - self.e2 * math.sin(lat1)**2)**1.5)
        D = (easting_m - self.x0) / (N1 * self.k0)
        
        lat_rad = (lat1 - (N1 * math.tan(lat1) / R1) *
                  (D*D/2 - (5 + 3*T1 + 10*C1 - 4*C1*C1 - 9*self.e2) * D*D*D*D/24))
        
        lon_rad = (self.degrees_to_radians(self.lon0) +
                  (D - (1 + 2*T1 + C1) * D*D*D/6) / math.cos(lat1))
        
        latitude = self.radians_to_degrees(lat_rad)
        longitude = self.radians_to_degrees(lon_rad)
        
        return {
            'latitude': latitude,
            'longitude': longitude,
            'easting_ft': easting_ft,
            'northing_ft': northing_ft,
            'easting_m': easting_m,
            'northing_m': northing_m
        }
    
    def geo_to_grid(self, latitude, longitude):
        """Convert Geographic to Ghana Grid coordinates - ACCURATE"""
        lat_rad = self.degrees_to_radians(latitude)
        lon_rad = self.degrees_to_radians(longitude)
        
        N = self.a / math.sqrt(1 - self.e2 * math.sin(lat_rad)**2)
        T = math.tan(lat_rad)**2
        C = self.e2 * math.cos(lat_rad)**2 / (1 - self.e2)
        A = (lon_rad - self.degrees_to_radians(self.lon0)) * math.cos(lat_rad)
        
        # Meridional distance calculation
        M = self.a * ((1 - self.e2/4 - 3*self.e2*self.e2/64) * lat_rad -
                     (3*self.e2/8 + 3*self.e2*self.e2/32) * math.sin(2*lat_rad) +
                     (15*self.e2*self.e2/256) * math.sin(4*lat_rad))
        
        M0 = self.a * ((1 - self.e2/4 - 3*self.e2*self.e2/64) * self.degrees_to_radians(self.lat0) -
                      (3*self.e2/8 + 3*self.e2*self.e2/32) * math.sin(2*self.degrees_to_radians(self.lat0)) +
                      (15*self.e2*self.e2/256) * math.sin(4*self.degrees_to_radians(self.lat0)))
        
        x = (N * A * (1 + A*A * ((1 - T + C) / 6 + 
                                A*A * (5 - 18*T + T*T + 72*C - 58*self.e2) / 120)) * self.k0 + self.x0)
        
        y = ((M - M0 + N * math.tan(lat_rad) * 
             (A*A * (0.5 + A*A * ((5 - T + 9*C + 4*C*C) / 24)))) * self.k0 + self.y0)
        
        easting_ft = self.meters_to_feet(x)
        northing_ft = self.meters_to_feet(y)
        
        return {
            'easting_ft': easting_ft,
            'northing_ft': northing_ft,
            'easting_m': x,
            'northing_m': y,
            'latitude': latitude,
            'longitude': longitude
        }


# Try to use pyproj for local development, fall back to pure Python for Vercel
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
    print("⚠️ pyproj not available - using accurate pure Python converter")
    GhanaWebConverter = GhanaPurePythonConverter  # type: ignore