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
    



    total_interest = total_paid - P

    years = months // 12
    remaining_months = months % 12

    return P, total_paid, total_interest, years, remaining_months
    
        

if __name__ == "__main__":
    P, total_paid, total_interest, years, remaining_months = payoff_length(15000, 0.154, 322)
    print(f"Principal: {P} \nTotal Amount Paid: {total_paid} \nTotal Interest Paid: {total_interest} \nTime to Pay Off: {years} years and {remaining_months} months")