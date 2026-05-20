def show_income_tax_percentage(income = 1000, tax_percent = 0.05):
    
    print(income, tax_percent)

def calculate_net_profit():
    income = float(input("Введіть ваш дохід: "))
    if income < 10000:
        tax_percent = 0
    else:
        tax_percent = 0.05
    net_profit = income - (income * tax_percent)
    print(f"Ваш чистий прибуток становить: {net_profit}")

if __name__ == "__main__":
    calculate_net_profit()

    show_income_tax_percentage()
    show_income_tax_percentage(500,1)


