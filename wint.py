import click
import requests
import json
from pygments import highlight, lexers, formatters
from colorclass import Color, Windows
from terminaltables import SingleTable
from sys import exit

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

def printRaw(jsondata):
    if (_raw):
        print(highlight(json.dumps(jsondata, indent=4), lexers.JsonLexer(), formatters.TerminalFormatter()))
        exit()

def fetch(url, **kwargs):
    response = requests.get(url, **kwargs)
    jsondata = json.loads(response.text)
    printRaw(jsondata)
    return jsondata

@click.group()
@click.option('--username', required = True)
@click.option('--api_key', required = True)
@click.option('--raw', is_flag=True, default=False)
def main(username, api_key, raw):
    global _username, _api_key, _raw
    _username = username
    _api_key = api_key
    _raw = raw

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
    print('not implemented')

@incominginvoice.command()
@click.option('--bg', required = True)
@click.option('--orgnr', required = True)
@click.option('--amount', required = True)
@click.option('--vat', required = True)
def add():
    print('implement')

@receipt.command()
def list():
    global _username
    global _api_key
    
    jsondata = fetch('https://superkollapi.wint.se/api/Receipt?OrderByProperty=Id&OrderByDescending=true', auth=(_username, _api_key))

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
    jsondata = fetch('https://superkollapi.wint.se/api/IncomingInvoice?OrderByProperty=DueDate&OrderByDescending=true', auth=(_username, _api_key))


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

if __name__ == "__main__":
    main(auto_envvar_prefix='WINT')