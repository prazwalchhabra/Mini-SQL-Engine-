import numpy as np

def get_table_meta(filename):    
   
    with open(filename) as f:
        metadata = f.readlines()

    metadata = [ x.strip() for x in metadata ]

    values = np.asarray(metadata)
    begin_indices = np.where(values == "<begin_table>")[0]

    values = np.asarray(metadata)
    end_indices = np.where(values == "<end_table>")[0]

    tables = {}

    for i in range(begin_indices.shape[0]):
        temp = metadata[begin_indices[i]+1:end_indices[i]]
        tables[temp[0]] = temp[1:len(temp)]

    return tables


def get_tables(metadata):
    data = {}
    for table in metadata:
        d = {}
        with open("files/"+table+".csv", 'r') as f:
            temp = f.readlines()
        temp = [ str(x.strip()).split(',') for x in temp ]
        temp = np.asarray(temp)

        for i in range(len(metadata[table])):
            # np.dtype(('i4', temp[:,i]))
            d[metadata[table][i].lower()] = [ int(str(x)) for x in temp[:,i] ]
        data[str(table)] = d
    return data
