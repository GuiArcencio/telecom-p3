PREAMBLE = 0
FRAME = 1

def decode(sig):
    state = PREAMBLE
    ethernet_frame = list()
    last_symbol = 0
    bit_counter = 0
    current_byte = 0

    for symbol in symbols(sig):
        if state == PREAMBLE:
            if last_symbol == 1 and symbol == 1:
                state = FRAME
            last_symbol = symbol
        elif state == FRAME:
            current_byte = current_byte | (symbol << bit_counter)
            
            if bit_counter == 7:
                ethernet_frame.append(current_byte)
                current_byte = 0

            bit_counter = (bit_counter + 1) % 8

    return bytes(ethernet_frame)

def symbols(samples):
    position_counter = 1
    current_level = samples[0]

    for sample in samples[1:]:
        if sample == current_level:
            position_counter += 1
        else:
            # Transition
            if position_counter >= 20:
                # Channel is idle
                return
            if position_counter >= 6:
                position_counter = 0
                yield sample # Symbol is inverse of current level

            current_level = sample