import smbus
import time
import os

# MPU6050'nin I2C adresi
MPU6050_ADDRESS = 0x68

# MPU6050 register adresleri
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47
ACCEL_CONFIG = 0x1C
# I2C bus numarası (Raspberry Pi genellikle bus 1 kullanır)
bus = smbus.SMBus(1)

# MPU6050'yi başlatma
def mpu6050_init():
    # Güç yönetimi 1 register'ını sıfırlayarak MPU6050'yi başlatıyoruz
    bus.write_byte_data(MPU6050_ADDRESS, PWR_MGMT_1, 0)    
    bus.write_byte_data(MPU6050_ADDRESS, ACCEL_CONFIG, 0x00)

# MPU6050'den 16 bit veri okuma
def read_raw_data(addr):
    # MPU6050'den veri okuma (2 byte)
    high = bus.read_byte_data(MPU6050_ADDRESS, addr)
    low = bus.read_byte_data(MPU6050_ADDRESS, addr+1)

    # Yüksek ve düşük byte'ları birleştiriyoruz
    value = ((high << 8) | low)

    # İmzalı 16 bit formatta sonucu döndürüyoruz
    if value > 32768:
        value = value - 65536
    return value

def average_readings(num_samples=10):
    accel_x_total = 0
    accel_y_total = 0
    accel_z_total = 0

    for _ in range(num_samples):
        accel_x_total += read_raw_data(ACCEL_XOUT_H)
        accel_y_total += read_raw_data(ACCEL_YOUT_H)
        accel_z_total += read_raw_data(ACCEL_ZOUT_H)
        time.sleep(0.001)  # Her okuma arasında kısa bir gecikme

    accel_x_avg = accel_x_total / num_samples
    accel_y_avg = accel_y_total / num_samples
    accel_z_avg = accel_z_total / num_samples

    return accel_x_avg, accel_y_avg, accel_z_avg


def MPU_AccelXYZ():
    accel_x_avg, accel_y_avg, accel_z_avg = average_readings()
# Ana fonksiyon
if __name__ == "__main__":
    mpu6050_init()

    while True:
        # Hızlanma verilerini okuma

        accel_x_avg, accel_y_avg, accel_z_avg = average_readings()

        # Ekrana yazdırma
        print(f"Accel X: {accel_x_avg} | Accel Y: {accel_y_avg} | Accel Z: {accel_z_avg}")

        # 1 saniye bekleme
        #time.sleep(0.1)
