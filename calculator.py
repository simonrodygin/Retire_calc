import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter, MaxNLocator
import io
import base64


def visualize_triple_portfolio_analysis(
        initial_income,
        savings_rate_pct,
        income_growth_annual_pct,
        roi_annual_pct,
        inflation_annual_pct,
        target_passive_real,
        life_expectancy_years,
        reinvest_percent_retirement,
        initial_savings = 0,
):
    # --- Math Setup ---
    nom_m_rate = (1 + roi_annual_pct / 100) ** (1 / 12) - 1
    m_inflation = (1 + inflation_annual_pct / 100) ** (1 / 12) - 1

    nom_bal, real_bal, total_inv_nom, total_inv_real = initial_savings, initial_savings, initial_savings, initial_savings
    curr_income = initial_income
    data, months, curr_real_passive = [], 0, 0

    # money movement before retirement
    while curr_real_passive < target_passive_real:
        months += 1
        nom_dep = curr_income * (savings_rate_pct / 100)
        real_dep = nom_dep / ((1 + m_inflation) ** months)

        # 1. Считаем ВЕСЬ сгенерированный доход
        gen_nom = nom_bal * nom_m_rate
        gen_real = gen_nom / ((1 + m_inflation) ** months)

        # 2. До пенсии наша потенциальная пенсия равна всему доходу
        pen_real = gen_real *  (1 - reinvest_percent_retirement / 100)

        # Update Balances (докладываем депозиты, реинвестируем 100% прибыли)
        nom_bal = nom_bal * (1 + nom_m_rate) + nom_dep
        real_bal = nom_bal / ((1 + m_inflation) ** months)  # Надежное дефлирование
        total_inv_nom += nom_dep
        total_inv_real += real_dep

        # Для условия цикла берем реальную пенсию
        curr_real_passive = pen_real

        data.append({
            'Year': months / 12,
            'Nominal_Inv': total_inv_nom,
            'Nominal_Profit': max(0, nom_bal - total_inv_nom),
            'Real_Inv': total_inv_real,
            'Real_Profit': max(0, real_bal - total_inv_real),
            'Gen_Nominal': gen_nom,
            'Gen_Real': gen_real,
            'Pen_Nominal': None,
            'Pen_Real': None
        })

        if months % 12 == 0:
            curr_income *= (1 + income_growth_annual_pct / 100)

    target_year_to_mark = data[-1]['Year']

    # money movement after retirement
    while months < life_expectancy_years * 12:
        months += 1

        reinvest_fraction = reinvest_percent_retirement / 100
        withdrawal_fraction = 1 - reinvest_fraction

        # 1. Весь сгенерированный доход
        gen_nom = nom_bal * nom_m_rate
        gen_real = gen_nom / ((1 + m_inflation) ** months)

        # 2. Фактическая пенсия (снимаем только часть)
        pen_nom = gen_nom * withdrawal_fraction
        pen_real = gen_real * withdrawal_fraction

        # Обновляем баланс: капитал растет ТОЛЬКО на реинвестированную часть
        nom_bal = nom_bal + (gen_nom * reinvest_fraction)
        real_bal = nom_bal / ((1 + m_inflation) ** months)

        data.append({
            'Year': months / 12,
            'Nominal_Inv': 0,
            'Nominal_Profit': nom_bal,
            'Real_Inv': 0,
            'Real_Profit': real_bal,
            'Gen_Nominal': gen_nom,
            'Gen_Real': gen_real,
            'Pen_Nominal': pen_nom,
            'Pen_Real': pen_real
        })

    df = pd.DataFrame(data)

    # --- Visuals ---
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

    def format_m(x, pos):
        return f'{x * 1e-6:,.2f}M'

    def format_k(x, pos):
        return f'{x:,.0f}'

    # Plot 1: Nominal Stack
    ax1.stackplot(df['Year'], df['Nominal_Inv'], df['Nominal_Profit'],
                  labels=['Nominal Deposits', 'Nominal Profit'], colors=['#d62728', '#1f77b4'], alpha=0.7)
    ax1.set_title('Nominal Portfolio Composition (Face Value)', fontsize=14)
    ax1.yaxis.set_major_formatter(FuncFormatter(format_m))
    ax1.legend(loc='upper left')

    # Plot 2: Real Stack
    ax2.stackplot(df['Year'], df['Real_Inv'], df['Real_Profit'],
                  labels=['Real Deposits', 'Real Profit'], colors=['#9467bd', '#2ca02c'], alpha=0.7)
    ax2.set_title('Real Portfolio Composition (Purchasing Power)', fontsize=14)
    ax2.yaxis.set_major_formatter(FuncFormatter(format_m))
    ax2.legend(loc='upper left')

    # Plot 3: Passive Income Growth
    # 1. Левая ось - РЕАЛЬНЫЕ показатели (зеленые оттенки)
    ax3.plot(df['Year'], df['Gen_Real'], label='Total Generated (Real)', color='#2ca02c', linewidth=2, alpha=0.4)
    ax3.plot(df['Year'], df['Pen_Real'], label='Actual Pension (Real)', color='#2ca02c', linewidth=3)
    ax3.axhline(y=target_passive_real, color='orange', linestyle='--', label='Target (Real)')
    ax3.axhline(y=data[-1]['Pen_Real'], color='red', linestyle='--', label='Target (Real)')
    ax3.set_ylabel('Real Income', fontsize=12)
    ax3.yaxis.set_major_formatter(FuncFormatter(format_k))

    # 2. Правая ось - НОМИНАЛЬНЫЕ показатели (синие оттенки)
    ax3_twin = ax3.twinx()
    ax3_twin.plot(df['Year'], df['Gen_Nominal'], label='Total Generated (Nominal)', color='#1f77b4', linewidth=2,
                  alpha=0.4)
    ax3_twin.plot(df['Year'], df['Pen_Nominal'], label='Actual Pension (Nominal)', color='#1f77b4', linewidth=3)
    ax3_twin.set_ylabel('Nominal Income', fontsize=12)
    ax3_twin.yaxis.set_major_formatter(FuncFormatter(format_k))

    # 3. Объединяем легенды
    lines_1, labels_1 = ax3.get_legend_handles_labels()
    lines_2, labels_2 = ax3_twin.get_legend_handles_labels()
    ax3.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

    ax3.set_title('Monthly Passive Income Development & Pension Extraction', fontsize=14)
    ax3.set_xlabel('Years', fontsize=12)

    for ax in [ax1, ax2, ax3]:
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.yaxis.set_major_locator(MaxNLocator(nbins=15))

        ax.axvline(x=target_year_to_mark, color='red', linestyle=':', linewidth=2, alpha=0.7)

    plt.tight_layout()

    # Convert plot to base64 string for web display
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)

    return data, target_year_to_mark, img_base64


# Run
visualize_triple_portfolio_analysis(3100, 60, 5, 8, 4, 2000, 45, 30, 32000)