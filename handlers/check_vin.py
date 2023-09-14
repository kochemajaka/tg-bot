import re

def IF_VIN(message):
    if re.fullmatch("[АВЕКМНОРСТУХ]\d{3}(?<!000)[АВЕКМНОРСТУХ]{2}\d{2,3}", message):
        # конвертация госномера в вин
        VIN = message
        return VIN
    elif re.fullmatch("(?=.*\d|=.*[A-Z])(?=.*[A-Z])[A-Z0-9]{17}", message):
        VIN = message
        return VIN
    return False