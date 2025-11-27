// Simple and reliable UI Handler with null checks
class UIHandler {
    constructor() {
        this.currentConversionType = 'grid_to_geo';
        this.currentFormat = 'dd';
        this.init();
    }

    init() {
        this.bindEvents();
        this.setDefaultValues();
        console.log('UI Handler initialized');
    }

    bindEvents() {
        // Conversion type buttons
        const conversionBtns = document.querySelectorAll('.conversion-btn');
        if (conversionBtns.length === 0) {
            console.error('No conversion buttons found!');
            return;
        }

        conversionBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.switchConversionType(e.target.dataset.type);
            });
        });

        // Format radio buttons
        const formatRadios = document.querySelectorAll('input[name="format"]');
        if (formatRadios.length > 0) {
            formatRadios.forEach(radio => {
                radio.addEventListener('change', (e) => {
                    this.switchInputFormat(e.target.value);
                });
            });
        }

        // Convert button
        const convertBtn = document.getElementById('convert-btn');
        if (convertBtn) {
            convertBtn.addEventListener('click', () => {
                this.convertCoordinates();
            });
        } else {
            console.error('Convert button not found!');
        }

        // DMS text inputs
        const dmsLatInput = document.getElementById('dms-latitude');
        const dmsLonInput = document.getElementById('dms-longitude');
        
        if (dmsLatInput) {
            dmsLatInput.addEventListener('change', () => this.parseDmsTextInput('latitude'));
        }
        if (dmsLonInput) {
            dmsLonInput.addEventListener('change', () => this.parseDmsTextInput('longitude'));
        }
    }

    switchConversionType(type) {
        console.log('Switching to:', type);
        this.currentConversionType = type;
        
        // Update active button
        document.querySelectorAll('.conversion-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        
        const activeBtn = document.querySelector(`.conversion-btn[data-type="${type}"]`);
        if (activeBtn) {
            activeBtn.classList.add('active');
        }
        
        // Show correct input section - FIXED ID NAMES
        document.querySelectorAll('.input-section').forEach(section => {
            section.classList.remove('active');
        });
        
        // Convert data-type to match HTML IDs
        let targetId;
        if (type === 'grid_to_geo') {
            targetId = 'grid-to-geo-input'; // Match HTML ID
        } else {
            targetId = 'geo-to-grid-input'; // Match HTML ID
        }
        
        const targetSection = document.getElementById(targetId);
        if (targetSection) {
            targetSection.classList.add('active');
            console.log(`Showing section: ${targetId}`);
        } else {
            console.error(`Input section not found: ${targetId}`);
        }
        
        this.clearResults();
    }

    switchInputFormat(format) {
        console.log('Switching format to:', format);
        this.currentFormat = format;
        
        const ddInput = document.getElementById('dd-input');
        const dmsInput = document.getElementById('dms-input');
        
        if (ddInput && dmsInput) {
            if (format === 'dd') {
                ddInput.style.display = 'block';
                dmsInput.style.display = 'none';
            } else {
                ddInput.style.display = 'none';
                dmsInput.style.display = 'block';
            }
        }
        
        this.clearResults();
    }

    async convertCoordinates() {
        const convertBtn = document.getElementById('convert-btn');
        const loading = document.getElementById('loading');
        const errorMessage = document.getElementById('error-message');
        
        if (!convertBtn || !loading || !errorMessage) {
            console.error('Required elements not found for conversion');
            return;
        }
        
        try {
            // Show loading
            convertBtn.disabled = true;
            loading.style.display = 'block';
            errorMessage.style.display = 'none';
            this.clearResults();

            const data = this.getInputData();
            
            const response = await fetch('/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                this.displayResults(result.data);
            } else {
                throw new Error(result.error);
            }

        } catch (error) {
            errorMessage.textContent = error.message;
            errorMessage.style.display = 'block';
        } finally {
            convertBtn.disabled = false;
            loading.style.display = 'none';
        }
    }

    getInputData() {
        const data = { type: this.currentConversionType };

        if (this.currentConversionType === 'grid_to_geo') {
            const easting = document.getElementById('easting');
            const northing = document.getElementById('northing');
            
            if (!easting || !northing || !easting.value || !northing.value) {
                throw new Error('Please enter both easting and northing values');
            }
            
            data.easting = parseFloat(easting.value);
            data.northing = parseFloat(northing.value);
        } else {
            if (this.currentFormat === 'dd') {
                const latitude = document.getElementById('latitude');
                const longitude = document.getElementById('longitude');
                
                if (!latitude || !longitude || !latitude.value || !longitude.value) {
                    throw new Error('Please enter both latitude and longitude values');
                }
                
                data.latitude = parseFloat(latitude.value);
                data.longitude = parseFloat(longitude.value);
            } else {
                // Check DMS text inputs first
                const dmsLatText = document.getElementById('dms-latitude');
                const dmsLonText = document.getElementById('dms-longitude');
                
                if (dmsLatText && dmsLonText && dmsLatText.value && dmsLonText.value) {
                    data.latitude_dms = dmsLatText.value;
                    data.longitude_dms = dmsLonText.value;
                } else {
                    // Use component inputs
                    const latDegrees = document.getElementById('lat-degrees');
                    const latMinutes = document.getElementById('lat-minutes');
                    const latSeconds = document.getElementById('lat-seconds');
                    const latHemisphere = document.getElementById('lat-hemisphere');
                    
                    const lonDegrees = document.getElementById('lon-degrees');
                    const lonMinutes = document.getElementById('lon-minutes');
                    const lonSeconds = document.getElementById('lon-seconds');
                    const lonHemisphere = document.getElementById('lon-hemisphere');
                    
                    if (!latDegrees || !latMinutes || !latSeconds || !lonDegrees || !lonMinutes || !lonSeconds ||
                        !latDegrees.value || !latMinutes.value || !latSeconds.value || 
                        !lonDegrees.value || !lonMinutes.value || !lonSeconds.value) {
                        throw new Error('Please fill all DMS fields or use the text input');
                    }
                    
                    data.latitude_dms = `${latDegrees.value} ${latMinutes.value} ${latSeconds.value} ${latHemisphere ? latHemisphere.value : 'N'}`;
                    data.longitude_dms = `${lonDegrees.value} ${lonMinutes.value} ${lonSeconds.value} ${lonHemisphere ? lonHemisphere.value : 'W'}`;
                }
            }
        }

        return data;
    }

    displayResults(data) {
        const resultsSection = document.getElementById('results-section');
        const resultsContent = document.getElementById('results-content');
        const backBtnContainer = document.getElementById('back-btn-container');
        
        if (!resultsSection || !resultsContent) {
            console.error('Results section elements not found');
            return;
        }
        
        let html = '';
        
        if (this.currentConversionType === 'grid_to_geo') {
            html = this.generateGridToGeoResults(data);
        } else {
            html = this.generateGeoToGridResults(data);
        }
        
        resultsContent.innerHTML = html;
        resultsSection.classList.add('active');
        
        if (backBtnContainer) {
            backBtnContainer.style.display = 'block';
        }
    }

    generateGridToGeoResults(data) {
        return `
            <div class="result-item">
                <div class="result-label">Latitude</div>
                <div class="result-value">${data.latitude.toFixed(6)}</div>
            </div>
            <div class="result-item">
                <div class="result-label">Longitude</div>
                <div class="result-value">${data.longitude.toFixed(6)}</div>
            </div>
            <div class="result-item">
                <div class="result-label">Latitude (DMS)</div>
                <div class="result-value">${data.latitude_dms}</div>
            </div>
            <div class="result-item">
                <div class="result-label">Longitude (DMS)</div>
                <div class="result-value">${data.longitude_dms}</div>
            </div>
            <div class="result-item">
                <div class="result-label">Original Easting</div>
                <div class="result-value">${data.easting_ft.toFixed(2)} ft</div>
            </div>
            <div class="result-item">
                <div class="result-label">Original Northing</div>
                <div class="result-value">${data.northing_ft.toFixed(2)} ft</div>
            </div>
        `;
    }

    generateGeoToGridResults(data) {
        return `
            <div class="result-item">
                <div class="result-label">Easting</div>
                <div class="result-value">${data.easting_ft.toFixed(2)} ft</div>
            </div>
            <div class="result-item">
                <div class="result-label">Northing</div>
                <div class="result-value">${data.northing_ft.toFixed(2)} ft</div>
            </div>
            <div class="result-item">
                <div class="result-label">Easting (meters)</div>
                <div class="result-value">${data.easting_m.toFixed(2)} m</div>
            </div>
            <div class="result-item">
                <div class="result-label">Northing (meters)</div>
                <div class="result-value">${data.northing_m.toFixed(2)} m</div>
            </div>
            <div class="result-item">
                <div class="result-label">Original Latitude</div>
                <div class="result-value">${data.latitude.toFixed(6)}</div>
            </div>
            <div class="result-item">
                <div class="result-label">Original Longitude</div>
                <div class="result-value">${data.longitude.toFixed(6)}</div>
            </div>
            <div class="result-item">
                <div class="result-label">Original Latitude (DMS)</div>
                <div class="result-value">${data.latitude_dms}</div>
            </div>
            <div class="result-item">
                <div class="result-label">Original Longitude (DMS)</div>
                <div class="result-value">${data.longitude_dms}</div>
            </div>
        `;
    }

    clearResults() {
        const resultsSection = document.getElementById('results-section');
        const errorMessage = document.getElementById('error-message');
        const backBtnContainer = document.getElementById('back-btn-container');
        
        if (resultsSection) resultsSection.classList.remove('active');
        if (errorMessage) errorMessage.style.display = 'none';
        if (backBtnContainer) backBtnContainer.style.display = 'none';
    }

    setDefaultValues() {
        // Set default values for testing - with null checks
        const setValue = (id, value) => {
            const element = document.getElementById(id);
            if (element) element.value = value;
        };

        setValue('easting', '1199601.82');
        setValue('northing', '333506.23');
        setValue('latitude', '5.588358');
        setValue('longitude', '-0.175317');
        
        // Set DMS defaults
        setValue('lat-degrees', '5');
        setValue('lat-minutes', '35');
        setValue('lat-seconds', '18.09');
        setValue('lon-degrees', '0');
        setValue('lon-minutes', '10');
        setValue('lon-seconds', '31.14');
        
        // Fix longitude hemisphere default
        const lonHemisphere = document.getElementById('lon-hemisphere');
        if (lonHemisphere) lonHemisphere.value = 'W';
    }

    parseDmsTextInput(type) {
        const inputElement = document.getElementById(`dms-${type}`);
        if (!inputElement) return;
        
        const text = inputElement.value.trim();
        if (!text) return;
        
        try {
            const parsed = this.parseDmsString(text);
            
            if (type === 'latitude') {
                this.setValue('lat-degrees', parsed.degrees);
                this.setValue('lat-minutes', parsed.minutes);
                this.setValue('lat-seconds', parsed.seconds.toFixed(2));
                this.setValue('lat-hemisphere', parsed.hemisphere);
            } else {
                this.setValue('lon-degrees', parsed.degrees);
                this.setValue('lon-minutes', parsed.minutes);
                this.setValue('lon-seconds', parsed.seconds.toFixed(2));
                this.setValue('lon-hemisphere', parsed.hemisphere);
            }
            
            this.showTemporaryMessage(`${type.toUpperCase()} parsed successfully!`, 'success');
            
        } catch (error) {
            this.showTemporaryMessage(`Error parsing ${type}: ${error.message}`, 'error');
        }
    }

    parseDmsString(dmsString) {
        // Handle formats like: "5° 35' 27.51\" N" or "5 35 27.51 N" or "5°35'27.51\"N"
        const cleaned = dmsString.trim().toUpperCase();
        
        // Regex to match DMS patterns
        const patterns = [
            /([NSWE]?)\s*([-]?\d+)[°\s]?\s*(\d+)[\'\s]?\s*([\d.]+)[\"\s]?\s*([NSWE]?)/,
            /([-]?\d+)\s*[°]?\s*(\d+)\s*[\']?\s*([\d.]+)\s*[\"]?\s*([NSWE])/
        ];
        
        let match = null;
        for (const pattern of patterns) {
            match = cleaned.match(pattern);
            if (match) break;
        }
        
        if (!match) {
            throw new Error('Invalid DMS format. Use: "5° 35\' 27.51" N" or "5 35 27.51 N"');
        }
        
        let degrees, minutes, seconds, hemisphere;
        
        if (match.length === 6) {
            // First pattern
            hemisphere = (match[1] || match[5]).toUpperCase();
            degrees = parseInt(match[2]);
            minutes = parseInt(match[3]);
            seconds = parseFloat(match[4]);
        } else {
            // Second pattern
            degrees = parseInt(match[1]);
            minutes = parseInt(match[2]);
            seconds = parseFloat(match[3]);
            hemisphere = match[4].toUpperCase();
        }
        
        // Validate ranges
        if (hemisphere === 'N' || hemisphere === 'S') {
            if (degrees < 0 || degrees > 90) throw new Error('Latitude degrees must be 0-90');
        } else {
            if (degrees < 0 || degrees > 180) throw new Error('Longitude degrees must be 0-180');
        }
        
        if (minutes < 0 || minutes >= 60) throw new Error('Minutes must be 0-59');
        if (seconds < 0 || seconds >= 60) throw new Error('Seconds must be 0-59.99');
        
        return { degrees, minutes, seconds, hemisphere };
    }

    showTemporaryMessage(message, type) {
        const tempDiv = document.createElement('div');
        tempDiv.textContent = message;
        tempDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 10px 15px;
            border-radius: 5px;
            color: white;
            z-index: 1000;
            font-weight: 500;
            background: ${type === 'success' ? '#27ae60' : '#e74c3c'};
            transition: opacity 0.3s ease;
        `;
        
        document.body.appendChild(tempDiv);
        
        setTimeout(() => {
            tempDiv.style.opacity = '0';
            setTimeout(() => tempDiv.remove(), 300);
        }, 3000);
    }

    // Helper method to safely set values
    setValue(id, value) {
        const element = document.getElementById(id);
        if (element) element.value = value;
    }
}

// Simple main.js - just handles the back button with null checks
document.addEventListener('DOMContentLoaded', () => {
    // Initialize UI Handler
    window.uiHandler = new UIHandler();
    
    console.log('Ghana Coordinate Converter loaded successfully!');
});