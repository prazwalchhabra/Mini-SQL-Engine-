import copy
from parser import parser
from helper import cmp, evaluate, aggregate_evaluate
from importdb import get_table_meta, get_tables


def join(joined,tables,query_tables,ind):

    if ind>=len(query_tables):
        return joined
    
    table = []
    cols = list(tables[query_tables[ind]].keys())
    sz = len(tables[query_tables[ind]][cols[0]])

    for row in joined:
        for i in range(sz):
            r = copy.deepcopy(row)
            for col in cols:
                if str(col) in r:
                    r[str(col)] = -1
                else:
                    r[str(col)] = tables[query_tables[ind]][col][i]
                r[str(query_tables[ind])+"."+str(col)] = tables[query_tables[ind]][col][i]
            table.append(r)
    
    return join(table,tables,query_tables,ind+1)

def solve_where(query,table):
    operators = ['<=' , '>=', '<', '>', '=' ]
    out = set()
    ind = 0
    for opr in operators:
        if query.find(opr)!=-1:
            cols = [ x.strip() for x in query.split(opr)]

            for row in table:
                try:
                    a = evaluate(row,cols[0])
                except:
                    print("error, no entry for '{}'".format(cols[0]))
                    return
                try:
                    b = evaluate(row,cols[1])
                except:
                    print("error, no entry for '{}'".format(cols[1]))
                    return
                if cmp(a,b,opr):
                    out.add(ind)
                ind+=1
            break
    return out

def execute(query,tables):
    # query[0] => select part, query[1] => from part, query[2] => where part (if any)
    
    for table in query[1]:
        if table not in tables.keys():
            print("error , {} does not exists".format(table)) 
            return
    try:
        table = []
        cols = list(tables[query[1][0]].keys())
        sz = len(tables[query[1][0]][cols[0]])

        for i in range(sz):
            row = {}
            for col in cols:
                row[str(col)] = tables[query[1][0]][col][i]
                row[str(query[1][0])+"."+str(col)] = tables[query[1][0]][col][i]
            table.append(row)
    except:
        print("error, after 'from' in query")

    ############## JOIN TABLES  #################
    joined_table = join(table,tables,query[1],1)
    
    ind = 0
    for row in joined_table:
        r = {}
        for col in row:
            # print(row[col])
            if row[col]!=-1:
                r[col] = row[col]
        joined_table[ind]=r
        ind+=1

    ############## SOLVE WHERE CLAUSE  #################
    if len(query[2])>0:
        if query[2].find('or')!=-1:
            query[2] = [ x.strip() for x in query[2].split('or')]
            out = solve_where(query[2][0],joined_table)
            out = out.union(solve_where(query[2][1],joined_table))
        elif query[2].find('and')!=-1:
            query[2] = [ x.strip() for x in query[2].split('and')]
            out = solve_where(query[2][0],joined_table)
            out = out.intersection(solve_where(query[2][1],joined_table))
        else:
            out = solve_where(query[2],joined_table)   
        output_table = []
        for ind in out:
            output_table.append(joined_table[ind])
    else:
        output_table = joined_table

    distinct = False

    ############## SOLVE SELECT  #################
    if query[0][0].startswith('distinct'):
        distinct = True
        query[0][0] = query[0][0][len('distinct'):]


    distinct_set = set()

    ###############  PRINT COLUMN NAMES #################
    if '*' in query[0]:
        if len(query[1])==1:
            cols = list(tables[query[1][0]].keys())
            for key in cols:
                print(key,end="  ")
        else:
            # distkeys = set()
            for key in joined_table[0].keys():
                if '.' in key:# and key.split('.')[1] not in distkeys:
                    # distkeys.add(key.split('.')[1])
                    print(key,end="  ")
    else:
        for cols in query[0]:
            print(cols,end="  ")
    print()


    ######################  AGGREAGATE EVALUATION ##################
    flag = 0
    aggregate_output = []
    for cols in query[0]:
        for aggregates in ['sum', 'average', 'max' , 'min']:
            if cols.find(aggregates)!=-1:

                flag = 1
                temp = [ x.strip() for x in cols.split('(') ]

                try:
                    aggregate_output.append( aggregate_evaluate(temp[0],temp[1][0:len(temp[1])-1],output_table) )
                except:
                    print("error near 'select' in query")
                    return

    if flag:
        for x in aggregate_output:
            print(x,end=' ')
        print()
        return
    ################################################################

    for row in output_table:
        try:
            out = []
            if '*' in query[0]:
                if len(query[1])==1:
                    cols = list(tables[query[1][0]].keys())
                    for col in cols:
                        out.append(row[col])
                    if distinct and tuple(out) in distinct_set:
                        continue
                    else:
                        distinct_set.add(tuple(out))
                        for x in out:
                            print(x,end=" ")
                else:
                    # distkeys = set()
                    for key in row.keys():
                        if '.' in key:
                            # if key.split('.')[1] not in distkeys:
                                # distkeys.add(key.split('.')[1])
                            out.append(row[key])
                    if distinct and tuple(out) in distinct_set:
                        continue
                    else:
                        distinct_set.add(tuple(out))
                        for x in out:
                            print(x,end=" ")
            else:
                for cols in query[0]:
                    out.append(row[cols])
                if distinct and tuple(out) in distinct_set:
                    continue
                else:
                    distinct_set.add(tuple(out))
                    for x in out:
                        print(x,end=" ")
            print()
        except:
            print("error near 'select in query'")
            return
    print()

if __name__ == "__main__":
    filename = "files/metadata.txt"
    metadata = get_table_meta(filename)
    tables = get_tables(metadata)
    
    # for table in tables:
    #     print(table)
    #     for cols in tables[table]:
    #         print(cols,tables[table][cols])

    print("Mini-SQL v0.1")
    while True:
        query = input(">  ")
        while query.endswith(";") == False:
            query = query+input(".. ")
        query = query[0:len(query)-1]
        query = query.lower()
        
        if query in ["quit","q"]:
            break
        
        try:
            parsed_query = parser(query)
            if type(parsed_query)==str and parsed_query.startswith("error"):
                print(parsed_query)
            else:
                # print(parsed_query)
                execute(parsed_query,tables)
        except:
            print("error, executing the command")
