import serial
import time

# 아두이노와의 시리얼 포트 설정 (적절한 포트로 변경)
ser = serial.Serial('COM7', 9600)  # Windows 예시
# ser = serial.Serial('/dev/ttyACM0', 9600)  # Linux 예시

time.sleep(2)  # 시리얼 포트 초기화 시간 대기

def send_command(command):
    ser.write((command + '\n').encode())
    time.sleep(0.1)  # 명령어 전송 후 잠시 대기
    response = ser.readline().decode().strip()  # 아두이노로부터의 응답 읽기
    print("Arduino:", response)

while True:
    # 사용자로부터 명령어 입력 받기
    cmd = input("Enter command: ")
    send_command(cmd)
