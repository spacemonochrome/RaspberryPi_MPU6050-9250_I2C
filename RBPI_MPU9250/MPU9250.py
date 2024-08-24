import smbus
import time

# MPU9250 I2C adresi
MPU9250_ADDRESS = 0x68  # MPU9250 I2C adresi (varsayılan)
ACCEL_XOUT_H = 0x3B    # X ekseni ivmeölçer yüksek veri byte'ı
ACCEL_XOUT_L = 0x3C    # X ekseni ivmeölçer düşük veri byte'ı
ACCEL_YOUT_H = 0x3D    # Y ekseni ivmeölçer yüksek veri byte'ı
ACCEL_YOUT_L = 0x3E    # Y ekseni ivmeölçer düşük veri byte'ı
ACCEL_ZOUT_H = 0x3F    # Z ekseni ivmeölçer yüksek veri byte'ı
ACCEL_ZOUT_L = 0x40    # Z ekseni ivmeölçer düşük veri byte'ı
PWR_MGMT_1 = 0x6B     # Güç yönetim register'ı
ACCEL_CONFIG = 0x1C
# I2C bus numarası
bus = smbus.SMBus(1)  # Raspbery Pi için 1 numaralı I2C bus kullanımı

def mpu9250_init():
    # MPU9250'yi uyandır (sleep modundan çıkar)
    bus.write_byte_data(MPU9250_ADDRESS, PWR_MGMT_1, 0)
    bus.write_byte_data(MPU9250_ADDRESS, ACCEL_CONFIG, 0x00)
    time.sleep(0.1)

def read_raw_data(addr):
    high = bus.read_byte_data(MPU9250_ADDRESS, addr)
    low = bus.read_byte_data(MPU9250_ADDRESS, addr + 1)
    value = ((high << 8) | low)
    if value > 32768:
        value -= 65536
    return value

def read_accelerometer():
    accel_x = read_raw_data(ACCEL_XOUT_H)
    accel_y = read_raw_data(ACCEL_YOUT_H)
    accel_z = read_raw_data(ACCEL_ZOUT_H)
    return accel_x, accel_y, accel_z

if __name__ == "__main__":
    mpu9250_init()
    while True:
        accel_x, accel_y, accel_z = read_accelerometer()
        print(f"Accel X: {accel_x}, Accel Y: {accel_y}, Accel Z: {accel_z}")
        time.sleep(0.1)  # 0.5 saniye bekle
