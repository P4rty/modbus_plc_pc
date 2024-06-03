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