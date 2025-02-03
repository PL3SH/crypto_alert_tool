import matplotlib.pyplot as plt
import pandas as pd
from typing import Any
from pathlib import Path
from datetime import datetime
import os
import logging

def ensure_assets_directory() -> Path:
    """
    Ensure the assets directory exists for saving plots.
    
    Returns:
        Path: Path object pointing to the assets directory.
    """
    BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    assets_path = BASE_DIR / "crypto_alert_tool" / "assets"
    assets_path.mkdir(parents=True, exist_ok=True)
    return assets_path

def plot_chart(df, symbol, fast_ema_period, slow_ema_period):
    fig, ax = plt.subplots(2, 1, figsize=(14, 10), gridspec_kw={'height_ratios': [3, 1]})

    # Upper Graphic: price and EMAs
    ax[0].plot(df.index, df['close'], label="Precio de Cierre", color="blue", linewidth=1)
    ax[0].plot(df.index, df['Fast_EMA'], label=f"EMA {fast_ema_period}", color="orange", linestyle="--")
    ax[0].plot(df.index, df['Slow_EMA'], label=f"EMA {slow_ema_period}", color="green", linestyle="--")

    # Mark alert points (Golden Cross and Death Cross)
    compra_indices = df[(df['Fast_EMA'] > df['Slow_EMA']) & (df['Fast_EMA'].shift(1) <= df['Slow_EMA'].shift(1))].index
    venta_indices = df[(df['Fast_EMA'] < df['Slow_EMA']) & (df['Fast_EMA'].shift(1) >= df['Slow_EMA'].shift(1))].index

    ax[0].scatter(compra_indices, df.loc[compra_indices, 'close'], color='green', label="Compra (Cruz de Oro)", marker="^", s=100, zorder=5)
    ax[0].scatter(venta_indices, df.loc[venta_indices, 'close'], color='red', label="Venta (Cruz de la Muerte)", marker="v", s=100, zorder=5)

    ax[0].set_title(f"Precio y EMAs con Alertas - {symbol}")
    ax[0].set_ylabel("Precio (USD)")
    ax[0].legend()
    ax[0].grid()

    # Lower Graphic: RSI
    ax[1].plot(df.index, df['RSI'], label="RSI", color="purple", linewidth=1)
    ax[1].axhline(70, color="red", linestyle="--", label="Sobrecompra (70)")
    ax[1].axhline(30, color="green", linestyle="--", label="Sobreventa (30)")

    # Mark alert points on RSI
    sobrecompra_indices = df[(df['RSI'] > 70)].index
    sobreventa_indices = df[(df['RSI'] < 30)].index

    ax[1].scatter(sobrecompra_indices, df.loc[sobrecompra_indices, 'RSI'], color='red', label="Sobrecompra", marker="x", s=50, zorder=5)
    ax[1].scatter(sobreventa_indices, df.loc[sobreventa_indices, 'RSI'], color='green', label="Sobreventa", marker="o", s=50, zorder=5)

    ax[1].set_title("Índice de Fuerza Relativa (RSI) con Alertas")
    ax[1].set_ylabel("RSI")
    ax[1].set_xlabel("Fecha")
    ax[1].legend()
    ax[1].grid()

    # Ajustar el diseño y mostrar
    plt.tight_layout()
    #plt.show()
    
    
    
    # Save the plot
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Sanitize the symbol for filename
    safe_symbol = symbol.replace('/', '_')
    filename = f"{safe_symbol}_{timestamp}.jpg"
    save_path = ensure_assets_directory() / filename
    plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close()  # Close the figure to free memory

    return str(save_path)  # Return the path of the saved file


def delete_image(image_path):
    try:
        os.remove(image_path)
    except FileNotFoundError:
        logging.warning(f"No se pudo eliminar el archivo {image_path} porque no existe.")