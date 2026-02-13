#!/usr/bin/env python
"""
Example mock API server for testing the entity resolver.

Run this in one terminal:
    python examples/mock_api_server.py

Then in another terminal, test the CLI:
    resolve-entity COMPANY123
    resolve-entity TEST456 --api-url http://localhost:8080/api/resolve
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock database of company entity identifiers
MOCK_DATABASE = {
    "COMPANY123": {
        "resolved_identifier": "US-CORP-123456",
        "company_name": "Example Corporation",
        "status": "active"
    },
    "TEST456": {
        "resolved_identifier": "UK-LTD-789012",
        "company_name": "Test Limited",
        "status": "active"
    },
    "INACTIVE999": {
        "resolved_identifier": "DE-GMBH-111222",
        "company_name": "Inactive Company",
        "status": "inactive"
    }
}


@app.route('/api/resolve', methods=['POST'])
def resolve_identifier():
    """Resolve a company entity identifier."""
    data = request.get_json()
    
    if not data or 'identifier' not in data:
        return jsonify({"error": "Missing identifier"}), 400
    
    identifier = data['identifier']
    
    if identifier in MOCK_DATABASE:
        return jsonify(MOCK_DATABASE[identifier]), 200
    else:
        return jsonify({
            "error": "Identifier not found",
            "identifier": identifier
        }), 404


if __name__ == '__main__':
    print("Starting mock API server on http://localhost:8080")
    print("\nAvailable test identifiers:")
    for identifier in MOCK_DATABASE.keys():
        print(f"  - {identifier}")
    print("\nTest with: resolve-entity COMPANY123")
    app.run(host='0.0.0.0', port=8080, debug=True)
