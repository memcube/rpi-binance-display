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

Asset positions with EUR values under EUR_LIMIT
are not displayed in detail but are included
in the total value.

If you have more than 7 assets in your binance wallet
the value after UPDATES = is the amount of updates
of your assets after that the next page is diplayed.
On a Raspberry Pi 4 the time between 2 updates of the
display if you have 14 assets will be approximately
5 seconds. So if you write 5 after UPDATES = the time
after that the next page is displayed will 
be ~25 seconds.

By clicking anywhere in the display the program
will exit.
