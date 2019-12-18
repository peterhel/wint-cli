import click
import requests
import json
from terminaltables import AsciiTable

@click.group()
@click.option('--username', required = True)
@click.option('--api_key', required = True)
def main(username, api_key):
	global _username, _api_key
	_username = username
	_api_key = api_key

@main.group()
def invoice():
	pass

@invoice.command()
def list():
	global _username
	global _api_key
	
	response = requests.get('https://superkollapi.wint.se/api/Invoice', auth=(_username, _api_key))
	jsondata = json.loads(response.text)

	data = [['#', 'OCR']]
	for item in jsondata['Items']:
		data.append([item['SerialNumber'], item['Ocr']])

	tabledata = AsciiTable(data)
	print(tabledata.table)

if __name__ == "wint":
	main(auto_envvar_prefix='WINT')