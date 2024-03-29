from datetime import datetime as dt
import json

class _CFH(object):
    def __init__(self):
        self.tick = {'cur_time' : [None],
        'bid1_price':None, 'bid1_qty':None,
        'ask1_price':None, 'ask1_qty':None
        }

        self.map = {
        '01' : ['bid1_price', 'bid1_qty'],
        '11' : ['ask1_price', 'ask1_qty']
        }

    def process(self, tick):
        
        try:
           
            cur_time = dt.fromtimestamp(float(tick['Time'])/1000)
            
            for t in tick['MDEntries']:

                no  = t['MDEntryPosNo']             
                bidask = t['MDEntryType']
                price = float(t['MDEntryPx'])
                key = bidask + no
                price_id, qty_id = self.map[key]

                self.tick['cur_time'] = cur_time
                self.tick[price_id] = price
                self.tick[qty_id] = 0

            return self.tick
                 
        except KeyError:
            return {}

       
class _CTP(object):

    def __init__(self):
        self.tick = {
        'cut_time' : None, 
        'exchange' : None,
        'commodity_type' : None,
        'commodity_no':None,
        'contract_no' : None,
        'last_price' : None,
        'bid_price' : None,
        'ask_price' : None,
        'total_qty' : 0,
        'last_qty' : None,
        'bid_qty' : None,
        'ask_qty' : None,
        }

    def process(self, tick, instrument):
        if tick != '':
            tick = tick.split(',')

            if tick[3] ==  instrument.upper():
                self.tick['cur_time'] = dt.strptime(tick[0], '%Y-%m-%d %H:%M:%S.%f')
                self.tick['exchange'] = tick[1]
                self.tick['commodity_type'] = tick[2]
                self.tick['commodity_no'] = tick[3]
                self.tick['contract_no'] = tick[4]
                self.tick['last_price'] = float(tick[10])
                self.tick['bid_price'] = float(tick[24])
                self.tick['ask_price'] = float(tick[26])
                self.tick['bid_qyt'] = int(tick[25])
                self.tick['ask_qty'] = int(tick[27])
                cur_total_qty = int(tick[27])
                if self.tick['total_qty'] != 0:
                    self.tick['last_qty'] = cur_total_qty - self.tick['total_qty']
                self.tick['total_qty'] = cur_total_qty

                return self.tick
            else:
                return {}
        else:
            return {}



def select_processor(exchange):
    exchange = exchange.upper()
    if exchange == 'CFH':
        obj = _CFH
    else:
        obj = _CTP
    
    class TickProcessor(obj):
        def __init__(self):
            super(TickProcessor, self).__init__()
    
    return TickProcessor()