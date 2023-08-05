from src.ykbio.utility import chr_cmd
from src.ykbio.io.read import pandas_read


def extract_site_from_dataFrame(inputFile, site, header=None, chunkSize=10000, columns=None):
    """
        quickly extract information from relatively large matrix files
        site: chrom:position
        chunkSize: line mumber of iterations
        columns: inputFile: chrom position, default=[0,1] 0-based
    """

    iterDataFrame = pandas_read(inputFile, header=header, iterator=True)
    if not columns:
        columns = [0, 1]

    target_chrom, target_position = site.strip().split(':')

    loop = True
    while loop:
        try:
            chunkDataFrame = iterDataFrame.get_chunk(chunkSize)
            columns_name = chunkDataFrame.columns
            chrom_index = columns_name[columns[0]]
            position_index = columns_name[columns[1]]
            first_chrom = chunkDataFrame.head(1)[chrom_index].values[0]
            if chr_cmd(first_chrom) > chr_cmd(target_chrom):
                return
            elif chr_cmd(first_chrom) <= chr_cmd(target_chrom):
                last_chrom = chunkDataFrame.tail(1)[chrom_index].values[0]
                if chr_cmd(last_chrom) >= chr_cmd(target_chrom):
                    chunkDataFrame = chunkDataFrame[chunkDataFrame[chrom_index] == target_chrom]
                    first_position = chunkDataFrame.head(1)[position_index].values[0]
                    if int(first_position) > int(target_position):
                        return
                    elif int(first_position) <= int(target_position):
                        last_position = chunkDataFrame.tail(1)[position_index].values[0]
                        if int(last_position) >= int(target_position):
                            for index, row in chunkDataFrame.iterrows():
                                position = getattr(row, position_index)
                                if int(position) == int(target_position):
                                    return row.tolist()
        except StopIteration:
            return

