income = float(input("Введіть ваш дохід: "))
if income < 10000:
    tax_percent = 0
else:
    tax_percent = 0.05
net_profit = income - (income * tax_percent)
print(f"Ваш чистий прибуток становить: {income}")