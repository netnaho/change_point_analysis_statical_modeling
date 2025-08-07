import pandas as pd
import numpy as np
import pymc3 as pm

def run_analysis():
    df = pd.read_csv('data/BrentOilPrices.csv')
    df['Date'] = pd.to_datetime(df['Date'], format='mixed', dayfirst=True, errors='coerce')
    df = df.dropna(subset=['Date', 'Price'])
    df = df.sort_values('Date')
    df['Log_Returns'] = np.log(df['Price']) - np.log(df['Price'].shift(1))
    df.dropna(inplace=True)

    log_returns = df['Log_Returns'].values
    n = len(log_returns)

    with pm.Model() as model:
        tau = pm.DiscreteUniform('tau', lower=0, upper=n - 1)
        mu1 = pm.Normal('mu1', mu=np.mean(log_returns), sigma=np.std(log_returns))
        mu2 = pm.Normal('mu2', mu=np.mean(log_returns), sigma=np.std(log_returns))
        sigma1 = pm.HalfNormal('sigma1', sigma=1.0)
        sigma2 = pm.HalfNormal('sigma2', sigma=1.0)
        idx = np.arange(n)
        mu = pm.math.switch(tau >= idx, mu1, mu2)
        sigma = pm.math.switch(tau >= idx, sigma1, sigma2)
        obs = pm.Normal('obs', mu=mu, sigma=sigma, observed=log_returns)
        trace = pm.sample(1000, tune=500, progressbar=False, return_inferencedata=False)

    tau_val = int(trace['tau'].mean())
    change_date = df.iloc[tau_val]['Date'].strftime('%Y-%m-%d')
    mu1_val = trace['mu1'].mean()
    mu2_val = trace['mu2'].mean()
    pct_change = (np.exp(mu2_val) - np.exp(mu1_val)) / np.exp(mu1_val) * 100

    return {
        'change_date': change_date,
        'tau_index': tau_val,
        'mu1': mu1_val,
        'mu2': mu2_val,
        'percent_change': round(pct_change, 2)
    }
