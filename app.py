from flask import Flask, render_template, request, jsonify
from converter import GhanaWebConverter
from converter.coordinate_utils import dms_to_decimal, decimal_to_dms

app = Flask(__name__, 
            static_folder='static',
            static_url_path='/static')

converter = GhanaWebConverter()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_coordinates():
    try:
        data = request.json
        if data is None:
            return jsonify({'success': False, 'error': 'Invalid JSON in request'})
        conversion_type = data.get('type')
        
        if conversion_type == 'grid_to_geo':
            easting = float(data['easting'])
            northing = float(data['northing'])
            result = converter.grid_to_geo(easting, northing)
            
            # Add DMS display
            result['latitude_dms'] = decimal_to_dms(result['latitude'], is_latitude=True)
            result['longitude_dms'] = decimal_to_dms(result['longitude'], is_latitude=False)
            
        elif conversion_type == 'geo_to_grid':
            # Handle both decimal and DMS input
            if 'latitude_dms' in data:
                lat = dms_to_decimal(data['latitude_dms'])
                lon = dms_to_decimal(data['longitude_dms'])
            else:
                lat = float(data['latitude'])
                lon = float(data['longitude'])
            
            result = converter.geo_to_grid(lat, lon)
            
            # Add DMS display
            result['latitude_dms'] = decimal_to_dms(lat, is_latitude=True)
            result['longitude_dms'] = decimal_to_dms(lon, is_latitude=False)
        
        return jsonify({'success': True, 'data': result})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)