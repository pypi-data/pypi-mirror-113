import gzip
import zipfile
import pandas as pd

from pathlib import Path
from collections import defaultdict

from src.ykbio.message import Message
from src.ykbio.utility import chr_cmd

compression_dict = defaultdict(lambda: 'infer')

compression_dict.update({
    '.gz': 'gzip',
    '.zip': 'zip',
    '.bz2': 'bz2',
    '.xz': 'xz'
})


def pandas_read(file, comment='#', header=None, sep='\t', **kwargs):
    # todo : Support excel format reading
    """

    read file by pandas,

    """
    compression = compression_dict[Path(file).suffix]
    iterator = kwargs.get('iterator', False)
    keep_default_na = kwargs.get('keep_default_na', True)

    try:
        dataframe = pd.read_csv(file, comment=comment, compression=compression, header=header,
                                sep=sep, iterator=iterator, low_memory=False, keep_default_na=keep_default_na)
    except pd.errors.ParserError:
        print('The file format cannot be parsed !!!')

    return dataframe


def ykOpen(inputFile):
    """
    common read, zip format file can only read the first file
    """
    if inputFile.endswith('gz'):
        return gzip.open(inputFile, 'rb')
    elif inputFile.endswith('.zip'):
        inputFile = zipfile.ZipFile(inputFile, "r").namelist()[0]
    return open(inputFile)


def iter_file_by_line(inputFile, number=4, header=False, contain=False):
    """
        File iteration by line
        contain false output not contain header
    """
    iterF = ykOpen(inputFile)
    loop, block = True, list()
    if header and contain:
        header = next(iterF)
        block.append(header)
    else:
        contain = False

    if not isinstance(number, int):
        raise Message(f'second parameter must be int, not {type(number)}')
    n = 0
    while loop:
        try:
            line = next(iterF)
            if n % number == 0 and n != 0:
                yield block
                block = list()
                if contain:
                    block.append(header)
                block.append(line)
            else:
                block.append(line)
            n += 1
        except StopIteration:
            loop = False
            if len(block) >= 1:
                yield block


def iter_file_by_tag(inputFile, start, end, header=False, contain=False):
    """
        File iteration by content
        start: block start
        end: block end
        contain false output not contain header
    """
    iterF = ykOpen(inputFile)
    loop, block = True, list()
    if header and contain:
        header = next(iterF)
    else:
        contain = False
    while loop:
        try:
            line = next(iterF)
            if line.strip() == start:
                if contain:
                    block.append(header)
                block.append(line)
            elif line.strip() == end:
                block.append(line)
                yield block
                block = list()
            else:
                block.append(line)
        except StopIteration:
            loop = False


def iter_file_by_bed(inputFile, bed, column=None, header=False, contain=False):
    """
        One line of the input file represents one coordinate point
        Extract from the input file according to the bed area
        bed: chrom start end
        inputFile: chrom position, default=[0,1] 0-based
    """
    if not column:
        column = [0, 1]

    iterF = ykOpen(inputFile)
    loop1, block = True, list()
    if header and contain:
        header = next(iterF)
    else:
        contain = False

    bed_list = ykOpen(bed).readlines()
    seek, n = 0, 0
    while loop1:
        try:
            line = next(iterF)
            array = line.strip().split('\t')
            chrom, position = array[column[0]], int(array[column[1]])
            loop2 = True
            while loop2:
                try:
                    chrom_bed, start, end = bed_list[seek].strip().split('\t')[:3]
                    if chr_cmd(chrom) < chr_cmd(chrom_bed):
                        loop2 = False
                    elif chr_cmd(chrom) > chr_cmd(chrom_bed):
                        seek += 1
                    else:
                        if int(start) <= position <= int(end):
                            if n == 0 and contain:
                                block.append(header)
                                n = 1
                            block.append(line)
                            loop2 = False
                        elif position <= int(start):
                            loop2 = False
                        elif position >= int(end):
                            if len(block) >= 1:
                                yield block
                                block = list()
                                n = 0
                            seek += 1
                except IndexError:
                    loop1, loop2 = False, False
        except StopIteration:
            loop1 = False
