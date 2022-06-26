import numpy as np
from pylatex import Document, LongTable, Table, Tabular, Tabularx
from pylatex.utils import bold

def build_table(doc:Document, data: np.ndarray, col_names: list=None,
                    position_codes:list=None, index:list=None):

    # Get data dimensions
    m, n = data.shape

    # Check if col_names have correct dimension
    if not col_names or len(col_names) != n:
        col_names = [f"col{i}" for i in range(n)]

    # Check if index has correct dimension
    if index and len(index) != m:
        index = None

    # Get (or generate) positional codes
    if not position_codes or len(position_codes) != n:
        position_codes = " ".join("c" for i in range(n))
        if index:
            position_codes = "l | " + position_codes

    # Generate table
    with doc.create(Tabularx(position_codes)) as table:

        # Add header
        if not index:
            table.add_row(col_names, mapper=bold)
        else:
            table.add_row([""] + col_names, mapper=bold)
        table.add_hline()
        #table.end_table_header()
        
        # Add data
        for i in range(m):
            if not index:
                table.add_row([data[i,:]])
            else:
                table.add_row([index[i]] + list(data[i,:]))
        table.add_hline()