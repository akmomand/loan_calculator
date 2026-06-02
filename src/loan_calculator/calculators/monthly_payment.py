def prin_int(P, annual_rate, years):
    """Calculate the monthly mortgage payment for a given principal, interest rate, and loan term.
    Args:
        P: Principal amount of the loan
        annual_rate: Monthly interest rate (as a decimal)
        years: Number of payments (total months)
    Returns:
        Monthly mortgage payment
    """
    r = annual_rate / 12
    n = years * 12
    if r == 0:
        return P / n
    else:
        return P * (r * (1 + r) ** n) / ((1 + r) ** n - 1)


print(prin_int(490000, 0.03, 30))
    