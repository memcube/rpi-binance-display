# rpi-binance-display
Displays the value of your Binance wallet and the assets in detail.

![BinanceDisplay](https://user-images.githubusercontent.com/84155543/118524970-ffa83080-b73e-11eb-8066-4b5ecd947da6.jpg)

Requirements:     
   os: Raspbian 10 Buster   
   packages: python3, lib-atlas-dev   
   python3 modules: python-binance, pandas   


All coins are calculated from the USDT market.
If you have coins in your wallet that have no USDT 
market on binance you should exclude them from USDT 
calculation using the comma separated BTC list in 
secret.cfg file (upper case letters).
Then they are calculated from the BTC market (also the 
24h ticker). Otherwise you will get a "Network Error" message. 
   
If you want to exclude some coins completely, configure
them with the comma separated list DEL in the config file.

Asset positions with EUR values below EUR_LIMIT
are not displayed explicitely, but are included
in the total value calculation.

On the screen 7 assets are displayed at one time.
If your Binance wallet includes more assets, BinanceDisplay 
will rotate through all the assets. The change frequency is
configured using the UPDATES value in secret.cfg. The value is
a counter for how many update loops the current assets are 
displayed. After that count the next 7 values are displayed. 
On a Raspberry Pi 4 one update loop takes approximately 5 sec.

A mouse click will exit the program.
