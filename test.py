from net_profit import calculate_net_profit

def test_net_profit():
    income = float(input("Введіть ваш дохід: "))
    if income < 10000:
        tax_percent = 0
    else:
        tax_percent = 0.05
    net_profit = calculate_net_profit(income, tax_percent)
    print(f"Ваш чистий прибуток становить: {net_profit}")

if __name__ == "__main__":
    test_net_profit()
