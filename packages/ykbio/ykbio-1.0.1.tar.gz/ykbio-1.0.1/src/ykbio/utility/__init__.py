from src.ykbio.message import Message


def chr_cmd(chr):
    if isinstance(chr, str):
        if chr.isdigit():
            return int(chr)
        else:
            if chr.split('chr')[-1] == 'X':
                return 23
            elif chr.split('chr')[-1] == 'Y':
                return 24
            elif chr.split('chr')[-1] == 'M':
                return 25
            return int(chr.split('chr')[-1])
    elif isinstance(chr, int):
        return chr
    else:
        raise Message(f'{chr} chromosome format is not supported')
