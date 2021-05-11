# purpose: to read (KC705-TDC's) raw binary file with some options

import os
import sys

# handle command line options
from argparse import ArgumentParser


class pycolor:
    # use as print(pycolor.RED, 'foo', pycolor.END)
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    RETURN = '\033[07m'
    ACCENT = '\033[01m'
    FLASH = '\033[05m'
    RED_FLASH = '\033[05;41m'
    END = '\033[0m'


def get_option():
    # define command line options
    argparser = ArgumentParser()
    argparser.add_argument(
        '-f', '--file', required=True, type=str, default=None, help='path to file')
    argparser.add_argument(
        '-d', '--decode', action='store_true', help='enable decoder')
    argparser.add_argument(
        '-df', '--diff', action='store_true', help='enable print diff of tdc')
    argparser.add_argument(
        '-hd', '--header', action='store_true', help='disable print header')
    argparser.add_argument(
        '-ft', '--footer', action='store_true', help='disable print footer')
    argparser.add_argument(
        '-td', '--tdc', action='store_true', help='disable print tdc')

    return argparser.parse_args()


# bits
BITS_SIZE_BOARDID = 4
BITS_SIZE_SPILLCOUNT = 16
BITS_SIZE_EMCOUNT = 16
BITS_SIZE_WRITECOUNT = 32
BITS_SIZE_HEADER_UPPER = 32
BITS_SIZE_HEADER_LOWER = 48
BITS_SIZE_FOOTER_UPPER = 32
BITS_SIZE_FOOTER_LOWER = 8
BITS_SIZE_SIG_MPPC = 64
BITS_SIZE_SIG_PMT = 12
BITS_SIZE_SIG_MRSYNC = 1
BITS_SIZE_TDC = 27

# use for 1 word of 104 bits
BITS_WORD_HEADER_UPPER = (0x01234567
                          << (BITS_SIZE_SPILLCOUNT + 4 + BITS_SIZE_BOARDID + BITS_SIZE_HEADER_LOWER))
BITS_WORD_HEADER_LOWER = 0x0123456789AB
BITS_WORD_FOOTER_UPPER = (0xAAAAAAAA
                          << (BITS_SIZE_SPILLCOUNT + BITS_SIZE_EMCOUNT + BITS_SIZE_WRITECOUNT + BITS_SIZE_FOOTER_LOWER))
BITS_WORD_FOOTER_LOWER = 0xAB

# use for 1 word of 104 bits, only the corresponding bits are filled with 1
BITS_MASK_HEADER_UPPER = ((2 ** BITS_SIZE_HEADER_UPPER - 1)
                          << (BITS_SIZE_SPILLCOUNT + 4 + BITS_SIZE_BOARDID + BITS_SIZE_HEADER_LOWER))
BITS_MASK_HEADER_LOWER = 2 ** BITS_SIZE_HEADER_LOWER - 1
BITS_MASK_FOOTER_UPPER = ((2 ** BITS_SIZE_FOOTER_UPPER - 1)
                          << (BITS_SIZE_SPILLCOUNT + BITS_SIZE_EMCOUNT + BITS_SIZE_WRITECOUNT + BITS_SIZE_FOOTER_LOWER))
BITS_MASK_FOOTER_LOWER = 2 ** BITS_SIZE_FOOTER_LOWER - 1
BITS_MASK_SPILLCOUNT_HEADER = ((2 ** BITS_SIZE_SPILLCOUNT - 1)
                               << (4 + BITS_SIZE_BOARDID + BITS_SIZE_HEADER_LOWER))
BITS_MASK_SPILLCOUNT_FOOTER = ((2 ** BITS_SIZE_SPILLCOUNT - 1)
                               << (BITS_SIZE_EMCOUNT + BITS_SIZE_WRITECOUNT + BITS_SIZE_FOOTER_LOWER))
BITS_MASK_BOARDID = ((2 ** BITS_SIZE_BOARDID - 1)
                     << (BITS_SIZE_HEADER_LOWER))
BITS_MASK_EMCOUNT = ((2 ** BITS_SIZE_EMCOUNT - 1)
                     << (BITS_SIZE_WRITECOUNT + BITS_SIZE_FOOTER_LOWER + 8))
BITS_MASK_WRITECOUNT = ((2 ** BITS_SIZE_WRITECOUNT - 1)
                        << (BITS_SIZE_FOOTER_LOWER + 8))

BITS_MASK_SIG_MPPC = ((2 ** BITS_SIZE_SIG_MPPC - 1)
                      << (BITS_SIZE_SIG_PMT + BITS_SIZE_SIG_MRSYNC + BITS_SIZE_TDC))

BITS_MASK_SIG_PMT = ((2 ** BITS_SIZE_SIG_PMT - 1)
                     << (BITS_SIZE_SIG_MRSYNC + BITS_SIZE_TDC))
BITS_MASK_SIG_MRSYNC = ((2 ** BITS_SIZE_SIG_MRSYNC - 1)
                        << BITS_SIZE_TDC)
BITS_MASK_TDC = 2 ** BITS_SIZE_TDC - 1


def header_or_not(data):
    if ((data & (BITS_MASK_HEADER_UPPER | BITS_MASK_HEADER_LOWER)) == (BITS_WORD_HEADER_UPPER | BITS_WORD_HEADER_LOWER)):
        return True
    else:
        return False


def footer_or_not(data):
    if ((data & (BITS_MASK_FOOTER_UPPER | BITS_MASK_FOOTER_LOWER)) == (BITS_WORD_FOOTER_UPPER | BITS_WORD_FOOTER_LOWER)):
        return True
    else:
        return False


