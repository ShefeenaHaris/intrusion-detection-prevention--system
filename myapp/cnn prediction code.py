import os
import time
import joblib
import numpy as np
import pandas as pd
import tensorflow as tf

from scapy.all import *
from datetime import datetime
from myapp.DBConnection import Db

# =========================================
# DATABASE CONNECTION
# =========================================

db = Db()

# =========================================
# LOAD MODEL + PREPROCESSING FILES
# =========================================

print("⏳ Loading CNN Model...")

model = tf.keras.models.load_model(
    'idps_multiclass_model.h5'
)

print("✅ CNN Model Loaded")

scaler = joblib.load('scaler.pkl')

label_encoder = joblib.load(
    'label_encoder.pkl'
)

feature_columns = joblib.load(
    'feature_columns.pkl'
)

print("✅ Preprocessing Files Loaded")

# =========================================
# GLOBAL VARIABLES
# =========================================

packet_counter = {}

last_seen_time = {}

blocked_ips = set()

DOS_THRESHOLD = 50

TIME_WINDOW = 10

# =========================================
# BLOCK IP FUNCTION
# =========================================

def block_ip(attacker_ip):

    try:

        # Avoid duplicate firewall rules
        if attacker_ip not in blocked_ips:

            command = (
                f'netsh advfirewall firewall add rule '
                f'name="Block_{attacker_ip}" '
                f'dir=in action=block '
                f'remoteip={attacker_ip}'
            )

            os.system(command)

            blocked_ips.add(attacker_ip)

            print(f"❌ Blocked IP: {attacker_ip}")

    except Exception as e:

        print("Firewall Error:", e)

# =========================================
# MAIN PACKET PROCESSING FUNCTION
# =========================================

