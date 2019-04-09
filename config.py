class TRACE_OPTS:
    MONTHLY_RETURN = {
            'name': 'Monthly Return',
            'type': 'bar',
            'yaxis': 'y4',
            'side': 'left',
            'position': 0.3
            }
    VOLATILITY = {
            'name': 'Volatility',
            'type': 'line',
            'yaxis': 'y3',
            'side': 'right',
            'position': 0.45
            }
    DRAWDOWN = {
            'name': 'Drawdown',
            'type': 'line',
            'yaxis': 'y2',
            }
    PRICE = {
            'name': 'Price',
            'type': 'line',
            'yaxis': 'y1',
            'side': 'left',
            'position': 0.15
            }

class AXIS_CONFIG:
    BASE = {
            'xaxis': {
                'domain': [0.1, 0.9]
                },
            'yaxis': {
                'title': 'Price'
                },
            'yaxis2': {
                'title': 'Drawdown' ,
                'overlaying': 'y',
                'side': 'left',
                'position': 0.05
                },
            'yaxis3': {
                'title': 'Volatility',
                'overlaying': 'y',
                'side': 'right'
                },
            'yaxis4': {
                'title': 'Monthly Return',
                'overlaying': 'y',
                'side': 'right',
                'position': 0.95
                }
            }
