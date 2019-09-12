
def parser(query):
    query = query.lower()

    ################### from parser ######################
    if query.find("from")==-1:
        return "error in syntax, a query without 'from'"
    else:
        parsed_query = query.split("from")

    ################### select parser ######################
    if parsed_query[0].strip().startswith("select")==False:
        return "error in syntax with 'select'"
    else:
        parsed_query[0] = str(parsed_query[0].strip().split("select")[1]).strip()
        if '*' in parsed_query[0]:
            temp = parsed_query[0]
            if parsed_query[0].startswith('distinct'):
                temp = parsed_query[0][len('distinct'):].strip()
            if len(temp)>1:
                return "error in syntax near select"

    # get all columns in query
    columns = str(parsed_query[0]).strip().split(",")
    if '' in columns:
        return "error in syntax"
    columns = [x.strip().replace(" ","") for x in columns]
    parsed_query[0] = columns

    ################### where parser ######################
    if parsed_query[1].strip().find('where')!=-1:
        parsed_where_query = parsed_query[1].strip().split('where')
        parsed_query[1] = [x.strip() for x in parsed_where_query[0].strip().split(',') ]
        parsed_query.append(str(parsed_where_query[1].strip()))
    else:
        parsed_query[1] = [x.strip() for x in parsed_query[1].strip().split(',') ]
        parsed_query.append("")

    return parsed_query
