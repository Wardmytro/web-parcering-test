def calculate_net_profit(income, tax_percent):
    net_profit = income - (income * tax_percent)
    corporate_net_profit = net_profit * 0.8
    return corporate_net_profit


if __name__ == "__main__":
    print(calculate_net_profit(1000, 0.5))
