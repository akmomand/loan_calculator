def total_amount(P, annual_rate, desired_monthly_payment):
    """Calculate the total amount you will end up paying for a loan given the principal, annual interest rate, number of years, and desired monthly payment."""
    r = annual_rate / 12
    balance = P
    total_paid = 0
    months = 0
    years = 0

    if desired_monthly_payment <= r * balance:
        raise ValueError("Desired monthly payment is too low to cover the interest.")

    while balance > 0:
        interest = balance * r
        principal_paid = desired_monthly_payment - interest
        
        balance -= principal_paid
        total_paid += desired_monthly_payment
        months += 1

        if balance < 0:
            balance = 0

    total_interest = total_paid - P

    years = months // 12
    remaining_months = months % 12

    return {
        "Total Amount Paid": total_paid, 
        "Total Interest Paid":total_interest, 
        "Time to Pay Off": f"{years if years > 0 else '0'} years and {remaining_months if remaining_months > 0 else '0'} months"
        }


if __name__ == "__main__":
    print(total_amount(450000, 0.04, 2400))

