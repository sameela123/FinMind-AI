import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from backend.agent_engine import FinMindAgentEngine

engine = FinMindAgentEngine()

class FinMindAPIHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_OPTIONS(self):
        self._send_json({"status": "OK"}, 200)

    def do_GET(self):
        if self.path in ['/', '/health']:
            self._send_json({
                "status": "HEALTHY",
                "service": "FinMind AI Multi-Agent Production API",
                "project_id": engine.project_id,
                "dataset_id": engine.dataset_id
            })
        elif self.path == '/api/audit':
            self._send_json(engine.run_expense_auditor())
        elif self.path == '/api/predict':
            self._send_json(engine.run_cash_flow_predictor())
        else:
            self._send_json({"error": "Endpoint not found"}, 404)

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body_bytes = self.rfile.read(content_length) if content_length > 0 else b'{}'
        try:
            body = json.loads(body_bytes.decode('utf-8'))
        except Exception:
            body = {}

        if self.path == '/api/audit':
            self._send_json(engine.run_expense_auditor())
        elif self.path == '/api/predict':
            self._send_json(engine.run_cash_flow_predictor())
        elif self.path == '/api/simulate':
            purchase = float(body.get("major_purchase", 0))
            expense_delta = float(body.get("monthly_expense_delta", 0))
            income_delta = float(body.get("income_delta", 0))
            self._send_json(engine.run_scenario_simulation(purchase, expense_delta, income_delta))
        elif self.path == '/api/advisor':
            prompt = body.get("prompt", "")
            self._send_json(engine.run_wealth_advisor(prompt))
        else:
            self._send_json({"error": "Endpoint not found"}, 404)

def run_server(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, FinMindAPIHandler)
    print(f"FinMind AI Production API listening on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    run_server(port)
