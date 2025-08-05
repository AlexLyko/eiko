import click
from utils.smallfuncs import *
from  gis.gisserie import GisSerie
from  gis.reference import Reference
from  utils.eikofastapi import EikoFastApi
from utils.parsedclass import ParsedScenario

"""
The main script uses the CLI Click framework to allow dev and admin user to launch BASH or Powershell invites.
Such as :
python main.py fastapi -fp 8000 # to launch the FastAPI service locally
python main.py reference -fp ./tests/datasets/series/georef-france-commune-millesime.shp -k key -ke "dep_code+'_'+com_code" -v df_val -ve "com_name_lo" -rv 2022 # to build a quite elaborated shp reference from a local file

"""
@click.command()
@click.option("-fp", "--file_path", help="Datasource file path")
@click.option("-k", "--key", help="Key name, for data imports")
@click.option("-v", "--value_name", help="Defaut value name, for data imports")
@click.option("-ke", "--key_expression", help="Expression to evaluate, to use it as a key")
@click.option("-ve", "--value_expression", help="Expression to evaluate, to use it as default value")
@click.option("-rv", "--reference_version", help="For references, some reference of a version to load. Can be a year, an id... if -rvf is not set, -rv will try to set the best format.")
@click.option("-rvf", "--reference_version_format", help="For references, format of the reference. Between date, year or string.")
@click.option("-ap", "--api_port", help="Fast API listening port")
@click.option("-ah", "--api_host", help="Fast API host")
@click.option("-sc", "--scenario", help="JSON scenario path")
@click.argument('arg') # is the command
def cli_test(arg,
             file_path, key, value_name, key_expression, value_expression, 
             reference_version, reference_version_format,
             api_port, api_host, 
             scenario):
    match arg :
        case "gis_serie": # Will try to build a GisSerie dataset
            gis_serie = GisSerie(file_path, value_name, key_expression , value_expression)
            if value_name is not None : gis_serie.log_data(10, value_name)
            else: gis_serie.log_data(10)
        case "reference": # Will try to build a Reference in GIS family dataset
            reference = Reference(file_path,reference_version, key, value_name, key_expression , value_expression, reference_version_format)
            if value_name is not None : reference.log_data(10, value_name)
            else: reference.log_data(10)
        case "api": # Will launch the api in production mode (for dev mode, check for efastapi.py file)
            EikoFastApi().run(api_port, api_host)
        case "scenario": # Will launch the JSON scenario parser
            ParsedScenario(scenario)


if __name__ == "__main__":
    cli_test()