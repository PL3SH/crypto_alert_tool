import logging
from datetime import datetime
import sys
import traceback
from data_fetcher import fetch_data
from indicators import calculate_indicators
from alerts import send_email, send_whatsapp
from logger import load_alert_log, is_alert_sent, log_alert
from plotter import plot_chart, delete_image
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(BASE_DIR, 'crypto_alert.log')),
        logging.StreamHandler(sys.stdout)
    ]
)

def main():
    try:
        logging.info(f"Directorio base: {BASE_DIR}")
        logging.info("Iniciando el programa de alertas crypto...")
        
        config_path = os.path.join(BASE_DIR, "crypto_alert_tool", "config.json")
        logging.info(f"Leyendo configuración desde: {config_path}")
        
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
            logging.info("Configuración cargada exitosamente")
        except FileNotFoundError:
            logging.error(f"No se encontró el archivo de configuración en: {config_path}")
            raise
        except json.JSONDecodeError:
            logging.error("El archivo de configuración contiene JSON inválido")
            raise

        logging.info("Obteniendo datos del mercado...")
        df = fetch_data()
        logging.info(f"Datos obtenidos exitosamente. Registros: {len(df)}")

        logging.info("Calculando indicadores técnicos...")
        df = calculate_indicators(
            df,
            config["fast_ema_period"],
            config["slow_ema_period"],
            config["rsi_period"]
        )
        logging.info("Indicadores calculados exitosamente")

        alert_log = load_alert_log()
        latest = df.iloc[-1]
        previous = df.iloc[-2]
        latest_date = latest.name

        logging.info(f"Analizando datos para {config['symbol']} en {latest_date}")
        logging.info(f"RSI actual: {latest['RSI']:.2f}")
        logging.info(f"EMAs - Rápido: {latest['Fast_EMA']:.2f}, Lento: {latest['Slow_EMA']:.2f}")
        
        
        # Detectar cruce de EMAs y validar con RSI
        if previous["Fast_EMA"] <= previous["Slow_EMA"] and latest["Fast_EMA"] > latest["Slow_EMA"]:
            logging.info("Detectada posible señal de compra - Validando condiciones...")
            if latest["RSI"] < 50:
                if not is_alert_sent(alert_log, latest_date, "Compra - Cruz de Oro"):
                    logging.info("¡Señal de compra confirmada!")
                    mensaje = (
                        f"Señal de Compra Detectada:\n"
                        f"- Cruz de Oro en {config['symbol']}.\n"
                        f"- RSI Actual: {latest['RSI']:.2f}."
                    )
                    logging.info("Generando gráfico...")
                    image_path = plot_chart(df, config["symbol"], config["fast_ema_period"], config["slow_ema_period"])
                    logging.info(f"Gráfico generado exitosamente en: {image_path}")
                    send_email("Señal de Compra - Cruz de Oro", mensaje, config["email"], image_path)
                    send_whatsapp(mensaje, config["whatsapp"])
                    log_alert(alert_log, latest_date, "Compra - Cruz de Oro")
                    logging.info("Alertas enviadas exitosamente")
                    delete_image(image_path)

        elif previous["Fast_EMA"] >= previous["Slow_EMA"] and latest["Fast_EMA"] < latest["Slow_EMA"]:
            logging.info("Detectada posible señal de venta - Validando condiciones...")
            if latest["RSI"] > 50:
                if not is_alert_sent(alert_log, latest_date, "Venta - Cruz de la Muerte"):
                    logging.info("¡Señal de venta confirmada!")
                    mensaje = (
                        f"Señal de Venta Detectada:\n"
                        f"- Cruz de la Muerte en {config['symbol']}.\n"
                        f"- RSI Actual: {latest['RSI']:.2f}."
                    )
                    logging.info("Generando gráfico...")
                    image_path = plot_chart(df, config["symbol"], config["fast_ema_period"], config["slow_ema_period"])
                    logging.info(f"Gráfico generado exitosamente en: {image_path}")
                    send_email("Señal de Venta - Cruz de la Muerte", mensaje, config["email"], image_path)
                    send_whatsapp(mensaje, config["whatsapp"])
                    log_alert(alert_log, latest_date, "Venta - Cruz de la Muerte")
                    logging.info("Alertas enviadas exitosamente") 
                    delete_image(image_path)

        
        
        logging.info("Ejecución completada con éxito")

    except Exception as e:
        logging.error(f"Error en la ejecución del programa: {str(e)}")
        logging.error(traceback.format_exc())
        raise

if __name__ == "__main__":
    main()
