import requests
from datetime import datetime, timedelta
import os

BASE_URL = "https://api.intel471.com/v1/cve/reports"
AUTH=(os.environ["INTEL471_USERNAME"], os.environ["INTEL471_PASSWORD"])

def getUpdatedCves(time_back = "2days"):
	resp_count = requests.get(f"{BASE_URL}?lastUpdatedFrom={time_back}&riskLevel=high", auth=AUTH)
	count = resp_count.json()["cveReportsTotalCount"]
	resp = requests.get(f"{BASE_URL}?lastUpdatedFrom={time_back}&riskLevel=high&count={count}", auth=AUTH)
	return resp.json()['cveReports']

def main():
	updated_cves = getUpdatedCves("5days")
	for cve in updated_cves:
		cve_name = cve["data"]["cve_report"]["name"]
		cve_type = cve["data"]["cve_report"]["cve_type"]
		product = cve["data"]["cve_report"]["product_name"]
		poc_observed = cve["data"]["cve_report"]["poc"] == "observed"
		print(f"{cve_name} - product: {product}, type: {cve_type}, poc: {poc_observed}")

if __name__ == '__main__':
	main()