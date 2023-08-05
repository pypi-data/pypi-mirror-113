import gzip
import zipfile
import pandas as pd

from pathlib import Path
from collections import defaultdict

compression_dict = defaultdict(lambda: 'infer')

compression_dict.update({
    '.gz': 'gzip',
    '.zip': 'zip',
    '.bz2': 'bz2',
    '.xz': 'xz'
})


def pandas_read(file, comment='#', header=None, sep='\t', **kwargs):
    """

    read file by pandas

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
