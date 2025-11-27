# ITA Ghana Coordinate Converter - Web Version
A professional web application for converting between Ghana Grid coordinates and Geographic coordinates (WGS84).

## 🎯 Features

- **Grid → Geographic Conversion**: Convert Ghana Grid coordinates to Latitude/Longitude
- **Geographic → Grid Conversion**: Convert Latitude/Longitude to Ghana Grid coordinates  
- **DMS Input Support**: Enter coordinates in Degrees, Minutes, Seconds format
- **Survey-Grade Accuracy**: Meets Ghana cadastral standards (±0.33ft precision)
- **Professional UI**: Clean, responsive design optimized for surveyors

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Geospatial**: pyproj for coordinate transformations
- **Deployment**: Vercel

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py

# Visit http://localhost:5000
📁 Project Structure
text
ghana-web-converter/
├── app.py                 # Main Flask application
├── converter/             # Core conversion logic
│   ├── __init__.py
│   ├── ghana_converter.py
│   └── coordinate_utils.py
├── templates/             # HTML templates
│   └── index.html
├── static/               # Static assets
│   ├── css/
│   ├── js/
│   └── images/
├── requirements.txt       # Python dependencies
└── vercel.json           # Deployment configuration
🎯 Usage Examples
Grid to Geographic
text
Input: Easting=1199601.82 ft, Northing=333506.23 ft
Output: Lat=5.588358, Lon=-0.175317
Geographic to Grid
text
Input: Lat=5.588358, Lon=-0.175317
Output: Easting=1199601.82 ft, Northing=333506.23 ft
🔧 Development
This project was developed through AI-assisted programming, demonstrating practical application of:

Flask web development

Geospatial coordinate transformations

Professional UI/UX design

Git version control

Vercel deployment

📄 License
MIT License - see LICENSE file for details

👨‍💻 Developer
Isaac Tetteh-Apotey

📧 Email: tettehapotey@gmail.com

📱 Phone: +233-559846747

🌐 Portfolio: life2allsofts.github.io

💼 LinkedIn: [Isaac Tetteh-Apotey](https://www.linkedin.com/in/isaac-tetteh-apotey-67408b89/)

Professional Background:
Geomatics Engineer with 15+ years experience

Quantic MSSE Candidate (Expected 2026)

Ghana Institution of Surveyors (GhIS) Member

Full-Stack Developer specializing in geospatial solutions

🆘 Support
For support, email tettehapotey@gmail.com or create an issue in this repository.

