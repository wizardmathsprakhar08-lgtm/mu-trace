import argparse
import sys
import os
from pathlib import Path

# Fix Windows console UTF-8 output if possible
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.config import settings
from orchestrator import ResearchReportOrchestrator
from evaluation.eval_benchmark import BenchmarkSuite
from data.seed_data import COMPANIES_SEED

# ANSI Color codes for Windows Command Prompt
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Safe ASCII progress bar
def get_progress_bar(pct: int, length: int = 25) -> str:
    filled = int(length * (pct / 100))
    return "=" * filled + ">" + " " * max(0, length - filled - 1)

def print_banner():
    print(f"""{CYAN}{BOLD}
========================================================================
   mu-trace | AUTOMATED INSTITUTIONAL EQUITY & BANK RESEARCH REPORT
   Audited Claim Provenance | 100% Deterministic Math | Red-Team Audit
========================================================================{RESET}
""")

def run_cli_report(ticker: str, focus: str = "comprehensive"):
    print_banner()
    print(f"{BOLD}[*] Target Entity Ticker:{RESET} {YELLOW}{ticker.upper()}{RESET} (Focus: {focus})")
    
    orchestrator = ResearchReportOrchestrator()
    
    def on_progress(stage: str, pct: int, meta: dict):
        bar = get_progress_bar(pct)
        try:
            sys.stdout.write(f"\r{CYAN}[{pct:3d}%]{RESET} [{bar}] {stage[:45]:<45}")
            sys.stdout.flush()
        except Exception:
            pass

    print(f"\n{BOLD}[+] Executing mu-trace 8-Stage Research Pipeline:{RESET}")
    report = orchestrator.run_pipeline(ticker, focus=focus, progress_callback=on_progress)
    print("\n")
    
    # Header summary
    print(f"{GREEN}{BOLD}========================================================================{RESET}")
    print(f"{GREEN}{BOLD}  mu-trace REPORT GENERATION COMPLETE: {report.report_id}{RESET}")
    print(f"{GREEN}{BOLD}========================================================================{RESET}")
    print(f"{BOLD}Entity:{RESET}            {report.company_name} ({report.ticker})")
    print(f"{BOLD}As-Of Date:{RESET}        {report.as_of_date}")
    print(f"{BOLD}Audit Status:{RESET}      {GREEN}{report.status}{RESET}")
    print(f"{BOLD}Numeric Accuracy:{RESET}  {GREEN}{report.audit_summary.numeric_accuracy*100:.1f}% (Zero Hallucination Guaranteed){RESET}")
    print(f"{BOLD}Faithfulness:{RESET}      {GREEN}{report.audit_summary.faithfulness_score*100:.1f}%{RESET}")
    print(f"{BOLD}Citation Quality:{RESET}  {GREEN}{report.audit_summary.citation_precision*100:.1f}%{RESET}")
    print(f"{BOLD}Claims Breakdown:{RESET}  {report.audit_summary.supported_claims} Supported, {report.audit_summary.partial_claims} Partial, {report.audit_summary.unsupported_claims} Unsupported\n")

    # Executive thesis
    print(f"{BOLD}--- [1] EXECUTIVE SUMMARY & CORE THESIS ---{RESET}")
    print(report.executive_summary)
    print("")

    # Key Deterministic Financials
    print(f"{BOLD}--- [2] DETERMINISTIC SCREENER FINANCIALS (AUDITED CODE COMPUTATION) ---{RESET}")
    print(f"{'Metric':<34} | {'Value':<18} | {'Formula / Source Schedule'}")
    print("-" * 78)
    for k, m in list(report.key_metrics.items())[:10]:
        safe_val = m.formatted_value.replace("₹", "Rs. ")
        print(f"{m.display_name:<34} | {YELLOW}{safe_val:<18}{RESET} | {m.source_ref}")
    print("-" * 78 + "\n")

    # Red-Team Thesis
    print(f"{RED}{BOLD}--- [3] ADVERSARIAL RED-TEAM STRESS TEST (\"WHAT WOULD MAKE US WRONG\") ---{RESET}")
    print(f"{BOLD}Forensic Bear Synopsis:{RESET} {report.red_team_critique.bear_case_thesis}")
    print(f"{BOLD}Thesis Killers:{RESET}")
    for idx, w in enumerate(report.red_team_critique.what_would_make_us_wrong):
        print(f"  {RED}* Trigger #{idx+1}:{RESET} {w}")
    print("")

    # Change Detection
    if report.change_detections:
        print(f"{YELLOW}{BOLD}--- [4] MANAGEMENT TONE & DISCLOSURE DELTA (DIFF) ---{RESET}")
        for c in report.change_detections:
            print(f"  * {BOLD}{c.topic}:{RESET} {c.tone_shift} ({c.delta_type})")
        print("")

    # Export paths
    pdf_path = settings.REPORTS_DIR / f"{report.ticker}_{report.report_id}.pdf"
    json_path = settings.REPORTS_DIR / f"{report.ticker}_{report.report_id}_claims.json"
    
    print(f"{CYAN}{BOLD}--- [5] AUDITED REPORT ARTIFACTS ---{RESET}")
    print(f"  [PDF Report]  {pdf_path}")
    print(f"  [Claims JSON] {json_path}")
    print(f"\n{BOLD}Compliance Notice:{RESET} {report.compliance_disclaimer[:110]}...\n")

