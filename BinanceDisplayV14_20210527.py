
import pygame
from binance.client import Client
import pandas as pd
import configparser
import math
import datetime

pygame.init()
 
black = (0, 0, 0)
grey = (250, 250, 250)
white = (255, 255, 255)
green = (0, 200, 0)
blue = (0, 0, 200)
red = (200, 0, 0)
orange = (255, 150, 0)

config = configparser.ConfigParser()
config.read_file(open('secret.cfg'))
api_key = config.get('BINANCE', 'API_KEY')
secret_key = config.get('BINANCE', 'SECRET_KEY')
coinlist_btc = config.get('COINS', 'BTC') 
coinlist_btc = list(map(str, coinlist_btc.split(',')))
coinlist_del = config.get('COINS', 'DEL') 
coinlist_del = list(map(str, coinlist_del.split(',')))
limit = float(config.get('COINS', 'EUR_LIMIT')) 
X = int(config.get('RESOLUTION', 'X'))
Y = int(config.get('RESOLUTION', 'Y'))
FS = config.get('RESOLUTION', 'FULLSCREEN')
updates = int(config.get('RESOLUTION', 'UPDATES')) + 1

font1 = pygame.font.Font('freesansbold.ttf', int(X/16))
font2 = pygame.font.Font('freesansbold.ttf', int(X/26.66))
font3 = pygame.font.Font('freesansbold.ttf', int(X/7.5))
font4 = pygame.font.Font('freesansbold.ttf', int(X/32))
font5 = pygame.font.Font('freesansbold.ttf', int(X/10.959))

client = Client(api_key, secret_key)
pd.set_option('float_format', '{:f}'.format)

btc_df = pd.DataFrame()
del_df = pd.DataFrame()


def grab_binance_balance():
	global btc_df
	global coinlist_btc
	global coinlist_del
	
	btc_df = pd.DataFrame()
	account = client.get_account()
	balance_df = pd.DataFrame(account['balances'])
	
	for index, row in balance_df.iterrows():
		if float(row['free']) < 0.00000001:
			balance_df.drop(index, inplace=True)

	if coinlist_btc != ['']:
		for i in coinlist_btc:
			btc_df = btc_df.append(balance_df[balance_df['asset']==i])
			balance_df = balance_df[balance_df['asset']!=i]
		btc_df['asset'] = btc_df['asset'].astype(str) + 'BTC'
		btc_df['free'] = btc_df['free'].astype(float) + btc_df['locked'].astype(float)
		btc_df.set_index('asset', inplace=True)
		btc_df = btc_df.drop('locked' , axis=1)

	if coinlist_del != ['']:
		for i in coinlist_del:
			balance_df = balance_df[balance_df['asset']!=i]		

	balance_df['asset'] = balance_df['asset'].astype(str) + 'USDT'	
	balance_df['free'] = balance_df['free'].astype(float) + balance_df['locked'].astype(float)
	balance_df.set_index('asset', inplace=True)
	balance_df = balance_df.drop('locked' , axis=1)
	return balance_df


def grab_usdt():
	prices = client.get_symbol_ticker(symbol='EURUSDT')
	usdt_df =pd.DataFrame(prices, index=[0])  
	usdt_df= float(usdt_df['price'])
	usdt_df = 1 / usdt_df
	return usdt_df


def grab_prices():
	global btc_df
	global asset_df
	global coinlist_btc
	usdt_value = grab_usdt()
	asset_df = pd.DataFrame()
	asset_df = grab_binance_balance()
	price_df = pd.DataFrame()
	for index, row in asset_df.iterrows():
		price_df = client.get_ticker(symbol=index)
		asset_df.at[index, 'Price_USDT'] = price_df['lastPrice']
		asset_df.at[index, '24h'] = price_df['priceChangePercent']
	
	if coinlist_btc != ['']:
		grab_prices_btc()
		asset_df = pd.concat([asset_df, btc_df])
	
	asset_df[['Price_USDT', 'free']] = asset_df[['Price_USDT', 'free']].astype(float)	
	asset_df['USDT'] = asset_df['Price_USDT']*asset_df['free']
	asset_df['EUR'] = asset_df['USDT'].multiply(float(usdt_value))
	asset_df['Price_EUR'] = asset_df['Price_USDT'].multiply(float(usdt_value))	
	return asset_df
	

def grab_prices_btc():
	global btc_df
	prices_btc = pd.DataFrame()
	btc_price_df = pd.DataFrame()
	for index, row in btc_df.iterrows():
		btc_price_df = client.get_ticker(symbol=index)
		btc_df.at[index, 'Price_BTC'] = btc_price_df['lastPrice']
		btc_df.at[index, '24h'] = btc_price_df['priceChangePercent']
	prices_btc = client.get_symbol_ticker(symbol='BTCUSDT')
	btc_usdt = pd.DataFrame(prices_btc, index=[0])  
	btc_usdt= float(btc_usdt['price'])

	btc_df['expand'] = btc_df.index
	btc_df['expand'] = btc_df['expand'].astype(str) + 'U'

	btc_df.set_index('expand', inplace=True)

	btc_df[['Price_BTC', 'free']] = btc_df[['Price_BTC', 'free']].astype(float)	
	btc_df['Price_USDT'] = btc_df['Price_BTC'].multiply(float(btc_usdt))
	btc_df = btc_df.drop('Price_BTC' , axis=1)
	
	columnsTitles=["free","Price_USDT","24h"]
	btc_df=btc_df.reindex(columns=columnsTitles)
	return btc_df


