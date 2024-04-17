from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Endpoint URL for the Freight Rate Estimator API
API_URL = "https://sandbox.freightos.com/api/v1/freightEstimates"

# API key provided by Freightos
API_KEY = "TKmoQPRECmJSKeGIzKjbuiaAPFZ3Yk8I"

# Secret key provided by Freightos
SECRET_KEY = "ijZifvMx57p17wOR"

# Function to handle the main route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data from the request
        origin = request.form['origin']
        destination = request.form['destination']
        quantity = request.form['quantity']
        unit_type = request.form['unit_type']
        unit_weight = request.form['unit_weight']
        unit_volume = request.form['unit_volume']

        # Prepare request payload
        payload = {
            "load": [{
                "quantity": int(quantity),
                "unitType": unit_type,
                "unitWeightKg": float(unit_weight),
                "unitVolumeCBM": float(unit_volume)
            }],
            "legs": [{
                "origin": {"unLocationCode": origin},
                "destination": {"unLocationCode": destination}
            }]
        }

        # Send POST request to the API
        headers = {
            "Content-Type": "application/json",
            "x-apikey": API_KEY,
            "Authorization": f"Apikey {SECRET_KEY}"
        }
        response = requests.post(API_URL, json=payload, headers=headers)

        # Check if request was successful
        if response.status_code == 200:
            data = response.json()
            print(data)  # Debug print

            # Extract OCEAN data
            ocean_price_min = data.get('OCEAN', {}).get('priceEstimate', {}).get('min')
            ocean_price_max = data.get('OCEAN', {}).get('priceEstimate', {}).get('max')
            ocean_transit_time_min = data.get('OCEAN', {}).get('transitTime', {}).get('min')
            ocean_transit_time_max = data.get('OCEAN', {}).get('transitTime', {}).get('max')

            context = {
                'ocean_price_min': ocean_price_min or 'Not available',
                'ocean_price_max': ocean_price_max or 'Not available',
                'ocean_transit_time_min': ocean_transit_time_min or 'Not available',
                'ocean_transit_time_max': ocean_transit_time_max or 'Not available'
            }

            return render_template('result.html', **context)
        else:
            return f"Error: Failed to fetch data from the API. Status code: {response.status_code}"
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
