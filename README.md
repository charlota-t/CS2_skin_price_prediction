#  CS2_skin_price_prediction

<a name="readme-top"></a>

### Table of Contents
<ol>
  <li>
    <a href="#about-the-project">About The Project</a>
  </li>
  <li>
    <a href="#prerequisites">Prerequisites</a>
  </li>
  <li><a href="#usage">Usage</a></li>
</ol>

## About The Project

This project aims to scrape skin prices from the Steam community market and then predict 
skin prices from the obtained data.


<p align="right">(<a href="#readme-top">back to top</a>)</p

## Prerequisities

All the required packages can be obtained by running pip install -r requirements.txt.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

The behaviour of the code can be changed trought the config file. If have_csv is set to False in USER config the script will scrape Steam Marketplace and Fandom for skin prices and generate a CSV file with all the data. This process takes around 3 hours so one CSV file is already provided in the utilities directory. 
Second mode gets selected by setting have_csv to True in USER config. Then the code predicts price for all 5 different coditions of a weapon according to these following atributes: Weapon type, Year of release and Quality which can all be chosen in the configuration file in the USER config.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
