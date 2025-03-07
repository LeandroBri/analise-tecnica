from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from data import get_ohlcv, calculate_macd, calculate_indicators

def register_callbacks(app):
    @app.callback(

        [Output(f"crypto-chart-{i}", "figure") for i in range(4)] +
        [Output(f"macd-alert-{i}", "children") for i in range(4)],
        [Input(f"dropdown-pair-{i}", "value") for i in range(4)] +
        [Input(f"dropdown-timeframe-{i}", "value") for i in range(4)] +
        [Input(f"indicators-{i}", "value") for i in range(4)] +
        [Input("interval-component", "n_intervals")]
    )    
    def update_charts_and_alerts(*selections):
        figures = []
        alerts = []
        pairs = selections[:4]
        timeframes = selections[4:8]
        indicators_list = selections[8:12]

        for i in range(4):
            pair = pairs[i]
            timeframe = timeframes[i]
            indicators = indicators_list[i]

            try:
                df = get_ohlcv(pair, timeframe)
                df = calculate_macd(df)
                df = calculate_indicators(df, indicators)

                #print(f"MACD {df}")                

                # Obtém os últimos valores de MACD e da linha de sinal
                last_macd = df["MACD"].iloc[-1]
                last_signal = df["Signal"].iloc[-1]
                prev_macd = df["MACD"].iloc[-2]
                prev_signal = df["Signal"].iloc[-2]

                # Preço de entrada (último fechamento)
                entry_price = df["close"].iloc[-1]
                    
                
                # Inicializa alerta como "Neutro"
                alert = html.Div(f"🔵 Neutro - Preço Atual: $ {entry_price:.2f}", style={'padding': '2px 4px', 'text-align': 'left', 'background': '#090909', 'color': '#999', 'font-size': '18px'})
                
                
                # Lógica de compra/venda
                if prev_macd < prev_signal and last_macd > last_signal:
                    exit_price = entry_price * 1.02  # Alvo de saída 2% acima
                    alert = html.Div(
                        f"🟢 COMPRA - \n💰 Entrada: $ {entry_price:.2f}\n🎯 Alvo: $ {exit_price:.2f}",
                        style={'padding': '2px 4px', 'text-align': 'left', 'background': '#98FB98', 'color': '#006400', 'font-size': '18px'}
                    )
                elif prev_macd > prev_signal and last_macd < last_signal:
                    exit_price = entry_price * 0.98  # Alvo de saída 2% abaixo
                    alert = html.Div(
                        f"🔴 VENDA - \n💰 Entrada: $ {entry_price:.2f} USDT\n🎯 Alvo: $ {exit_price:.2f} USDT",
                        style={'padding': '2px 4px', 'text-align': 'left', 'background': '#D83822', 'color': '#FEC0B1', 'font-size': '18px'}
                    )

                '''
                # Lógica de compra/venda
                if prev_macd < prev_signal and last_macd > last_signal:
                    exit_price = entry_price * 1.02  # Alvo de saída 2% acima
                    alert = html.Div(
                        f"🟢 COMPRA - MACD cruzou para cima!\n💰 Entrada: $ {entry_price:.2f}\n🎯 Alvo: $ {exit_price:.2f}",
                        style={'padding': '2px 4px', 'text-align': 'left', 'background': '#98FB98', 'color': '#006400', 'font-size': '18px'}
                    )
                elif prev_macd > prev_signal and last_macd < last_signal:
                    exit_price = entry_price * 0.98  # Alvo de saída 2% abaixo
                    alert = html.Div(
                        f"🔴 VENDA - MACD cruzou para baixo!\n💰 Entrada: $ {entry_price:.2f} USDT\n🎯 Alvo: $ {exit_price:.2f} USDT",
                        style={'padding': '2px 4px', 'text-align': 'left', 'background': '#D83822', 'color': '#FEC0B1', 'font-size': '18px'}
                    )
                '''    
                
                fig = go.Figure(data=[go.Candlestick(
                    x=df["timestamp"], open=df["open"], high=df["high"], low=df["low"], close=df["close"], name=pair
                )])

                if "RSI" in indicators:
                    fig.add_trace(go.Scatter(x=df["timestamp"], y=df["RSI"], mode="lines", name="RSI", line=dict(color="purple"), yaxis="y2"))

                if "EMA" in indicators:
                    fig.add_trace(go.Scatter(x=df["timestamp"], y=df["EMA"], mode="lines", name="EMA", line=dict(color="orange")))

                if "SMA" in indicators:
                    fig.add_trace(go.Scatter(x=df["timestamp"], y=df["SMA"], mode="lines", name="SMA", line=dict(color="yellow")))

                if "BB" in indicators:
                    fig.add_trace(go.Scatter(x=df["timestamp"], y=df["BB_Upper"], mode="lines", name="Bollinger Superior", line=dict(color="red")))
                    fig.add_trace(go.Scatter(x=df["timestamp"], y=df["BB_Lower"], mode="lines", name="Bollinger Inferior", line=dict(color="green")))

                fig.update_layout(
                    title=f"Grafico de: {timeframe} - Crypto: {pair}",
                    #xaxis_title="Tempo",
                    #yaxis_title="Preço (USDT)",
                    paper_bgcolor="#090909",
                    plot_bgcolor="#010101",
                    font=dict(color="white"),
                    xaxis=dict(showgrid=False, zeroline=False),
                    yaxis=dict(showgrid=False, zeroline=False),
                    showlegend=False,
                    legend=dict(x=0, y=1, bgcolor="black", font=dict(size=12, color="white")),
                    margin=dict(l=4, r=4, t=50, b=4),
                    hovermode="x unified",
                    dragmode="pan",
                    xaxis_rangeslider_visible=False,
                    #width=600,
                    height=300
                )    

                #fig.update_layout(
                #    title=f"{pair} - {timeframe}",
                #    xaxis_title="Tempo", yaxis_title="Preço (USDT)",
                #    yaxis2=dict(overlaying="y", side="right", showgrid=False),
                #    paper_bgcolor="#090909", plot_bgcolor="#010101",
                #    font=dict(color="white"),
                #    xaxis_rangeslider_visible=False
                #)

            except Exception as e:
                fig = go.Figure()
                alert = f"❌ Erro: {str(e)}"              

            figures.append(fig)
            alerts.append(alert)

        return figures + alerts