def get_spillcount_header(data):
    return ((data & BITS_MASK_SPILLCOUNT_HEADER) >> (4 + BITS_SIZE_BOARDID + BITS_SIZE_HEADER_LOWER))


def get_spillcount_footer(data):
    return ((data & BITS_MASK_SPILLCOUNT_FOOTER) >> (BITS_SIZE_EMCOUNT + BITS_SIZE_WRITECOUNT + BITS_SIZE_FOOTER_LOWER))


def get_boardid(data):
    return ((data & BITS_MASK_BOARDID) >> (BITS_SIZE_HEADER_LOWER))


def get_emcount(data):
    return ((data & BITS_MASK_EMCOUNT) >> (BITS_SIZE_WRITECOUNT + BITS_SIZE_FOOTER_LOWER + 8))


def get_writecount(data):
    return ((data & BITS_MASK_WRITECOUNT) >> (BITS_SIZE_FOOTER_LOWER + 8))


def get_sig_mppc(data):
    return ((data & BITS_MASK_SIG_MPPC) >> (BITS_SIZE_SIG_PMT + BITS_SIZE_SIG_MRSYNC + BITS_SIZE_TDC))


def get_sig_pmt(data):
    return ((data & BITS_MASK_SIG_PMT) >> (BITS_SIZE_SIG_MRSYNC + BITS_SIZE_TDC))


def get_sig_mrsync(data):
    return ((data & BITS_MASK_SIG_MRSYNC) >> (BITS_SIZE_TDC))


def get_tdc(data):
    return (data & BITS_MASK_TDC)


def main(path_to_file):
    # 1 word, bytes
    DATA_UNIT = 13

    with open(path_to_file, 'rb') as f:
        while f.tell() != os.path.getsize(path_to_file):
            bytearray_13bytes = f.read(DATA_UNIT)
            int_13bytes = int.from_bytes(bytearray_13bytes, 'big')

            line_num = int(f.tell() / 13) - 1

            if header_or_not(int_13bytes):
                # header
                if args.header:
                    # disable
                    pass
                else:
                    if args.decode:
                        # decode
                        print(pycolor.RED, 'no.', str(line_num), ':',
                              'spillcount:',
                              get_spillcount_header(int_13bytes),
                              'boardid:',
                              get_boardid(int_13bytes), pycolor.END)
                    else:
                        # raw
                        print(pycolor.RED, 'no.', str(line_num), ':',
                              ' '.join(['{:02x}'.format(x) for x in bytearray_13bytes]), pycolor.END)
            elif footer_or_not(int_13bytes):
                # footer
                if args.footer:
                    # disable
                    pass
                else:
                    if args.decode:
                        # decode
                        print(pycolor.BLUE, 'no.', str(line_num), ':',
                              'spillcount:',
                              get_spillcount_footer(int_13bytes),
                              'emcount:',
                              get_emcount(int_13bytes),
                              'writecount:',
                              get_writecount(int_13bytes), pycolor.BLUE)
                    else:
                        # raw
                        print(pycolor.BLUE, 'no.', str(line_num), ':',
                              ' '.join(['{:02x}'.format(x) for x in bytearray_13bytes]), pycolor.END)
            else:
                # tdc
                if args.tdc:
                    # disable
                    pass
                else:
                    if args.diff:
                        # diff
                        tdc_latest = get_tdc(int_13bytes)
                        if 'tdc_old' in locals():
                            tdc_diff = tdc_latest - tdc_old
                        else:
                            tdc_diff = 'None'
                        tdc_old = tdc_latest

                        diff_print = pycolor.GREEN \
                            + ' diff:' + str(tdc_diff) \
                            + pycolor.END + '\n'
                    else:
                        diff_print = '\n'

                    if args.decode:
                        # decode
                        # insert space every 4 digits
                        # 79 = 64(bits) + (64/4 - 1)(spaces)
                        mppc_bitfield \
                            = format(get_sig_mppc(int_13bytes), '079_b')
                        mppc_transtable \
                            = mppc_bitfield.maketrans('01_', '-* ')
                        mppc_print \
                            = mppc_bitfield.translate(mppc_transtable)

                        # 14 = 12(bits) + (12/4 - 1)(spaces)
                        pmt_bitfield \
                            = format(get_sig_pmt(int_13bytes), '014_b')
                        pmt_transtable \
                            = pmt_bitfield.maketrans('01_', '-* ')
                        pmt_print \
                            = pmt_bitfield.translate(pmt_transtable)

                        mrsync_bitfield \
                            = format(get_sig_mrsync(int_13bytes), '01_b')
                        mrsync_transtable \
                            = mrsync_bitfield.maketrans('01_', '-* ')
                        mrsync_print \
                            = mrsync_bitfield.translate(mrsync_transtable)

                        print('no.', str(line_num), ':',
                              'mppc:', mppc_print,
                              'pmt:', pmt_print,
                              'mrsync:', mrsync_print, pycolor.GREEN,
                              'tdc:', get_tdc(int_13bytes), pycolor.END, end=diff_print)
                    else:
                        # raw
                        print('no.', str(line_num), ':',
                              ' '.join(['{:02x}'.format(x) for x in bytearray_13bytes]), end=diff_print)


if __name__ == '__main__':
    args = get_option()

    path_to_file = args.file
    print('path_to_file:', path_to_file)
    main(path_to_file)
