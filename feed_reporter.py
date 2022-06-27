import requests
from datetime import datetime, timedelta
import os
from configutils import ConfigUtils

BASE_URL = "https://api.intel471.com/v1/cve/reports"

CONFIG_DIR = '/config'
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
	for cve in updated_cves:
		cve_name = cve["data"]["cve_report"]["name"]
		cve_type = cve["data"]["cve_report"]["cve_type"]
		product = cve["data"]["cve_report"]["product_name"]
		poc_observed = cve["data"]["cve_report"]["poc"] == "observed"
		print(f"{cve_name} - product: {product}, type: {cve_type}, poc: {poc_observed}")

if __name__ == '__main__':
	main()