from flask import Flask, render_template, request, jsonify
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
from calculator import visualize_triple_portfolio_analysis

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Get form data
        data = request.json

        initial_income = float(data['initial_income'])
        savings_rate_pct = float(data['savings_rate_pct'])
        income_growth_annual_pct = float(data['income_growth_annual_pct'])
        roi_annual_pct = float(data['roi_annual_pct'])
        inflation_annual_pct = float(data['inflation_annual_pct'])
        target_passive_real = float(data['target_passive_real'])
        life_expectancy_years = float(data['life_expectancy_years'])
        reinvest_percent_retirement = float(data['reinvest_percent_retirement'])
        initial_savings = float(data.get('initial_savings', 0))

        # Generate plot using calculator.py
        data, target_year, img_base64 = visualize_triple_portfolio_analysis(
            initial_income, savings_rate_pct, income_growth_annual_pct,
            roi_annual_pct, inflation_annual_pct, target_passive_real,
            life_expectancy_years, reinvest_percent_retirement, initial_savings
        )

        return jsonify({
            'success': True,
            'image': img_base64,
            'target_year': round(target_year, 2)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
