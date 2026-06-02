def total_amount(P, annual_rate, desired_monthly_payment):
    """Calculate the total amount you will end up paying for a loan given the principal, annual interest rate, number of years, and desired monthly payment."""
    r = annual_rate / 12
    balance = P
    total_paid = 0
    months = 0

    while balance > 0:
        interest = balance * r
        principal_paid = desired_monthly_payment - interest

        if principal_paid < 0:
            raise ValueError("Desired monthly payment is too low to cover the interest.")
        
        balance -= principal_paid
        total_paid += desired_monthly_payment
        months += 1

    total_interest = total_paid - P

    return {
        "Total Amount Paid: ": total_paid, 
        "Total Interest Paid: ":total_interest, 
        "Months to Pay Off: ": months
        }

print(total_amount(490000, 0.04, 2700))

