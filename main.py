import datetime
from pathlib import Path
from fpdf import FPDF
from src.pipeline_etl import extract_sales, transform_sales, load_sales_summary
from src.analytics import generate_insights
from src.plots import compile_analytical_plots

class ExecutiveReportPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 10, "Walmart Enterprise Performance Tracking Portal", ln=True, border="B")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()} | Confidential Internal Data Assets", align="C")

def build_pdf_report(insights: dict, plots_dir: Path, out_pdf: Path):
    """Generates structural executive-ready analytical reports to target directories."""
    pdf = ExecutiveReportPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Page 1: Abstract Cover Summary
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 24)
    pdf.cell(0, 15, "Walmart Sales Performance Report", ln=True, align="L")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 10, f"Pipeline Automation Compilation Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(10)
    
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 7, "This document encapsulates high-velocity diagnostic indicators derived automatically "
                         "through our custom data management engine. All metric logs are derived from structured data partitions.")
    pdf.ln(10)
    
    # Page 2: Key Strategic Metrics
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Core Financial Insights Matrix", ln=True)
    pdf.ln(5)
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, f"Top Revenue Generation Unit  : Store {insights['top_store']}", ln=True)
    pdf.cell(0, 8, f"Underperforming Operational Unit: Store {insights['worst_store']}", ln=True)
    pdf.ln(5)
    
    # Milestone Days Tracking Breakdown
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Historical Benchmark Breakdowns", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, f"Peak Transactions Profile  -> Date: {insights['best_day']['date']} | Store: {insights['best_day']['store']} | Value: ${insights['best_day']['sales']:,.2f}", ln=True)
    pdf.cell(0, 6, f"Lowest Transactions Profile -> Date: {insights['worst_day']['date']} | Store: {insights['worst_day']['store']} | Value: ${insights['worst_day']['sales']:,.2f}", ln=True)
    
    # Page 3: Visual Layout Graphics Map
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Data Visualization Summary Matrices", ln=True)
    pdf.ln(5)
    
    pdf.image(str(plots_dir / "weekly_sales_ma7.png"), x=15, w=180)
    pdf.ln(5)
    pdf.image(str(plots_dir / "sales_heatmap_month_by_year.png"), x=15, w=180)
    
    out_pdf.parent.mkdir(exist_ok=True)
    pdf.output(str(out_pdf))

def main():
    BASE_DIR = Path(__file__).resolve().parent
    DB_PATH = BASE_DIR / "data" / "sales.db"
    OUTPUT_DIR = BASE_DIR / "outputs"
    PDF_REPORT_PATH = OUTPUT_DIR / "sales_report.pdf"
    
    print("[ETL Pipeline] Initiating extraction steps...")
    raw_data = extract_sales(days=60)
    
    print("[ETL Pipeline] Initiating business logical transformations...")
    transformed_df = transform_sales(raw_data)
    
    print(f"[ETL Pipeline] Streaming arrays directly to warehouse: {DB_PATH}")
    load_sales_summary(transformed_df, DB_PATH)
    
    print("[Analytics] Compiling diagnostic insights maps...")
    insights = generate_insights(transformed_df)
    
    print("[Graphics Engine] Compiling plotting instances...")
    compile_analytical_plots(transformed_df, OUTPUT_DIR)
    
    print("[Reporting] Designing high-fidelity Executive PDF manual...")
    build_pdf_report(insights, OUTPUT_DIR, PDF_REPORT_PATH)
    
    print(f"\n Automated Execution Complete. Report accessible at: {PDF_REPORT_PATH}")

if __name__ == "__main__":
    main()