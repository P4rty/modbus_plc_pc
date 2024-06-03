import serial
import time

def main():
    # 시리얼 포트 설정
    port = 'COM6'  # 자신의 시리얼 포트로 수정
    baud_rate = 9600
    ser = serial.Serial(port, baud_rate, timeout=1)
    time.sleep(2)  # 시리얼 포트가 안정화될 때까지 잠시 대기

    while True:
        # 데이터 프레임 읽기 (4바이트)
        received_bytes = ser.read(4)
        if len(received_bytes) == 4 and received_bytes[0] == 0x02:
            # 체크섬 검증
            temp_int = received_bytes[1]
            humi_int = received_bytes[2]
            checksum = received_bytes[3]
            if checksum == (temp_int + humi_int) & 0xFF:
                print(f"Received Temperature: {temp_int}C, Humidity: {humi_int}%")
            else:
                print("Checksum error")
        else:
            print("Invalid frame received")

        time.sleep(1)

if __name__ == "__main__":
    main()
