import serial
import requests
import time

# Flask 서버 주소
server_url = "http://:5000/data"

def send_data_to_server(data):
    response = requests.post(server_url, json=data)
    print(response.json())

def DA_CMD_Data_LRC(DA, CMD, Data):
    DA_h = [hex(ord(char))[2:] for char in DA]
    CMD_h = [hex(ord(char))[2:] for char in CMD]
    Data_h = [hex(ord(char))[2:] for char in Data]
    total_h = DA_h + CMD_h + Data_h
    total_sum = sum(int(hex_value, 16) for hex_value in total_h)
    # 2의 보수 계산
    LRC_inv_b = bin((~total_sum + 1) & 0xFF)
    LRC_inv_h = hex(int(LRC_inv_b, 2))
    LRC_inv_h_1 = hex(ord(LRC_inv_h[2]))
    LRC_inv_h_2 = hex(ord(LRC_inv_h[3]))
    LRC_inv_h_1 = int(LRC_inv_h_1, 16)
    LRC_inv_h_2 = int(LRC_inv_h_2, 16)
    if LRC_inv_h_1 >= 97:
        LRC_inv_h_1 = LRC_inv_h_1 - 32
    if LRC_inv_h_2 >= 97:
        LRC_inv_h_2 = LRC_inv_h_2 - 32
    LRC_inv_h_1 = hex(LRC_inv_h_1)
    LRC_inv_h_2 = hex(LRC_inv_h_2)
    DA = ' '.join([f"{ord(char):02X}" for char in DA])
    CMD = ' '.join([f"{ord(char):02X}" for char in CMD])
    Data = [ord(char) for char in Data]
    Data = " ".join([f"{d:02X}" for d in Data])
    st = '3A'
    end_1 = '0D'
    end_2 = '0A'
    frame_tmp = f'{st}{DA}{CMD}{Data}{LRC_inv_h_1[2:]}{LRC_inv_h_2[2:]}{end_1}{end_2}'
    frame = bytes.fromhex(frame_tmp)
    return frame

def main():
    # 시리얼 포트 설정
    port_sensor = 'COM6'  # 자신의 센서 시리얼 포트로 수정
    port_controller_plc = 'COM7'  # 자신의 컨트롤러 시리얼 포트로 수정
    baud_rate = 9600

    ser_sensor = serial.Serial(port_sensor, baud_rate, timeout=1)
    ser_controller_plc = serial.Serial(port_controller_plc, baud_rate, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
    
    time.sleep(2)  # 시리얼 포트 안정화를 위한 대기

    while True:
        # 아두이노로부터 데이터 프레임 읽기 (5바이트)
        received_bytes = ser_sensor.read(5)
        if len(received_bytes) == 5 and received_bytes[0] == 0x02:
            # 체크섬 검증
            temp_int = received_bytes[1]
            humi_int = received_bytes[2]
            moist_int = received_bytes[3]
            checksum = received_bytes[4]
            if checksum == (temp_int + humi_int + moist_int) & 0xFF:
                print(f"Received Temperature: {temp_int}C, Humidity: {humi_int}%, Moisture: {moist_int}%")
                # PLC로 데이터 전송
                ser_controller_plc.write(DA_CMD_Data_LRC('01', '04', f'{temp_int:02d}{humi_int:02d}{moist_int:02d}00'))
            else:
                print("Checksum error")
        else:
            print("Invalid frame received")

        # 아두이노 데이터를 Flask 서버로 전송
        if ser_sensor.in_waiting > 0:
            line = ser_sensor.readline().decode('utf-8').rstrip()
            print(f"Received: {line}")
            data = {"sensor_value": line}
            send_data_to_server(data)

if __name__ == "__main__":
    main()
