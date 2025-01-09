# Crypto Alert Tool 🚀

Alert tool for cryptocurrency trading who monitors the market of BTC/USDT and send notification via email and whatsApp when an important technical signal is detected, the tool monitorizes each minute, when a signal of sell or buy is detected based on the parameters.

## 📋 Features

- Real time monitor of BTC/USDT in Binance
- Tech analisys using:
  - EMAs (Exponential Moving Averages)
  - RSI (Relative Strength Index)
- Automatic signal detection:
  - Golden Cross (bullish signal)
  - Death Cross (bearish signal)
- Notifications by:
  - Email (with graphics attached)
  - WhatsApp
- Technical chart generation using matplotlib

## 🔧 Requirements

- Python 3.7+
- Binance account with API key and Secret key
- Gmail account
- Twillio account for messaging to whatsapp(requires a premiun subscription in twillio)

## 📦 Dependencies
- python: Programming language used to develop the tool.
- ccxt: Library for interacting with multiple cryptocurrency exchanges, in this case, Binance.
- pandas: Library for data manipulation and analysis, especially useful for handling time series data.
- ta: Library for calculating technical indicators like EMAs and RSI.
- matplotlib: Library for generating technical charts.
- twilio: Library for sending notifications via WhatsApp.
- os: Standard Python library for interacting with the operating system, used for handling file and directory paths.

## ⚙️ Configuration

1. Create a file or modify `config.json` in the `crypto_alert_tool` folder with the following structure:
```json
{
  "api_key": "YOUR_BINANCE_API_KEY",
  "secret_key": "YOUR_BINANCE_SECRET_KEY",
  "symbol": "BTC/USDT",
  "timeframe": "1m",
  "fast_ema_period": 12,
  "slow_ema_period": 26,
  "rsi_period": 14,
  "limit": 100,
  "email": {
    "sender": "your_email@gmail.com",
    "password": "your_application_password",
    "receiver": "destination_email@example.com"
  },
  "whatsapp": {
    "account_sid": "YOUR_TWILIO_ACCOUNT_SID",
    "auth_token": "YOUR_TWILIO_AUTH_TOKEN",
    "from_number": "whatsapp:+SOURCE_NUMBER",
    "to_number": "whatsapp:+DESTINATION_NUMBER"
  }
}
```

## 🚀 Use

To run the tool:

```bash
python crypto_alert_tool/main.py
# or
python3 crypto_alert_tool/main.py
```


## 📊 Señales de Trading

Trading Signals

The tool generates alerts based on:

1. **Buy Signal (Golden Cross)**:
   - When the fast EMA crosses above the slow EMA.
   - RSI below 50

2. **Sell Signal (Death Cross)**:
   - When the fast EMA crosses below the slow EMA.
   - RSI above 50

## 📁 Project Structure
```crypto_alert_tool/
├── init.py
├── alerts.py # Manejo de notificaciones
├── data_fetcher.py # Obtención de datos de Binance
├── indicators.py # Cálculo de indicadores técnicos
├── logger.py # Sistema de registro
├── main.py # Punto de entrada principal
└── plotter.py # Generación de gráficos
```


## ⚠️ Security Notes

- Do not share your Binance API keys
- Use application passwords for Gmail
- Keep your Twilio tokens secure
- Don't upload `config.json` file to public repositories

## 📝 License

This project is licensed under the MIT License.

## 👥 Contributions

Contributions are welcome. 