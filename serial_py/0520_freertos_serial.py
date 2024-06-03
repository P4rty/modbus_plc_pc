import time
import serial

# 시리얼 포트 설정
ser = serial.Serial('COM6', 115200)

while True:
    # 4개의 0, 1을 스페이스바로 구분하여 입력받기
    input_values = input("4개의 0과 1을 입력: ").split()

    # 입력받은 문자열을 정수 리스트로 변환
    if len(input_values) == 4:
        try:
            integer_values = list(map(int, input_values))
            
            # 정수 값을 16진수 문자열로 변환
            hex_string = ''.join(format(i, '02X') for i in integer_values)
            
            # 문자열을 바이트로 변환
            hex_bytes = bytes.fromhex(hex_string)
            
            # 바이트 보내기
            ser.write(hex_bytes)
            
            # 전송된 바이트 출력
            print("보낸 바이트:", hex_bytes)
            
            # 켜진 LED 상태 받기
            time.sleep(1)  # 잠시 대기 (필요에 따라 조정)
            if ser.in_waiting > 0:
                received_data = ser.read(ser.in_waiting)
                print("받은 바이트:", received_data)
                
                # 받은 데이터를 16진수 문자열로 변환
                received_hex = received_data.hex().upper()
                print("받은 16진수 문자열:", received_hex)
                
                # 받은 데이터를 각 LED 상태로 해석
                led_states = [int(received_hex[i:i+2], 16) for i in range(0, len(received_hex), 2)]
                print("LED 상태:", led_states)
            else:
                print("받은 데이터가 없습니다.")
                
        except ValueError:
            print("0과 1로만 구성된 4개의 정수를 입력해주세요.")
    else:
        print("4개의 정수를 정확히 입력해주세요.")

    time.sleep(1)
