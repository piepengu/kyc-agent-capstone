"""
KYC Bot: A Multi-Agent System for Automated KYC Compliance

This is the main entry point for the KYC Bot agent system.
It orchestrates a sequential multi-agent workflow using LangGraph to automate KYC compliance checks.
"""

import os
import argparse
from dotenv import load_dotenv
from graph import create_workflow, AgentState

# Load environment variables
load_dotenv()


def main():
    """Main entry point for the KYC Bot."""
    parser = argparse.ArgumentParser(description="KYC Bot - Automated KYC Compliance Agent")
    parser.add_argument("--name", type=str, required=True, help="Customer name to investigate")
    args = parser.parse_args()
    
    # Initialize state
    initial_state: AgentState = {
        "customer_name": args.name,
        "search_results": [],
        "watchlist_results": {},
        "final_report": "",
        "error": ""
    }
    
    print(f"🔍 Starting KYC investigation for: {args.name}")
    print("=" * 60)
    print()
    
    try:
        # Create and run the LangGraph workflow
        workflow = create_workflow()
        
        # Execute the workflow
        final_state = workflow.invoke(initial_state)
        
        # Display results
        print()
        print("=" * 60)
        print("✅ KYC investigation complete!")
        print("=" * 60)
        
        if final_state.get("error"):
            print(f"\n⚠️  Errors encountered: {final_state['error']}")
        
        print("\n📄 FINAL RISK ASSESSMENT REPORT:")
        print("-" * 60)
        print(final_state.get("final_report", "Report not generated"))
        print("-" * 60)
        
        # Summary statistics
        print("\n📊 Summary:")
        print(f"   - Search Results: {len(final_state.get('search_results', []))} items found")
        print(f"   - Watchlists Checked: {len(final_state.get('watchlist_results', {}).get('watchlists_checked', []))}")
        print(f"   - Watchlist Matches: {len(final_state.get('watchlist_results', {}).get('matches', []))}")
        
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

