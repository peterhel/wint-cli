# wint-cli
###### by Peter Helenefors
```
git clone git@github.com:peterhel/wint-cli.git

cd wint-cli

# Install dependencies
python3 setup.py develop --prefix ~/.local

python3 wint.py invoice list
```

Add the following environment variables if you don't want to pass you credentials each time you execute the command.

```
WINT_USERNAME=<username>
WINT_API_KEY=<apikey>
```

##### References
https://codeburst.io/building-beautiful-command-line-interfaces-with-python-26c7e1bb54df

http://superkollapi.wint.se/index.html

https://pypi.org/project/colorclass/

https://robpol86.github.io/terminaltables/

https://realpython.com/python-requests/#the-get-request

https://click.palletsprojects.com/en/7.x/quickstart/#nesting-commands
