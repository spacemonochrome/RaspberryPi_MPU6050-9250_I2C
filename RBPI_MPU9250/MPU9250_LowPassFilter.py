import smbus
import time

# MPU9250 I2C adresi ve register'lar
MPU9250_ADDRESS = 0x68
ACCEL_XOUT_H = 0x3B
ACCEL_XOUT_L = 0x3C
ACCEL_YOUT_H = 0x3D
ACCEL_YOUT_L = 0x3E
ACCEL_ZOUT_H = 0x3F
ACCEL_ZOUT_L = 0x40
ACCEL_CONFIG = 0x1C
PWR_MGMT_1 = 0x6B

# I2C bus numarası
bus = smbus.SMBus(1)

def mpu9250_init():
    # MPU9250'yi uyandır (sleep modundan çıkar)
    bus.write_byte_data(MPU9250_ADDRESS, PWR_MGMT_1, 0)
    time.sleep(0.1)

    # Hassasiyeti ±2g olarak ayarlama
    bus.write_byte_data(MPU9250_ADDRESS, ACCEL_CONFIG, 0x00)

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

def low_pass_filter(new_value, prev_value, alpha=0.1):
    return alpha * new_value + (1 - alpha) * prev_value

if __name__ == "__main__":
    mpu9250_init()
    
    prev_x, prev_y, prev_z = 0, 0, 0
    
    while True:
        accel_x, accel_y, accel_z = read_accelerometer()
        
        # Düşük geçiren filtre uygulama
        accel_x_filtered = low_pass_filter(accel_x, prev_x)
        accel_y_filtered = low_pass_filter(accel_y, prev_y)
        accel_z_filtered = low_pass_filter(accel_z, prev_z)
        
        print(f"Accel X: {accel_x_filtered}, Accel Y: {accel_y_filtered}, Accel Z: {accel_z_filtered}")
        
        # Gelecek ölçümler için değerleri güncelle
        prev_x, prev_y, prev_z = accel_x_filtered, accel_y_filtered, accel_z_filtered
        
        time.sleep(0.1)  # 0.1 saniye bekle
