# rpi-binance-display
Displays the value of your Binance wallet and the assets in detail.

![BinanceDisplay](https://user-images.githubusercontent.com/84155543/118524970-ffa83080-b73e-11eb-8066-4b5ecd947da6.jpg)

Requirements:     
   os: Raspbian 10 Buster   
   packages: python3, lib-atlas-dev   
   python3 modules: python-binance, pandas   


All coins are calculated from the USDT market.
If you have coins in your wallet that have no USDT 
market on binance you should write them in the
secret.cfg file (behind BTC =) as comma separated 
string in upper case letters. Otherwise you will get
the error message "Network Error".   
   
If you have coins you want to exclude from being
calculated and displayed you may write them behind
DEL = as comma separated string.
