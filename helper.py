
def cmp(a,b,operator):
    if operator=='<':
        if a<b:
            return True
        else:
            return False
    if operator=='>':
        if a>b:
            return True
        else:
            return False
    if operator=='<=':
        if a<=b:
            return True
        else:
            return False
    if operator=='>=':
        if a>=b:
            return True
        else:
            return False
    if operator=='=':
        if a==b:
            return True
        else:
            return False

def aggregate_evaluate(aggregate,col,table):
    if aggregate =='sum':
        ans = 0
        for row in table:
            ans+=int(row[col])
        return ans
    if aggregate =='average':
        ans = 0
        n = 0
        for row in table:
            ans+=int(row[col])
            n+=1
        if len(table)>0:
            return ans/n
        else:
            return 0
    if aggregate =='max':
        if len(table)>0:
            ans = table[0][col]
        else:
            return '-'
        for row in table:
            ans = max(ans,int(row[col]))
        return ans
    if aggregate=='min':
        if len(table)>0:
            ans = table[0][col]
        else:
            return '-'
        for row in table:
            ans = min(ans,int(row[col]))
        return ans

def evaluate(row,col):
    if col.isnumeric():
        a = int(col)
    else:
        a = row[col]
    return a
