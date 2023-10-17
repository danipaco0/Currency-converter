from flask import Flask, request, render_template
import requests
import plotly
import plotly.graph_objs as go

from datetime import datetime, timedelta

app = Flask(__name__, template_folder='templates')
app.config['TEMPLATES_AUTO_RELOAD'] = True
@app.route('/')
def index():
    return '''
        <style>
            body {background-color: #88BDBC;
            font-family: Arial, sans-serif;}
            h1:   {color: #254E58;}
        </style>
        <h1 style="text-align:center">Currency converter</h1>
        <form method="POST" action="/convert" style="text-align:center">
            <input type="text" name="montant" >
            <select id="choix_StartDevise" name="start_devise" >
                <option value="AUD">AUD</option>
                <option value="BRL">BRL</option>
                <option value="CAD">CAD</option>
                <option value="CHF">CHF</option>
                <option value="CNY">CNY</option>
                <option value="CZK">CZK</option>
                <option value="DKK">DKK</option>
                <option value="EUR">EUR</option>
                <option value="GBP">GBP</option>
                <option value="HRK">HRK</option>
                <option value="HUF">HUF</option>
                <option value="ILS">ILS</option>
                <option value="ISK">ISK</option>
                <option value="INR">INR</option>
                <option value="JPY">JPY</option>
                <option value="KRW">KRW</option>
                <option value="MXN">MXN</option>
                <option value="MYR">MYR</option>
                <option value="NOK">NOK</option>
                <option value="NZD">NZD</option>
                <option value="PHP">PHP</option>
                <option value="PLN">PLN</option>
                <option value="RON">RON</option>
                <option value="RUB">RUB</option>
                <option value="SEK">SEK</option>
                <option value="SGD">SGD</option>
                <option value="THB">THB</option>
                <option value="TRY">TRY</option>
                <option value="USD">USD</option>
                <option value="ZAR">ZAR</option>
            </select>
            <select id="choix_EndDevise" name="end_devise">
                <option value="AUD">AUD</option>
                <option value="BRL">BRL</option>
                <option value="CAD">CAD</option>
                <option value="CHF">CHF</option>
                <option value="CNY">CNY</option>
                <option value="CZK">CZK</option>
                <option value="DKK">DKK</option>
                <option value="EUR">EUR</option>
                <option value="GBP">GBP</option>
                <option value="HRK">HRK</option>
                <option value="HUF">HUF</option>
                <option value="ILS">ILS</option>
                <option value="ISK">ISK</option>
                <option value="INR">INR</option>
                <option value="JPY">JPY</option>
                <option value="KRW">KRW</option>
                <option value="MXN">MXN</option>
                <option value="MYR">MYR</option>
                <option value="NOK">NOK</option>
                <option value="NZD">NZD</option>
                <option value="PHP">PHP</option>
                <option value="PLN">PLN</option>
                <option value="RON">RON</option>
                <option value="RUB">RUB</option>
                <option value="SEK">SEK</option>
                <option value="SGD">SGD</option>
                <option value="THB">THB</option>
                <option value="TRY">TRY</option>
                <option value="USD">USD</option>
                <option value="ZAR">ZAR</option>
            </select>
            <br>
            <br>
            <input type="submit" value="Convertir">
        </form>
    '''


@app.route('/convert', methods=['POST'])
def convert():
    apiKey = 'cur_live_hLKt5oYaOEl3WleBMKLWfR8VjcJAF7MRnk3TuINf'

    current_date = datetime.now() - timedelta(days=1)
    current_date_string = current_date.strftime('%Y-%m-%d')
    year_date = current_date - timedelta(days=365)
    year_date_string = year_date.strftime('%Y-%m-%d')

    amount = float(request.form['montant'])
    input_currency = request.form['start_devise']
    output_currency = request.form['end_devise']
    url = f'https://api.currencyapi.com/v3/latest?apikey={apiKey}&base_currency={input_currency}'
    urlHist = f'https://api.currencyapi.com/v3/range?apikey={apiKey}&datetime_start={year_date_string}&datetime_end={current_date_string}&base_currency={input_currency}&currencies={output_currency}'
    urlInfo = f'https://api.currencyapi.com/v3/currencies?apikey={apiKey}&currencies={input_currency},{output_currency}'
    
    responseInfo = requests.get(urlInfo)
    dataInfo = responseInfo.json()

    responseExchange = requests.get(url)
    dataExchange = responseExchange.json()
    rate = dataExchange['data'][output_currency]['value']
    result = amount * rate
    conversion = str(amount)+" "+dataInfo['data'][input_currency]['symbol_native']+" = "+str(result)+" "+dataInfo['data'][output_currency]['symbol_native']

    responseHistorical = requests.get(urlHist)
    dataHistorical = responseHistorical.json()
    print(dataHistorical)
    dict = dataHistorical['data']
    dates = []
    rates = []
    for d in dict:
        dates.append(d)
        rates.append(dict[d][output_currency])

    plotData = [go.Scatter(x=dates, y=rates, mode='lines', name=dataInfo['data'][input_currency]['name']+" to "+dataInfo['data'][output_currency]['name'])]
    layout = {'title': '<b>'+dataInfo['data'][input_currency]['name']+" to "+dataInfo['data'][output_currency]['name']+'</b>', 'paper_bgcolor': '#88BDBC', 
              'font_family': 'Arial, sans-sherif', 'font_size':20, 'font_color':'#254E58'}
    fig = go.Figure(data=plotData, layout=layout)
    plot_div = plotly.offline.plot(fig, output_type='div')
    return render_template('index.html', plot_div=plot_div, conversion=conversion)

if __name__ == '__main__':
    app.run()
