from src.ykbio.io import ykOpen
from src.ykbio.utility import chr_cmd


def intersect_bed(bed1, bed2):
    # todo overlap fraction
    """
        Intersection of two bed
        overlap: all
    """

    iterF = ykOpen(bed1)
    loop1, block = True, list()

    bed_list = ykOpen(bed2).readlines()
    seek, n = 0, 0
    while loop1:
        try:
            line = next(iterF)
            array = line.strip().split('\t')
            chrom_bed1, start_bed1, end_bed1 = array[0], int(array[1]), int(array[2])
            loop2 = True
            while loop2:
                try:
                    chrom_bed2, start_bed2, end_bed2 = bed_list[seek].strip().split('\t')[:3]
                    start_bed2, end_bed2 = int(start_bed2), int(end_bed2)
                    if chr_cmd(chrom_bed1) < chr_cmd(chrom_bed2):
                        loop2 = False
                    elif chr_cmd(chrom_bed1) > chr_cmd(chrom_bed2):
                        seek += 1
                    else:
                        overlap = (max(start_bed1, start_bed2), min(end_bed1, end_bed2))
                        if overlap[0] < overlap[1]:
                            block.append('\t'.join([chrom_bed1, str(overlap[0]), str(overlap[1])]))
                            if overlap[1] == end_bed1:
                                loop2 = False
                            else:
                                seek += 1
                        elif overlap[1] == end_bed1:
                            loop2 = False
                        elif overlap[1] == end_bed2:
                            seek += 1
                except IndexError:
                    return block
        except StopIteration:
            return block
