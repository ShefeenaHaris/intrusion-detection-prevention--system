
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.regularizers import l2
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import joblib

# -------------------------------
# 1. Load Dataset
# -------------------------------

columns = ["duration","protocol_type","service","flag","src_bytes","dst_bytes","land","wrong_fragment","urgent","hot","num_failed_logins","logged_in","num_compromised","root_shell","su_attempted","num_root","num_file_creations","num_shells","num_access_files","num_outbound_cmds","is_host_login","is_guest_login","count","srv_count","serror_rate","srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate","diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count","dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate","dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate","attack","level"]

df = pd.read_csv('KDDTrain+.csv', names=columns)

# -------------------------------
# 2. Multi-class Mapping
# -------------------------------

def map_attack(attack):

    dos = ['back','land','neptune','pod','smurf','teardrop','apache2','udpstorm','processtable','mailbomb']
    probe = ['ipsweep','mscan','nmap','portsweep','saint','satan']
    r2l = ['ftp_write','guess_passwd','imap','multihop','phf','spy','warezclient','warezmaster','sendmail','named','snmpgetattack','snmpguess','xlock','xsnoop','worm']
    u2r = ['buffer_overflow','loadmodule','perl','rootkit','httptunnel','ps','sqlattack','xterm']

    if attack == 'normal': return 'Normal'
    if attack in dos: return 'DoS'
    if attack in probe: return 'Probe'
    if attack in r2l: return 'R2L'
    if attack in u2r: return 'U2R'
    return 'DoS'

df['attack_class'] = df['attack'].apply(map_attack)

# -------------------------------
# 3. Encoding
# -------------------------------

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df['attack_class'])

X = pd.get_dummies(df.drop(['attack','level','attack_class'], axis=1))

# SAVE FEATURE COLUMNS (IMPORTANT)
joblib.dump(X.columns.tolist(), 'feature_columns.pkl')

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Reshape for CNN
X_reshaped = np.reshape(X_scaled, (X_scaled.shape[0], X_scaled.shape[1], 1))

# Stratified split to avoid bias
X_train, X_val, y_train, y_val = train_test_split(
    X_reshaped,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

# -------------------------------
# 4. CNN Model (ANTI-OVERFITTING)
# -------------------------------

model = Sequential([

    Conv1D(32, kernel_size=3, activation='relu',
           kernel_regularizer=l2(0.001),
           input_shape=(X_train.shape[1],1)),

    BatchNormalization(),
    MaxPooling1D(pool_size=2),

    Dropout(0.5),

    Flatten(),

    Dense(64, activation='relu',
          kernel_regularizer=l2(0.001)),

    Dropout(0.5),

    Dense(5, activation='softmax')

])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# -------------------------------
# 5. Training Callbacks
# -------------------------------

early_stop = EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True
)

reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.3,
    patience=3,
    min_lr=0.00001
)

checkpoint = ModelCheckpoint(
    'idps_multiclass_model.h5',
    monitor='val_accuracy',
    save_best_only=True
)

# -------------------------------
# 6. Train
# -------------------------------

model.fit(
    X_train,
    y_train,
    epochs=40,
    batch_size=128,
    validation_data=(X_val, y_val),
    callbacks=[early_stop, reduce_lr, checkpoint]
)

# -------------------------------
# 7. Save components
# -------------------------------

joblib.dump(scaler, 'scaler.pkl')
joblib.dump(label_encoder, 'label_encoder.pkl')

print("✅ Training Complete (Optimized to reduce overfitting)")
