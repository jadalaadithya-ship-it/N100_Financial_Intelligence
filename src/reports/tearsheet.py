import sqlite3
from pathlib import Path

import pandas as pd
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"
REPORT_DIR = PROJECT_ROOT / "reports" / "tearsheets"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB_PATH)

styles = getSampleStyleSheet()


def fmt(value, suffix=""):
    """
    Safely format numeric values.
    Returns N/A for None or NaN.
    """
    if pd.isna(value):
        return "N/A"

    try:
        return f"{float(value):.2f}{suffix}"
    except Exception:
        return str(value)


def generate_tearsheet(company):

    company_df = pd.read_sql(
        "SELECT * FROM companies WHERE id=?",
        conn,
        params=[company],
    )

    if company_df.empty:
        print(company, "not found")
        return

    company_row = company_df.iloc[0]

    ratio = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios_computed
        WHERE company_id=?
        ORDER BY year DESC
        LIMIT 1
        """,
        conn,
        params=[company],
    )

    pdf_path = REPORT_DIR / f"{company}.pdf"

    doc = SimpleDocTemplate(str(pdf_path))

    story = []

    # -------------------------
    # Title
    # -------------------------

    story.append(
        Paragraph(
            f"<b>{company_row['company_name']}</b>",
            styles["Title"],
        )
    )

    story.append(Spacer(1, 12))

    # -------------------------
    # About Company
    # -------------------------

    about = company_row["about_company"]

    if pd.isna(about):
        about = "Description not available."

    story.append(
        Paragraph(
            about,
            styles["BodyText"],
        )
    )

    story.append(Spacer(1, 20))

    # -------------------------
    # Financial Ratios
    # -------------------------

    if not ratio.empty:

        r = ratio.iloc[0]

        story.append(
            Paragraph(
                "<b>Latest Financial Ratios</b>",
                styles["Heading2"],
            )
        )

        story.append(
            Paragraph(
                f"ROE : {fmt(r['return_on_equity_pct'], ' %')}",
                styles["BodyText"],
            )
        )

        story.append(
            Paragraph(
                f"Net Profit Margin : {fmt(r['net_profit_margin_pct'], ' %')}",
                styles["BodyText"],
            )
        )

        story.append(
            Paragraph(
                f"Operating Margin : {fmt(r['operating_profit_margin_pct'], ' %')}",
                styles["BodyText"],
            )
        )

        story.append(
            Paragraph(
                f"Debt / Equity : {fmt(r['debt_to_equity'])}",
                styles["BodyText"],
            )
        )

        story.append(
            Paragraph(
                f"Asset Turnover : {fmt(r['asset_turnover'])}",
                styles["BodyText"],
            )
        )

        story.append(
            Paragraph(
                f"Financial Year : {r['year']}",
                styles["BodyText"],
            )
        )

    else:

        story.append(
            Paragraph(
                "Financial ratio data not available.",
                styles["BodyText"],
            )
        )

    story.append(Spacer(1, 20))

    # -------------------------
    # Company Information
    # -------------------------

    story.append(
        Paragraph(
            "<b>Company Information</b>",
            styles["Heading2"],
        )
    )

    story.append(
        Paragraph(
            f"Face Value : {fmt(company_row['face_value'])}",
            styles["BodyText"],
        )
    )

    story.append(
        Paragraph(
            f"Book Value : {fmt(company_row['book_value'])}",
            styles["BodyText"],
        )
    )

    story.append(
        Paragraph(
            f"ROCE : {fmt(company_row['roce_percentage'], ' %')}",
            styles["BodyText"],
        )
    )

    story.append(
        Paragraph(
            f"ROE : {fmt(company_row['roe_percentage'], ' %')}",
            styles["BodyText"],
        )
    )

    website = company_row["website"]

    if pd.isna(website):
        website = "N/A"

    story.append(
        Paragraph(
            f"Website : {website}",
            styles["BodyText"],
        )
    )

    doc.build(story)

    print(f"{company} PDF created")


if __name__ == "__main__":

    companies = pd.read_sql(
        "SELECT id FROM companies",
        conn,
    )

    for company in companies["id"]:
        try:
            generate_tearsheet(company)
        except Exception as e:
            print(f"Error generating PDF for {company}: {e}")

    conn.close()