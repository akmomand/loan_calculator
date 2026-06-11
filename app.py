import io

import pandas as pd
import streamlit as st

from src.loan_calculator.calculators.monthly_payment import prin_int
from src.loan_calculator.calculators.payoff_length import payoff_length

SCHEDULE_PREVIEW_ROWS = 20

st.set_page_config(
    page_title="Loan Calculator",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .block-container { padding-top: 3rem; padding-bottom: 2rem; overflow: visible; }
    [data-testid="stMarkdownContainer"] { overflow: visible !important; }
    .hero-header {
        padding: 0.5rem 0 0.25rem 0;
        overflow: visible;
    }
    .hero-title {
        font-size: 2.4rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.35;
        padding: 0.1em 0;
        background: linear-gradient(90deg, #818CF8, #6366F1);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        color: transparent;
        display: block;
        overflow: visible;
    }
    .hero-subtitle {
        color: #94A3B8;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.1rem 1.25rem;
        height: 100%;
    }
    .metric-label {
        color: #94A3B8;
        font-size: 0.85rem;
        margin-bottom: 0.35rem;
    }
    .metric-value {
        color: #F8FAFC;
        font-size: 1.55rem;
        font-weight: 700;
    }
    .section-title {
        font-size: 1.15rem;
        font-weight: 600;
        margin: 1.5rem 0 0.75rem 0;
        color: #E2E8F0;
    }
    div[data-testid="stSidebar"] .stRadio > label {
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def format_currency(value: float) -> str:
    return f"${value:,.2f}"


def format_percent(value: float) -> str:
    return f"{value:.2f}%"


def render_metric_card(label: str, value: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def normalize_schedule_result(result: tuple) -> dict:
    """Normalize prin_int return values across 0% and standard interest cases."""
    monthly_payment = result[0]

    if len(result) == 2:
        schedule = result[1]
        schedule_df = (
            pd.DataFrame(schedule)
            if not isinstance(schedule, pd.DataFrame)
            else schedule
        )
        total_principal = schedule_df["principal"].sum()
        total_interest = schedule_df["interest"].sum()
        total_paid = schedule_df["total_payment"].sum()
    else:
        schedule_df = result[1]
        total_principal = result[2]
        total_interest = result[3]
        total_paid = result[4]

    return {
        "monthly_payment": monthly_payment,
        "schedule_df": schedule_df,
        "total_principal": total_principal,
        "total_interest": total_interest,
        "total_paid": total_paid,
    }


def prepare_schedule_display(schedule_df: pd.DataFrame) -> pd.DataFrame:
    display_df = schedule_df.copy()
    display_df = display_df.rename(
        columns={
            "month": "Month",
            "interest": "Interest",
            "principal": "Principal",
            "total_payment": "Payment",
            "balance": "Remaining Balance",
        }
    )
    for col in ("Interest", "Principal", "Payment", "Remaining Balance"):
        if col in display_df.columns:
            display_df[col] = display_df[col].map(lambda x: f"${x:,.2f}")
    return display_df


def minimum_monthly_interest(principal: float, annual_rate: float) -> float:
    return principal * annual_rate / 12


def render_payment_too_low_error(principal: float, annual_rate: float) -> None:
    min_interest = minimum_monthly_interest(principal, annual_rate)
    st.error("Monthly payment is too low to cover the interest.")
    st.warning(
        "Your monthly payment must be greater than the first month's interest charge "
        f"({format_currency(min_interest)})."
    )


def payoff_label(years: int, remaining_months: int) -> str:
    if years or remaining_months:
        return f"{years} yr {remaining_months} mo"
    return "0 mo"


def schedule_to_csv(schedule_df: pd.DataFrame) -> bytes:
    export_df = schedule_df.rename(
        columns={
            "month": "Month",
            "interest": "Interest Paid",
            "principal": "Principal Paid",
            "total_payment": "Monthly Payment",
            "balance": "Remaining Balance",
        }
    )
    buffer = io.StringIO()
    export_df.to_csv(buffer, index=False)
    return buffer.getvalue().encode("utf-8")


# Sidebar

st.sidebar.markdown("## Loan Inputs")
calculator_mode = st.sidebar.radio(
    "What would you like to calculate?",
    [
        "Monthly Payment & Schedule",
        "Payoff Timeline & Total Cost",
    ],
    help="Choose the calculator that matches the loan question you want answered.",
)

principal = st.sidebar.number_input(
    "Loan Amount ($)",
    min_value=1_000,
    max_value=10_000_000,
    value=300_000,
    step=1_000,
    format="%d",
)

annual_rate_pct = st.sidebar.number_input(
    "Annual Interest Rate (%)",
    min_value=0.0,
    max_value=30.0,
    value=6.5,
    step=0.1,
    format="%.2f",
)

annual_rate = annual_rate_pct / 100

if calculator_mode == "Monthly Payment & Schedule":
    loan_term_years = st.sidebar.number_input(
        "Loan Term (years)",
        min_value=1,
        max_value=40,
        value=30,
        step=1,
    )
else:
    monthly_payment_input = st.sidebar.number_input(
        "Monthly Payment ($)",
        min_value=1.0,
        max_value=100_000.0,
        value=2_000.0,
        step=50.0,
        format="%.2f",
    )

calculate = st.sidebar.button("Calculate", type="primary", use_container_width=True)

st.sidebar.markdown("---")
with st.sidebar.expander("About these calculators"):
    st.markdown(
        """
        **Monthly Payment & Schedule** — Enter principal, rate, and term to get
        your fixed monthly payment plus a full amortization schedule.

        **Payoff Timeline & Total Cost** — Enter principal, rate, and a monthly
        payment to see how long until the loan is paid off and what you'll pay
        in total.
        """
    )

# Main content

st.markdown(
    '<div class="hero-header"><h1 class="hero-title">Loan Calculator</h1></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="hero-subtitle">'
    "Model your loan with two calculators: "
    "monthly payments with an amortization schedule, or payoff timeline and total cost."
    "</p>",
    unsafe_allow_html=True,
)

if not calculate:
    st.info("Adjust your loan details in the sidebar, then click **Calculate** to see results.")
    st.stop()

# Monthly Payment & Schedule

if calculator_mode == "Monthly Payment & Schedule":
    try:
        result = normalize_schedule_result(prin_int(principal, annual_rate, loan_term_years))
    except Exception as exc:
        st.error(f"Could not calculate monthly payment: {exc}")
        st.stop()

    st.markdown('<p class="section-title">Payment Summary</p>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_metric_card("Monthly Payment", format_currency(result["monthly_payment"]))
    with col2:
        render_metric_card("Total Interest", format_currency(result["total_interest"]))
    with col3:
        render_metric_card("Total Paid", format_currency(result["total_paid"]))
    with col4:
        render_metric_card("Loan Term", f"{loan_term_years} years")

    st.markdown('<p class="section-title">Amortization Schedule</p>', unsafe_allow_html=True)

    schedule_df = result["schedule_df"]
    total_rows = len(schedule_df)
    preview_df = prepare_schedule_display(schedule_df.head(SCHEDULE_PREVIEW_ROWS))

    st.dataframe(preview_df, use_container_width=True, hide_index=True)

    if total_rows > SCHEDULE_PREVIEW_ROWS:
        st.caption(
            f"Showing the first {SCHEDULE_PREVIEW_ROWS} of {total_rows:,} payments. "
            "Download the CSV below for the complete schedule."
        )
    else:
        st.caption(f"Showing all {total_rows:,} payments.")

    st.download_button(
        label="Download Full Schedule (CSV)",
        data=schedule_to_csv(schedule_df),
        file_name=f"amortization_schedule_{int(principal)}_{loan_term_years}yr.csv",
        mime="text/csv",
        use_container_width=False,
    )

# Payoff Timeline & Total Cost

else:
    try:
        (
            _principal,
            total_paid,
            total_interest,
            years,
            remaining_months,
        ) = payoff_length(principal, annual_rate, monthly_payment_input)
    except ValueError:
        render_payment_too_low_error(principal, annual_rate)
        st.stop()
    except Exception as exc:
        st.error(f"Could not calculate payoff timeline: {exc}")
        st.stop()

    total_months = years * 12 + remaining_months

    st.markdown('<p class="section-title">Payoff Timeline</p>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_metric_card("Monthly Payment", format_currency(monthly_payment_input))
    with col2:
        render_metric_card("Payoff Time", payoff_label(years, remaining_months))
    with col3:
        render_metric_card("Total Interest", format_currency(total_interest))
    with col4:
        render_metric_card("Total Paid", format_currency(total_paid))

    timeline_data = pd.DataFrame(
        {
            "Metric": [
                "Principal",
                "Annual Rate",
                "Monthly Payment",
                "Total Months",
                "Total Amount Paid",
                "Total Interest Paid",
            ],
            "Value": [
                format_currency(principal),
                format_percent(annual_rate_pct),
                format_currency(monthly_payment_input),
                f"{total_months:,}",
                format_currency(total_paid),
                format_currency(total_interest),
            ],
        }
    )
    interest_ratio = total_interest / principal * 100
    st.progress(min(interest_ratio / 100, 1.0))
    st.caption(
        f"Interest represents {interest_ratio:.1f}% of the original "
        f"{format_currency(principal)} principal."
    )

    st.markdown('<p class="section-title">Loan Details</p>', unsafe_allow_html=True)
    st.dataframe(timeline_data, use_container_width=True, hide_index=True)
