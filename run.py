# Local Imports
from helpers import (
    get_hanary_hub_gas_prices,
    create_gas_prices_csv_file,
)



if __name__ == '__main__':
    """
        It is a main script which uses helper functions to scrape 
        daily and monthly gas prices and write data into files.
    """
    records = get_hanary_hub_gas_prices(
        'https://www.eia.gov/dnav/ng/hist/rngwhhdD.htm', 
        'daily'
    )
    create_gas_prices_csv_file(
        'daily_gas_price.csv',
        records,
        'daily'
    )

    records = get_hanary_hub_gas_prices(
        'https://www.eia.gov/dnav/ng/hist/rngwhhdM.htm', 
        'monthly'
    )
    create_gas_prices_csv_file(
        'monthly_gas_price.csv',
        records,
        'monthly'
    )
