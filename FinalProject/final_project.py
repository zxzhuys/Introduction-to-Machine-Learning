import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras import layers, models, optimizers, callbacks
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Load Data
# Full year data for 2020 (20200101-20201231)
csv_file_path = 'POWER_Point_Hourly_20200101_20201231_033d45N_0112d07W_LST.csv'
df = pd.read_csv(csv_file_path, skiprows=12)

features = ['ALLSKY_SFC_SW_DWN', 'WS50M', 'T2M', 'WD50M']
target_cols = ['ALLSKY_SFC_SW_DWN', 'WS50M']
target_idx = [features.index(c) for c in target_cols]
data = df[features].replace(-999, np.nan).dropna().reset_index(drop=True).values

# Parameters
LOOK_BACK = 2 * 24         # Input: Past 48 hours
TEST_HOURS = 30 * 24       # Predict last 30 days (720 hours)
VAL_RATIO = 0.1            # Validation set ratio

# Corrected Data Splitting
n_total = len(data)
test_start_idx = n_total - TEST_HOURS

# Determine validation set range, remaining data (excluding test set) used for training and validation
n_train_val = test_start_idx
val_size = int(n_train_val * VAL_RATIO)
val_start_idx = n_train_val - val_size

# Split data
train_raw = data[:val_start_idx, :]
val_raw = data[val_start_idx - LOOK_BACK : test_start_idx, :]
test_raw = data[test_start_idx - LOOK_BACK :, :]

print(f"Total data length: {len(data)}")
print(f"Train raw shape: {train_raw.shape}")
print(f"Val raw shape:   {val_raw.shape} (Includes look-back buffer)")
print(f"Test raw shape:  {test_raw.shape} (Includes look-back buffer)")

# Normalization
scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()

train_X = scaler_X.fit_transform(train_raw)
val_X   = scaler_X.transform(val_raw)
test_X  = scaler_X.transform(test_raw)

train_y = scaler_y.fit_transform(train_raw[:, target_idx])
val_y   = scaler_y.transform(val_raw[:, target_idx])
test_y  = scaler_y.transform(test_raw[:, target_idx])

# Build Sequence Data
def make_seq(X2d, y2d, look_back):
    X, y = [], []
    for i in range(len(X2d) - look_back):
        X.append(X2d[i:i+look_back])
        y.append(y2d[i+look_back])
    return np.asarray(X), np.asarray(y)

X_train, y_train = make_seq(train_X, train_y, LOOK_BACK)
X_val,   y_val   = make_seq(val_X,   val_y,   LOOK_BACK)
X_test,  y_test  = make_seq(test_X,  test_y,  LOOK_BACK)

print(f"X_test shape: {X_test.shape}")

# CNN-LSTM Model
model = models.Sequential([
    layers.Input(shape=(LOOK_BACK, X_train.shape[2])),
    layers.Conv1D(128, kernel_size=5, activation='relu', padding='same'),
    layers.BatchNormalization(),
    layers.MaxPooling1D(pool_size=2),
    layers.Conv1D(64, kernel_size=3, activation='relu', padding='same'),
    layers.LSTM(128, return_sequences=True), 
    layers.Dropout(0.2),
    layers.LSTM(64, return_sequences=False),
    layers.Dropout(0.2),
    layers.Dense(64, activation='relu'),
    layers.Dense(2)
])

lr = 5e-4
model.compile(
    optimizer=optimizers.Adam(learning_rate=lr),
    loss='mse',
    metrics=['mae']
)

cb = [
    callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True),
    callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=1e-6)
]

# Train Model
history = model.fit(
    X_train, y_train,
    epochs=100,
    batch_size=64, 
    validation_data=(X_val, y_val),
    shuffle=False,
    callbacks=cb,
    verbose=1
)

# Prediction and Evaluation
pred_scaled = model.predict(X_test)
pred = scaler_y.inverse_transform(pred_scaled)
true = scaler_y.inverse_transform(y_test)

rmse_solar = np.sqrt(mean_squared_error(true[:, 0], pred[:, 0]))
r2_solar   = r2_score(true[:, 0], pred[:, 0])

rmse_wind = np.sqrt(mean_squared_error(true[:, 1], pred[:, 1]))
r2_wind   = r2_score(true[:, 1], pred[:, 1])

print("\n===== Test Metrics (Last 1 Month) =====")
print(f"SOLAR -> RMSE: {rmse_solar:.3f}, R2: {r2_solar:.3f}")
print(f"WIND  -> RMSE: {rmse_wind:.3f}, R2: {r2_wind:.3f}")

# Plot
plt.figure(figsize=(15, 8))
# Subplot 1: Solar Irradiance
plt.subplot(2, 1, 1)
plt.plot(true[:, 0], label='Actual Solar', alpha=0.7)
plt.plot(pred[:, 0], label='Predicted Solar', linestyle='--')
plt.title('Solar Irradiance Forecast (Last 30 Days)')
plt.ylabel('Solar Irradiance')
plt.legend()
# Subplot 2: Wind Speed
plt.subplot(2, 1, 2)
plt.plot(true[:, 1], label='Actual Wind', alpha=0.7)
plt.plot(pred[:, 1], label='Predicted Wind', linestyle='--')
plt.title('Wind Speed Forecast (Last 30 Days)')
plt.ylabel('Wind Speed')
plt.xlabel('Hours')
plt.legend()
plt.tight_layout()
plt.show()