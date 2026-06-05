import pandas as pd
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

    # total_monthly_payment = P * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
    # total_monthly_interest = total_monthly_payment - P / n
    # total_monthly_principal = total_monthly_payment - total_monthly_interest

    # return {
    #     "Total Monthly Payment": total_monthly_payment,
    #     "Total Monthly Interest": total_monthly_interest,
    #     "Total Monthly Principal": total_monthly_principal
    # }
    if r == 0:
        monthly_payment = P / n
        schedule = []
        balance = P
        for month in range(1, n + 1):
            principal_payment = monthly_payment
            interest_payment = 0.0
            balance -= principal_payment
            schedule.append({
                "month": month,
                "interest": interest_payment,
                "principal": principal_payment,
                "total_payment": monthly_payment,
                "balance": max(balance, 0)
            })
        schedule_df = pd.DataFrame(schedule)
        return monthly_payment, schedule

    # Standard mortgage payment formula
    monthly_payment = P * (r * (1 + r) ** n) / \
                      ((1 + r) ** n - 1)

    # Build amortization schedule
    schedule = []
    balance = P
    for month in range(1, n + 1):
        interest_payment = balance * r
        principal_payment = monthly_payment - interest_payment
        balance -= principal_payment
        schedule.append({
            "month": month,
            "interest": round(interest_payment, 2),
            "principal": round(principal_payment, 2),
            "total_payment": round(monthly_payment, 2),
            "balance": round(max(balance, 0), 2)
        })

    schedule_df = pd.DataFrame(schedule)
    return round(monthly_payment, 2), schedule_df


# if __name__ == "__main__":
#     print(prin_int(490000, 0.03, 30))

if __name__ == "__main__":
    principal, schedule = prin_int(500000, 0.05, 5)
    print(f"Monthly Payment: {principal}")
    print(schedule.to_string(index=False))