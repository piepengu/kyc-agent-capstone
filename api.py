"""
REST API server for KYC Bot.

This module provides HTTP endpoints for running KYC investigations.
Can be deployed to Cloud Run or run locally.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import traceback
from typing import Dict, Any
from graph import create_workflow, AgentState
from logger import workflow_logger

app = Flask(__name__)
# Enable CORS for all routes
CORS(app)

# Configure logging
import logging
logging.basicConfig(level=logging.INFO)


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "KYC Bot",
        "version": "1.0.0"
    }), 200


@app.route('/api/v1/investigate', methods=['POST'])
def investigate():
    """
    Run KYC investigation for a customer.
    
    Request body:
    {
        "customer_name": "John Doe"
    }
    
    Response:
    {
        "customer_name": "John Doe",
        "search_results": [...],
        "watchlist_results": {...},
        "final_report": "...",
        "risk_level": "LOW|MEDIUM|HIGH",
        "execution_time": 8.5,
        "error": ""
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        customer_name = data.get('customer_name')
        
        if not customer_name:
            return jsonify({"error": "customer_name is required"}), 400
        
        # Validate customer name
        from error_handling import validate_customer_name
        is_valid, error_msg = validate_customer_name(customer_name)
        if not is_valid:
            return jsonify({"error": f"Invalid customer name: {error_msg}"}), 400
        
        # Run investigation
        workflow_logger.info(f"API request received for: {customer_name}")
        
        # Create workflow and run investigation
        workflow = create_workflow()
        initial_state: AgentState = {
            "customer_name": customer_name.strip(),
            "search_results": [],
            "watchlist_results": {},
            "final_report": "",
            "error": ""
        }
        
        # Start performance tracking
        from logger import performance_tracker
        performance_tracker.start_investigation(customer_name)
        
        try:
            final_state = workflow.invoke(initial_state)
            performance_tracker.end_investigation()
        except Exception as e:
            performance_tracker.end_investigation()
            raise
        
        # Extract risk level from report
        risk_level = "UNKNOWN"
        report = final_state.get("final_report", "")
        if "Risk Level:" in report or "risk level:" in report.lower():
            import re
            risk_match = re.search(r'Risk Level[:\s]+(LOW|MEDIUM|HIGH)', report, re.IGNORECASE)
            if risk_match:
                risk_level = risk_match.group(1).upper()
        
        response = {
            "customer_name": final_state.get("customer_name", customer_name),
            "search_results": final_state.get("search_results", []),
            "watchlist_results": final_state.get("watchlist_results", {}),
            "final_report": final_state.get("final_report", ""),
            "risk_level": risk_level,
            "error": final_state.get("error", "")
        }
        
        workflow_logger.info(f"API request completed for: {customer_name}, risk_level: {risk_level}")
        
        return jsonify(response), 200
        
    except Exception as e:
        error_msg = f"Error processing request: {str(e)}"
        workflow_logger.error(f"API error: {error_msg}\n{traceback.format_exc()}")
        return jsonify({
            "error": error_msg,
            "customer_name": data.get('customer_name', '') if data else ''
        }), 500


@app.route('/api/v1/metrics', methods=['GET'])
def metrics():
    """Get service metrics."""
    # This would typically query a metrics database
    # For now, return basic info
    return jsonify({
        "service": "KYC Bot",
        "version": "1.0.0",
        "status": "operational"
    }), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    # Get port from environment variable or default to 8080
    port = int(os.environ.get('PORT', 8080))
    
    # Run Flask app
    app.run(host='0.0.0.0', port=port, debug=False)