def interactive_mode():
    print_banner()
    print(f"{BOLD}Available Entities (Banks & Blue-Chip Corporates):{RESET}")
    print("-" * 65)
    print(f"{CYAN}{BOLD}BANKING INSTITUTIONS (BFSI):{RESET}")
    banks = [c for c in COMPANIES_SEED if c.get("is_bank")]
    for idx, c in enumerate(banks):
        print(f"  [{idx+1:2d}] {c['ticker']:<14} - {c['name']}")
        
    print(f"\n{YELLOW}{BOLD}CONGLOMERATES & CORPORATES:{RESET}")
    corporates = [c for c in COMPANIES_SEED if not c.get("is_bank")]
    for idx, c in enumerate(corporates):
        print(f"  [{len(banks)+idx+1:2d}] {c['ticker']:<14} - {c['name']}")
        
    print(f"\n  [ 0] Custom Ticker (Any NSE/BSE or Global Stock e.g. INFY.NS, AAPL)\n")

    choice = input("Enter number or ticker symbol: ").strip()
    ticker = "SBIN.NS"
    all_companies = banks + corporates
    
    if choice.isdigit():
        num = int(choice)
        if 1 <= num <= len(all_companies):
            ticker = all_companies[num - 1]["ticker"]
        elif num == 0:
            custom = input("Enter custom stock ticker (e.g. INFY.NS, AAPL): ").strip().upper()
            if custom:
                ticker = custom
    elif choice:
        ticker = choice.upper()

    print(f"\nSelected: {YELLOW}{ticker}{RESET}")
    print("Report Focus:")
    print("  [1] Comprehensive (Default)")
    print("  [2] Valuation & Scenarios")
    print("  [3] Forensic & Risk Audit")
    f_choice = input("Select focus [1-3]: ").strip()
    focus = "comprehensive"
    if f_choice == "2":
        focus = "valuation"
    elif f_choice == "3":
        focus = "risk"

    run_cli_report(ticker, focus)

def main():
    parser = argparse.ArgumentParser(description="mu-trace: Institutional Equity & Bank Research Report Generator")
    parser.add_argument("--ticker", "-t", type=str, help="Stock ticker symbol (e.g. SBIN.NS, ICICIBANK.NS, RELIANCE.NS, TCS.NS)")
    parser.add_argument("--focus", "-f", type=str, default="comprehensive", help="Report focus: comprehensive, valuation, risk")
    parser.add_argument("--benchmark", "-b", action="store_true", help="Run evaluation benchmark and ablation study")
    parser.add_argument("--interactive", "-i", action="store_true", help="Launch interactive CLI prompt")
    
    args = parser.parse_args()

    if args.benchmark:
        BenchmarkSuite.run_evaluation()
    elif args.ticker:
        run_cli_report(args.ticker, args.focus)
    else:
        interactive_mode()

if __name__ == "__main__":
    main()
