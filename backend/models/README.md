Place trained model artifacts in this folder:

- csrnet_model.pth
- lstm_model.pth

Optional normalization metadata file for LSTM:
- lstm_scaler.json

Example lstm_scaler.json (min-max):
{
  "method": "minmax",
  "min": 0,
  "max": 50000
}

Example lstm_scaler.json (z-score):
{
  "method": "zscore",
  "mean": 12000,
  "std": 4000
}
