# Web-Scraper using TCP
Client-server based web-scraping application that works on TCP.

## App description
There are two roles: client and server. The client sends the url address to the server, then the number of the images and the leaf paragraphs in the url (web page) are counted in the server part and sent to the client as a response.

## Installation
In terminal, enter:
```bash
https://github.com/TarlanOmarbayli/Web-Scraper-TCP
```
Then, install requirements by entering
```bash
pip install -r requirements.txt
```
## Usage
In the Server terminal:
```bash
python3 web_scraper.py server
```
Pressing ```Ctrl+C``` will stop the terminal

In the Client terminal:
```bash
python3 web_scraper.py client {-p} {url address}
```
Example: ```python3 web_scraper.py client -p www.pcworld.com```

#### Note

Pre-defined hostname is ```127.0.0.1``` and port number is ```4488```
