# real estate crowdfunding scraper

A Python-based web scraper built with Scrapy to collect real estate crowdfunding project data from multiple platforms. This tool helps investors and analysts gather information about available real estate crowdfunding opportunities across different platforms.

## Features

[!NOTE]
> This project is a work in progress and the data is not yet fully reliable.
> Working to add more platforms and fields to the output.

- Scrapes data from multiple real estate crowdfunding platforms:
  - [Urbanitae](https://urbanitae.com)
  - [Wecity](https://wecity.com)
- Combines data from all platforms into a single CSV file
- Removes duplicate listings
- Provides detailed project information including:
  - Project title
  - Location (city, region, address)
  - Investment terms (total return, term in months)
  - Business model
  - Project status
  - Project URL

## Output

```csv
platform,title,city,region,address,status,total_return,term_months,business_model,url
Urbanitae,Burgos | Arlanzón Commercial Park Project,Burgos,Burgos,"C. de la Ventosa, 09001 Burgos",POST_STUDY,16.87%,18,LENDING,https://urbanitae.com/es/proyectos/P000347
Urbanitae,Barcelona | Catalonia,Barcelona,Cataluña,Barcelona,IN_STUDY,,0,SOLD,https://urbanitae.com/es/proyectos/P000199
Urbanitae,Madrid | Madrid,Madrid,Madrid,Madrid,IN_STUDY,0,0,RENT,https://urbanitae.com/es/proyectos/P000268
Urbanitae,Mallorca | Balearic Islands,Sevilla,Andalucía,Sevilla,IN_STUDY,,,SOLD,https://urbanitae.com/es/proyectos/P000174
Urbanitae,France | Paris,París,París,París,IN_STUDY,0,0,LENDING,https://urbanitae.com/es/proyectos/P000267
Urbanitae,Portugal | Lisbon,Lisboa,Lisboa,Lisboa,IN_STUDY,0, ,SOLD,https://urbanitae.com/es/proyectos/P000149
Wecity,Marbella,Marbella,,,En estudio,12.00,12,Préstamo,https://www.wecity.com/oportunidades/marbella/
Wecity,Madrid,Madrid,,,En estudio,0.00,0,Préstamo,https://www.wecity.com/oportunidades/madrid-5/
Wecity,Cádiz,Cádiz,,,En estudio,0.00,0,Préstamo,https://www.wecity.com/oportunidades/cadiz/
```

## Requirements

- python `>=3.13`
- pipenv (for dependency management)
- scrapy `>=2.12.0`

## Installation

1. Clone the repository

```bash
git clone <repository-url>
cd scrapy-real-state-crowdfunding
```

2. Create and activate a virtual environment using Pipenv

```bash
pipenv install
pipenv shell
```

## Usage

Run the scraper with

```bash
python real_state_scraper/main.py
```

The script will:

1. Remove any existing CSV files from previous runs
2. Scrape data from each platform
3. Combine the results into a single CSV file named `real_estate_crowdfunding.csv`

## Output Format

The final CSV file (`real_estate_crowdfunding.csv`) contains the following columns:

- `platform`: name of the crowdfunding platform
- `title`: project title
- `city`: project location (city)
- `region`: project location (region)
- `address`: project address
- `status`: current project status
- `total_return`: expected total return
- `term_months`: investment term in months
- `business_model`: type of business model
- `url`: project url
