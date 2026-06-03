def payoff_length(P, annual_rate, monthly_payment):
    """Calculate the number of months it will take to pay off a loan given the principal, annual interest rate, and monthly payment."""
    r = annual_rate / 12
    balance = P
    months = 0
    total_paid = 0.0
    if monthly_payment <= r * balance:
        raise ValueError("Monthly payment is too low to cover the interest.")
    while balance > 0:
        interest = balance * r
        principal_paid = monthly_payment - interest
        balance -= principal_paid
        months += 1
        total_paid += monthly_payment

        if balance < 0:
            balance = 0
    

    years = months / 12

    total_interest = total_paid - P

    return {
        "Principal: ": P,
        "Total Amount Paid: ": total_paid,
        "Total Interest Paid: ": total_interest,
        "Years to Pay Off: ": years,
        "Months to Pay Off: ": months
    }
        

if __name__ == "__main__":
    principal = 500000
    annual_rate = 0.05
    monthly_payment = 3000
    print(payoff_length(principal, annual_rate, monthly_payment))