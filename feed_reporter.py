import requests
from datetime import datetime, timedelta
import os
from configutils import ConfigUtils
from slack_sdk.webhook import WebhookClient

BASE_URL = "https://api.intel471.com/v1/cve/reports"

CONFIG_DIR = '/app/config'
CONFIG_FILE = f'{CONFIG_DIR}/config.yaml'

def getUpdatedCves(username, password, time_back = "2days"):
	resp = requests.get(f"{BASE_URL}?lastUpdatedFrom={time_back}&riskLevel=high&count=100", auth=(username, password))
	if resp.json()['cveReportsTotalCount'] == 0:
		return {}
	else:
		return resp.json()['cveReports']

def main():
	cfg = ConfigUtils(sources=[{'name': 'consul',
                                'uri': os.getenv('CONSUL_URI', '127.0.0.1'),
                                'token': os.getenv('CONSUL_TOKEN'),
                                'env': '/'.join(['cluster', os.getenv('ENV_NAMESPACE')])},
                               {'name': 'env'}],
                      schemas=[CONFIG_FILE,])
	config = cfg.load_config()

	updated_cves = getUpdatedCves(config.get("intel471_username"), config.get("intel471_password"))
	text_to_send = f"CVEs updated in the last 48h: {len(updated_cves)}\n\n"

	for cve in updated_cves:
		cve_name = cve["data"]["cve_report"]["name"]
		cve_type = cve["data"]["cve_report"]["cve_type"]
		product = cve["data"]["cve_report"]["product_name"]
		poc_observed = cve["data"]["cve_report"]["poc"] == "observed"
		text_to_send += f"{cve_name} - product: {product}, type: {cve_type}, poc observed: {poc_observed}\n"
	
	webhook = WebhookClient(config.get("intel471_slack_webhook"))
	webhook.send(text=text_to_send)

if __name__ == '__main__':
	main()