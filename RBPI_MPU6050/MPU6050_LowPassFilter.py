import smbus
import time
import os

# MPU6050 I2C adresi
MPU6050_ADDRESS = 0x68
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
ACCEL_CONFIG = 0x1C
filtered_accel_x = 0
filtered_accel_y = 0
filtered_accel_z = 0

# I2C bus numarası
bus = smbus.SMBus(1)

# MPU6050'yi başlatma
def mpu6050_init():
    bus.write_byte_data(MPU6050_ADDRESS, PWR_MGMT_1, 0)    
    bus.write_byte_data(MPU6050_ADDRESS, ACCEL_CONFIG, 0x00)

# MPU6050'den 16 bit veri okuma
def read_raw_data(addr):
    high = bus.read_byte_data(MPU6050_ADDRESS, addr)
    low = bus.read_byte_data(MPU6050_ADDRESS, addr+1)
    value = ((high << 8) | low)
    if value > 32768:
        value = value - 65536
    return value

# Düşük geçirgen filtre uygulama
def low_pass_filter(new_value, prev_value, alpha=0.5):
    return prev_value + alpha * (new_value - prev_value)

def MPU_AccelXYZ():

    global filtered_accel_x
    global filtered_accel_y
    global filtered_accel_z

    accel_x = read_raw_data(ACCEL_XOUT_H)
    accel_y = read_raw_data(ACCEL_YOUT_H)
    accel_z = read_raw_data(ACCEL_ZOUT_H)

    filtered_accel_x = low_pass_filter(accel_x, filtered_accel_x)
    filtered_accel_y = low_pass_filter(accel_y, filtered_accel_y)
    filtered_accel_z = low_pass_filter(accel_z, filtered_accel_z)

    return filtered_accel_x, filtered_accel_y, filtered_accel_z

# Ana fonksiyon
if __name__ == "__main__":
    mpu6050_init()

    # İlk filtrelenmiş değerleri başlatma

    while True:
		#os.system("clear")
        # Ham hızlanma verilerini okuma
        accel_x = read_raw_data(ACCEL_XOUT_H)
        accel_y = read_raw_data(ACCEL_YOUT_H)
        accel_z = read_raw_data(ACCEL_ZOUT_H)

        # Düşük geçirgen filtre uygulama
        filtered_accel_x = low_pass_filter(accel_x, filtered_accel_x)
        filtered_accel_y = low_pass_filter(accel_y, filtered_accel_y)
        filtered_accel_z = low_pass_filter(accel_z, filtered_accel_z)

        # Filtrelenmiş değerleri ekrana yazdırma
        print(f"Accel X: {int(filtered_accel_x)} | Accel Y: {int(filtered_accel_y)} |  Accel Z: {int(filtered_accel_z)}")

        # 0.1 saniye bekleme
        time.sleep(0.01)