def eur_btc():
	prices = client.get_symbol_ticker(symbol='BTCEUR')
	eurbtc_df =pd.DataFrame(prices, index=[0])  
	eurbtc_df= float(eurbtc_df['price'])
	return eurbtc_df

	
def headlines():
	logo = pygame.image.load('bitcoin.png')
	logo = pygame.transform.scale(logo, (X // 10, X // 10))
	texte = font1.render('BINANCE Wallet', True, green, None)
	texteRect = texte.get_rect()
	texteRect.center = (X // 2, Y // 16)
	display_surface.blit(logo, (X // 80, X // 80))
	display_surface.blit(texte, texteRect)
	
	Yup = int (Y / 2.42)
	headl = ['Asset','Value','Price','EUR','%24h']
	pos = [int(X / 9.8),int(X / 2.66),int(X / 1.569),int(X / 1.194),int(X / 1.017)]
	for i,x in zip(headl,pos): 
		textup = font4.render(i, True, orange, None)
		textRectup = textup.get_rect()
		textRectup.topright = (x, Yup)
		display_surface.blit(textup, textRectup)
	return
	
	
def error():
		text = font5.render('CONNECTION ERROR', True, black, red)
		textRect = text.get_rect()
		textRect.center = (X // 2, int(Y / 1.778))
		display_surface.blit(text, textRect)
		pygame.display.update()
		for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					pygame.display.quit()
					pygame.quit()
					exit()
		return
	
		
def draw():
		global valueeur
		global asset_df
		global running
		
		back = pygame.image.load('back.jpg')
		back = pygame.transform.scale(back, (X, Y))
		display_surface.blit(back, (0, 0))
		
		now = datetime.datetime.now()
		timeval = now.strftime('%H:%M:%S')
		timeval = font2.render(timeval, True, grey, None)
		timevalRect = timeval.get_rect()
		timevalRect.topright = (int(X/1.015), int(Y/48))
		display_surface.blit(timeval, timevalRect)
		
		texteur = font3.render('€ %.2f' % (valueeur), True, grey, None)
		texteurRect = texteur.get_rect()
		texteurRect.center = (X // 2, int(Y/4.3))
		display_surface.blit(texteur, texteurRect)
		eurbtc = eur_btc()
		valuebtc = valueeur / eurbtc
		texteur = font2.render('BTC %.8f' % (valuebtc), True, grey, None)
		texteurRect = texteur.get_rect()
		texteurRect.center = (X // 2, int(Y/2.8))
		display_surface.blit(texteur, texteurRect)
		
		p = int(Y/2.087)                                         
		for index, row in asset_df.iterrows():
			value = index[:-4]
			value = value[0:5]
			text = font2.render(str(value), True, grey, None)
			textRect = text.get_rect()
			textRect.topleft = (int(X / 61.54), p)
			display_surface.blit(text, textRect)
			p = p + int(Y/13.714)
			
		p = int(Y/2.087)
		for index, row in asset_df.iterrows():
			value = row['free']
			value = round(value,6)
			text = font2.render(str(value), True, grey, None)
			textRect = text.get_rect()
			textRect.topright = (int(X / 2.66), p)
			display_surface.blit(text, textRect)
			p = p + int(Y/13.714)
			
		p = int(Y/2.087)
		for index, row in asset_df.iterrows():
			value = row['Price_EUR']
			value = round(value,4)
			text = font2.render('%.4f' % (value), True, grey, None)
			textRect = text.get_rect()
			textRect.topright = (int(X / 1.569), p)
			display_surface.blit(text, textRect)
			p = p + int(Y/13.714)
					
		p = int(Y/2.087)
		for index, row in asset_df.iterrows():
			value = row['EUR']
			value = round(value,2)
			text = font2.render('%.2f' % (value), True, grey, None)
			textRect = text.get_rect()
			textRect.topright = (int(X / 1.194), p)
			display_surface.blit(text, textRect)
			p = p + int(Y/13.714)
				
		p = int(Y/2.087)
		for index, row in asset_df.iterrows():
			value = row['24h']
			value = round(float(value),2)
			if value >= 0:
				text = font2.render('%.2f' % (value), True, green, None)
			else:
				text = font2.render('%.2f' % (value), True, red, None)
					
			textRect = text.get_rect()
			textRect.topright = (int(X / 1.017), p)
			display_surface.blit(text, textRect)
			p = p + int(Y/13.714)
		
		headlines()
				
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				running = False	
		
		pygame.display.update()
		return
	
	
def main():
	global running
	global valueeur	
	global asset_df
	global limit
	global updates
	
	a=0
	b=7
	running = True
	while running:
		try:
					
			c = 1
			while c < updates and running:
				asset_df = grab_prices()
				valueeur = asset_df['EUR'].sum()
				valueeur = round(valueeur, 2)
				for index, row in asset_df.iterrows():
					if float(row['EUR']) < limit:
						asset_df.drop(index, inplace=True)
				dfcount = asset_df.shape[0]
				asset_df = asset_df.iloc[a:b]
				draw()
				c += 1 
		
			if (dfcount-b-7) > 0:
				a += 7
				b += 7
			else: 
				if b >= dfcount:
					a=0
					b=7
				else:
					b=dfcount
					a=dfcount-7
		
	
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					running = False	
		except:
			error()
				
	pygame.display.quit()
	pygame.quit()
	exit()
	return
	
if FS == 'True':
	display_surface = pygame.display.set_mode((X, Y), pygame.FULLSCREEN, 32)
else:
	display_surface = pygame.display.set_mode((X, Y))

pygame.display.set_caption('Binance')
pygame.mouse.set_visible(False)
main()	


