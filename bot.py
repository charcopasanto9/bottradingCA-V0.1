from kucoin.client import Market, Trade
import time
from config import API_KEY, API_SECRET, API_PASSPHRASE

# Configuración del bot
market_client = Market()
trade_client = Trade(API_KEY, API_SECRET, API_PASSPHRASE)

symbol = 'DOGE-USDT'  # Par de trading
investment = 50       # Monto inicial (en USDT)
take_profit = 0.02    # 2% de ganancia
stop_loss = 0.01      # 1% de pérdida

def get_price():
    """Obtener el precio actual del mercado."""
    ticker = market_client.get_ticker(symbol)
    return float(ticker['price'])

def place_order(order_type, amount):
    """Coloca una orden en el mercado."""
    try:
        if order_type == 'buy':
            return trade_client.create_market_order(symbol, 'buy', funds=amount)
        elif order_type == 'sell':
            return trade_client.create_market_order(symbol, 'sell', size=amount)
    except Exception as e:
        print(f"Error al colocar orden: {e}")

def run_bot():
    """Ejecuta el bot de trading."""
    balance = investment  # Saldo inicial
    while True:
        try:
            # Obtener precio actual
            price = get_price()
            print(f"Precio actual de {symbol}: {price}")

            # Calcular cantidad a comprar
            amount = balance / price

            # Comprar
            place_order('buy', balance)
            print(f"Comprado {amount} de {symbol} a {price}")

            # Monitorear el precio para TP/SL
            target_price = price * (1 + take_profit)
            stop_price = price * (1 - stop_loss)
            print(f"Esperando objetivo: {target_price}, Stop Loss: {stop_price}")

            while True:
                current_price = get_price()
                if current_price >= target_price:
                    place_order('sell', amount)
                    print(f"Ganancia alcanzada. Vendido a {current_price}")
                    break
                elif current_price <= stop_price:
                    place_order('sell', amount)
                    print(f"Pérdida alcanzada. Vendido a {current_price}")
                    break

            time.sleep(10)

        except Exception as e:
            print(f"Error en el bot: {e}")
            time.sleep(10)

# Inicia el bot
if __name__ == "__main__":
    run_bot()
