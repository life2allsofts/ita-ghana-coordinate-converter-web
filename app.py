from flask import Flask, render_template, request, jsonify
from converter.ghana_converter import GhanaWebConverter
from converter.coordinate_utils import dms_to_decimal, decimal_to_dms

app = Flask(__name__)
converter = GhanaWebConverter()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_coordinates():
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({'success': False, 'error': 'No JSON payload provided'}), 400

        conversion_type = data.get('type')
        if conversion_type == 'grid_to_geo':
            if 'easting' not in data or 'northing' not in data:
                return jsonify({'success': False, 'error': 'Missing easting or northing'}), 400
            try:
                easting = float(data['easting'])
                northing = float(data['northing'])
            except (TypeError, ValueError):
                return jsonify({'success': False, 'error': 'Invalid easting or northing value'}), 400

            result = converter.grid_to_geo(easting, northing)
            
            # Add DMS display
            result['latitude_dms'] = decimal_to_dms(result['latitude'], is_latitude=True)
            result['longitude_dms'] = decimal_to_dms(result['longitude'], is_latitude=False)
            
        elif conversion_type == 'geo_to_grid':
            # Handle both decimal and DMS input
            if 'latitude_dms' in data and 'longitude_dms' in data:
                lat = dms_to_decimal(data['latitude_dms'])
                lon = dms_to_decimal(data['longitude_dms'])
            else:
                if 'latitude' not in data or 'longitude' not in data:
                    return jsonify({'success': False, 'error': 'Missing latitude or longitude'}), 400
                try:
                    lat = float(data['latitude'])
                    lon = float(data['longitude'])
                except (TypeError, ValueError):
                    return jsonify({'success': False, 'error': 'Invalid latitude or longitude value'}), 400
            
            result = converter.geo_to_grid(lat, lon)
            
            # Add DMS display
            result['latitude_dms'] = decimal_to_dms(lat, is_latitude=True)
            result['longitude_dms'] = decimal_to_dms(lon, is_latitude=False)
        else:
            return jsonify({'success': False, 'error': 'Unknown conversion type'}), 400
        
        return jsonify({'success': True, 'data': result})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)