# PM10 Air Quality Forecasting and Explanation
 
Time series forecasting of PM10 particulate matter concentrations in Sarajevo, combining air quality and meteorological data with missing-value imputation, comparative model evaluation, and model interpretability via SHAP.
 
## Dataset
 
The dataset was built from air quality and meteorological data collected between **2018 and 2023** in Sarajevo by the Federal Hydrometeorological Institute, at the **Bjelave** meteorological station.
 
- **2179 daily measurements**
- **8 meteorological parameters**: wind speed, wind direction, precipitation, pressure, temperature, humidity, visibility, cloudiness
- **3 pollutant concentrations**: PM10, SO2, NO2
- **12 columns total** (including DateTime)
## Data Imputation
 
A significant portion of measurements were missing across the observed time horizon (2018–2023). Missing values were handled using **Neighboring Average Imputation**:
 
```
x_missing = (Σ x_i for i in 1..2N) / 2N
```
 
Where:
- `x_missing` — the estimated value for the missing data point
- `Σ x_i` — sum of the neighboring data points' values
- `N` — number of consecutive missing values
- `2N` — total number of neighboring points used for the average (N points before the gap, N points after)
## Methodology
 
Two forecasting models were evaluated on the imputed time series:
 
- **Facebook Prophet** — selected for its strong performance on data with seasonal trends; also tested on raw data (without imputation), since Prophet can natively handle discontinuous time series
- **LSTM** — selected for its ability to model complex, non-linear, long-term temporal dependencies; requires a fully continuous, scaled sequence, so it was trained exclusively on the imputed and `MinMaxScaler`-normalized dataset
Both models were tested across **three forecasting horizons**: 30-day, 60-day, and 90-day PM10 predictions, and evaluated using **MAE**, **RMSE**, and **R²**.
 
**Result:** Facebook Prophet consistently outperformed LSTM across all three horizons.
 
## Model Interpretation — SHAP
 
To explain the predictions of the best-performing model (FB Prophet), **Kernel SHAP** was applied. Kernel SHAP was chosen specifically because it is **model-agnostic**, as time series models such as FB Prophet are not natively compatible with model-specific SHAP explainers (e.g., TreeExplainer). 
 
- Shapley values were computed using a background dataset, a subset of the training data
- Explanations are provided for the **30-day** and **60-day** prediction horizons
- Additional explanations are presented for **individual predictions** within the one-month horizon

  
## Pipeline Overview

<img width="2800" height="625" alt="xxx - Flow diplomski 2" src="https://github.com/user-attachments/assets/daca75fd-9b53-4571-83c7-86b7869d3af7" />

 

                    ├──> 60-day PM10 predictions ──> SHAP analysis
                    └──> 90-day PM10 predictions
```
