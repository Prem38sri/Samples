# -*- coding: utf-8 -*-
import sys
import re

"""
Creating below data structure for holding all records named stocks of type dictionary -

{
	'2017-01-03': {
				'num_of_vcount': 6, 
				'last_quote_time': '16:29:59', 
				'most_act_hr': ['16', '16', '16', '16', '16', '16'], 
				'most_act_hr_count': '16', 
				'most_act_symbol': ['AAPL', 'AMD', 'AAPL', 'AMZN', 'AAPL', 'FB'], 
				'most_act_symbol_count': 'AAPL', 
				'strips': {
						'AAPL': {
								'lowprice': '140.64', 
								'highprice': '142.64', 
								'lasttradetime': '2017-01-03 16:28:50'}, 
						'AMD': {
								'lowprice': '13.86', 
								'highprice': '13.86', 
								'lasttradetime': '2017-01-03 16:25:22'}, 
						'AMZN': {
								'lowprice': '845.61', 
								'highprice': '845.61', 
								'lasttradetime': '2017-01-03 16:25:28'}, 
						'FB': {
								'lowprice': '140.34', 
								'highprice': '140.34', 
								'lasttradetime': '2017-01-03 16:29:59'}
				}
			}, 
	'2017-01-04': {
				'num_of_vcount': 1, 
				'last_quote_time': '16:29:32', 
				'most_act_hr': ['16'], 
				'most_act_hr_count': '16', 
				'most_act_symbol': ['AAPL'], 
				'most_act_symbol_count': 'AAPL', 
				'strips': {
						'AAPL': {
								'lowprice': '143.64', 
								'highprice': '143.64', 
								'lasttradetime': '2017-01-04 16:29:32'}
					}
			}
}
"""
stocks={} #Dictionary to hold values from all valid records
current_trading_day= 1990-00-00 # Default trading date, to compare with trading date of record and insert in DS
vcount=0 #valid count of records for a day

#variables to check if a record is valid, which should fall between starttime and endtime

starttime = 34200 #09H30M00S in seconds
endtime = 59400 #16H30M00S in seconds

#read records from command line(consider this approach for this test). Iterrate 1st row number times to check each record.
#validate record, if valid then create a key with date in DS stocks. 

try:
    num_of_quotes=input()
    num_of_quotes=int(num_of_quotes)
except ValueError:
    print("Not a valid Number of row")
    sys.exit(0)
    
#print(num_of_quotes)
for i in range(0,num_of_quotes):
    #read each record
    record=input()
    if not re.match("^\d{4}-\d{2}-\d{2},\d{2}:\d{2}:\d{2},[A-Z]+,[0-9]+\.[0-9]+$",record):
        print("record pattern is not valid,proceeding with next iteration")
        continue
    #print(record)
    #split
    date=record.split(',')[0]
    time=record.split(',')[1]
    hour=time.split(':')[0]
    mins=time.split(':')[1]
    secs=time.split(':')[2]
    symbol=record.split(',')[2]
    price=record.split(',')[3]
     
    totaltime = (int((hour[1] if hour.startswith('0') else hour)) * 3600 ) + (int((mins[1] if mins.startswith('0') else mins)) * 60 ) + int((secs[1] if secs.startswith('0') else secs))
    #print(totaltime)
    #proceed to insert data in stocs dictionary only if time falls in given range
    if ((totaltime >= starttime) and (totaltime <= endtime)):
        #comarison to reset valid count for a given date
        if current_trading_day != date:
            current_trading_day=date
            vcount=0
        # add a date as key in srocks dictionary if not exsist    
        if date not in stocks:
            stocks[date]={'num_of_vcount':"",'last_quote_time':"",'most_act_hr':[],'most_act_hr_count':"",'most_act_symbol':[],'most_act_symbol_count':"",'strips':{}}
        
        vcount = vcount + 1
        stocks[date]['num_of_vcount'] = vcount
        stocks[date]['last_quote_time'] = time
        stocks[date]['most_act_hr'].append(hour)
        stocks[date]['most_act_hr_count']=max(stocks[date]['most_act_hr'],key=stocks[date]['most_act_hr'].count)
        stocks[date]['most_act_symbol'].append(symbol)
        stocks[date]['most_act_symbol_count']=max(stocks[date]['most_act_symbol'],key=stocks[date]['most_act_symbol'].count)
       
        #Add strip if not available as key to nested dictionary strips, else add informations from record
        if symbol not in stocks[date]['strips']:
            stocks[date]['strips'][symbol] = {'lowprice':price,'highprice':price,'lasttradetime':date+" "+time}
            
        else:
            
            stocks[date]['strips'][symbol]['lowprice'] = (price if stocks[date]['strips'][symbol]['lowprice'] > price else stocks[date]['strips'][symbol]['lowprice'])
            stocks[date]['strips'][symbol]['highprice'] = (price if stocks[date]['strips'][symbol]['highprice'] < price else stocks[date]['strips'][symbol]['highprice'])
            stocks[date]['strips'][symbol]['lasttradetime']=date+" "+time

    #print(stocks)
    
#print("final dictionary snap")
#print(stocks)

"""
Print output in given template. 
We will iterate over each key of stocks dictionary which is a date.
"""
for key in sorted(stocks.keys()):
    print("Trading Day = "+key)
    print("Last Quote Time = "+stocks[key]['last_quote_time'])
    print("Number of valid quotes = "+str(stocks[key]['num_of_vcount']))
    print("Most active hour = "+stocks[key]['most_act_hr_count'])
    print("Most active symbol = "+stocks[key]['most_act_symbol_count'])
    for eachstrip in sorted(stocks[key]['strips'].keys()):
        #print(eachstrip)
        print(str(stocks[key]['strips'][eachstrip]['lasttradetime'])+','+eachstrip+','+stocks[key]['strips'][eachstrip]['highprice']+','+stocks[key]['strips'][eachstrip]['lowprice'])


"""
Sample output

Trading Day = 2017-01-03
Last Quote Time = 16:29:59
Number of valid quotes = 6
Most active hour = 16
Most active symbol = AAPL
2017-01-03 16:28:50,AAPL,142.64,140.64
2017-01-03 16:25:22,AMD,13.86,13.86
2017-01-03 16:25:28,AMZN,845.61,845.61
2017-01-03 16:29:59,FB,140.34,140.34
Trading Day = 2017-01-04
Last Quote Time = 16:29:32
Number of valid quotes = 1
Most active hour = 16
Most active symbol = AAPL
2017-01-04 16:29:32,AAPL,143.64,143.64

"""