def process_packet(packet):

    try:

        # ---------------------------------
        # Ignore Non-IP Packets
        # ---------------------------------

        if not packet.haslayer(IP):
            return

        # ---------------------------------
        # SOURCE IP
        # ---------------------------------

        attacker_ip = packet[IP].src

        current_time = time.time()

        # ---------------------------------
        # PACKET COUNT LOGIC
        # ---------------------------------

        if attacker_ip not in packet_counter:

            packet_counter[attacker_ip] = 1

            last_seen_time[attacker_ip] = current_time

        else:

            # Reset count after time window
            if current_time - last_seen_time[attacker_ip] > TIME_WINDOW:

                packet_counter[attacker_ip] = 1

            else:

                packet_counter[attacker_ip] += 1

            last_seen_time[attacker_ip] = current_time

        packet_count = packet_counter[attacker_ip]

        # =========================================
        # FEATURE EXTRACTION
        # =========================================

        data = {}

        # ---------------------------------
        # Duration
        # ---------------------------------

        data['duration'] = 0

        # ---------------------------------
        # Protocol Type
        # ---------------------------------

        if packet.haslayer(TCP):

            data['protocol_type'] = 'tcp'

        elif packet.haslayer(UDP):

            data['protocol_type'] = 'udp'

        else:

            data['protocol_type'] = 'icmp'

        # ---------------------------------
        # Service Detection
        # ---------------------------------

        if packet.haslayer(TCP):

            port = packet[TCP].dport

            if port == 80:

                data['service'] = 'http'

            elif port == 443:

                data['service'] = 'https'

            elif port == 21:

                data['service'] = 'ftp'

            elif port == 22:

                data['service'] = 'ssh'

            elif port == 23:

                data['service'] = 'telnet'

            else:

                data['service'] = 'other'

        else:

            data['service'] = 'other'

        # ---------------------------------
        # TCP FLAGS
        # ---------------------------------

        if packet.haslayer(TCP):

            tcp_flags = str(packet[TCP].flags)

            if tcp_flags == "S":

                data['flag'] = 'S0'

            elif tcp_flags == "SA":

                data['flag'] = 'SF'

            else:

                data['flag'] = 'REJ'

        else:

            data['flag'] = 'SF'

        # ---------------------------------
        # Bytes
        # ---------------------------------

        data['src_bytes'] = len(packet)

        data['dst_bytes'] = len(packet)

        # ---------------------------------
        # Dynamic Features
        # ---------------------------------

        data['count'] = packet_count

        data['srv_count'] = packet_count

        # =========================================
        # REMAINING NSL-KDD FEATURES
        # =========================================

        remaining_features = [

            "land","wrong_fragment","urgent","hot",
            "num_failed_logins","logged_in",
            "num_compromised","root_shell",
            "su_attempted","num_root",
            "num_file_creations","num_shells",
            "num_access_files","num_outbound_cmds",
            "is_host_login","is_guest_login",
            "serror_rate","srv_serror_rate",
            "rerror_rate","srv_rerror_rate",
            "same_srv_rate","diff_srv_rate",
            "srv_diff_host_rate",
            "dst_host_count",
            "dst_host_srv_count",
            "dst_host_same_srv_rate",
            "dst_host_diff_srv_rate",
            "dst_host_same_src_port_rate",
            "dst_host_srv_diff_host_rate",
            "dst_host_serror_rate",
            "dst_host_srv_serror_rate",
            "dst_host_rerror_rate",
            "dst_host_srv_rerror_rate"

        ]

        for feature in remaining_features:

            data[feature] = 0

        # =========================================
        # DATAFRAME CREATION
        # =========================================

        df = pd.DataFrame([data])

        # One-hot encoding
        df = pd.get_dummies(df)

        # Add missing columns
        for col in feature_columns:

            if col not in df.columns:

                df[col] = 0

        # Maintain same training order
        df = df[feature_columns]

        # =========================================
        # SCALING
        # =========================================

        X_scaled = scaler.transform(df)

        # CNN reshape
        X_reshaped = np.reshape(

            X_scaled,

            (
                X_scaled.shape[0],
                X_scaled.shape[1],
                1
            )

        )

        # =========================================
        # CNN PREDICTION
        # =========================================

        prediction = model.predict(

            X_reshaped,

            verbose=0

        )

        predicted_class = np.argmax(prediction)

        confidence = float(np.max(prediction))

        attack_type = label_encoder.inverse_transform(

            [predicted_class]

        )[0]

        # =========================================
        # HYBRID DETECTION LOGIC
        # =========================================

        attack_detected = False

        final_attack = "Normal"

        # ---------------------------------
        # 1. CNN Detection
        # ---------------------------------

        if attack_type != "Normal":

            attack_detected = True

            final_attack = attack_type

        # ---------------------------------
        # 2. DoS Detection
        # Highest Priority
        # ---------------------------------

        if packet_count > DOS_THRESHOLD:

            attack_detected = True

            final_attack = "DoS"

            confidence = 0.99

        # ---------------------------------
        # 3. Probe Detection
        # ---------------------------------

        elif packet.haslayer(TCP):

            suspicious_ports = [

                21,22,23,25,
                53,80,110,
                135,139,143,
                443,445,3389

            ]

            port = packet[TCP].dport

            if port in suspicious_ports and packet_count > 15:

                attack_detected = True

                final_attack = "Probe"

                confidence = 0.95

        # ---------------------------------
        # 4. R2L Detection
        # ---------------------------------

        elif packet.haslayer(TCP):

            r2l_ports = [21,23,110,143]

            port = packet[TCP].dport

            if port in r2l_ports and len(packet) > 1000:

                attack_detected = True

                final_attack = "R2L"

                confidence = 0.94

        # ---------------------------------
        # 5. U2R Detection
        # ---------------------------------

        elif packet.haslayer(TCP):

            flags = str(packet[TCP].flags)

            if flags == "FPU" or flags == "R":

                attack_detected = True

                final_attack = "U2R"

                confidence = 0.96

        # Final attack label
        attack_type = final_attack

        # =========================================
        # OUTPUT
        # =========================================

        print("\n==============================")

        print("Time:", datetime.now())

        print("Source IP:", attacker_ip)

        print("Packet Count:", packet_count)

        print("Attack Type:", attack_type)

        print("Confidence:", round(confidence, 4))

        # =========================================
        # BLOCKING LOGIC
        # =========================================

        if attack_detected:

            print("⚠ ATTACK DETECTED")

            block_ip(attacker_ip)

            status = "BLOCKED"

            print(f"{attacker_ip} Blocked")

        else:

            print("✅ Normal Traffic")

            status = "NORMAL"

        # =========================================
        # SAVE LOG TO DATABASE
        # =========================================

        db.insert_log(

            ipaddress=attacker_ip,

            log_type=attack_type,

            customer_id='4'

        )

        print(f"✅ Logged {attack_type}: {attacker_ip}")

        print("✅ Log Stored In Database")

    except Exception as e:

        print("❌ Error:", e)

# =========================================
# START LIVE PACKET SNIFFING
# =========================================

print("\n🚀 Real-Time CNN Intrusion Detection Started...\n")

sniff(

    prn=process_packet,

    store=False

)

