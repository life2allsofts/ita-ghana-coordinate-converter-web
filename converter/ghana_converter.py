from pyproj import Transformer

class GhanaWebConverter:
    def __init__(self):
        # OUR EXACT parameters from successful Dart implementation
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
        """Convert Ghana Grid to Geographic coordinates"""
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
        """Convert Geographic to Ghana Grid coordinates"""
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