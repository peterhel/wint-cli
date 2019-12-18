import click
import requests
import json
from colorclass import Color, Windows
from terminaltables import SingleTable

stateCols = {
	1: 'autoblue',
	7: 'autogreen',
	8: 'autobggreen'
}

def beginColor(state):
	global stateCols
	color = stateCols.get(state) or 'autowhite'
	return '{' + color + '}'
	# Color('{autogreen}<10ms{/autogreen}')

def endColor(state):
	global stateCols
	color = stateCols.get(state) or 'autowhite'
	return '{/' + color +'}'

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

@main.group()
def receipt():
	pass

@main.group()
def incominginvoice():
	pass

@receipt.command()
def add():
	print('implement')

@receipt.command()
def list():
	global _username
	global _api_key
	
	response = requests.get('https://superkollapi.wint.se/api/Receipt?OrderByProperty=Id&OrderByDescending=true', auth=(_username, _api_key))
	jsondata = json.loads(response.text)

	data = [['Id', 'DateTime', 'PaymentMethodName', 'CategoryName', 'Amount']]
	for item in jsondata['Items']:
		data.append([item['Id'], item['DateTime'], item['PaymentMethodName'], item['CategoryName'], f"{int(round(item['Amount'], 0))} {item['Currency']}"])

	tabledata = SingleTable(data, 'Receipts')
	tabledata.justify_columns[4] = 'right'
	print(tabledata.table)

@incominginvoice.command()
def list():
	global _username
	global _api_key

	# 8: skickad för betalning. 7: betald, 1: bokförs
	response = requests.get('https://superkollapi.wint.se/api/IncomingInvoice?OrderByProperty=DueDate&OrderByDescending=true', auth=(_username, _api_key))
	jsondata = json.loads(response.text)

	data = [['DueDate', 'State', 'Supplier', 'Amount']]
	for item in jsondata['Items']:
		data.append( [Color(beginColor(item['State']) + item['DueDate'] + endColor(item['State'])), item['State'], item['Supplier']['Name'], f"{int(round(item['Amount'], 0))} {item['Currency']}"])

	tabledata = SingleTable(data, 'Incoming Invoices')
	tabledata.justify_columns[3] = 'right'
	print(tabledata.table)

@invoice.command()
def list():
	global _username
	global _api_key
	
	response = requests.get('https://superkollapi.wint.se/api/Invoice?OrderByProperty=SerialNumber&OrderByDescending=true', auth=(_username, _api_key))
	jsondata = json.loads(response.text)

	data = [['#', 'Date', 'OCR']]
	for item in jsondata['Items']:
		data.append([item['SerialNumber'], item['PostingDate'], item['Ocr']])

	tabledata = SingleTable(data, 'Invoices')
	print(tabledata.table)

if __name__ == "wint":
	main(auto_envvar_prefix='WINT')