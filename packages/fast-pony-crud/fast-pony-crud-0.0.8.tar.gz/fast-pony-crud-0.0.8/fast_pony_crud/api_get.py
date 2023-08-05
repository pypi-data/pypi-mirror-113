from pony.orm import db_session
from uuid import UUID

@db_session
def api_get(table,kwargs:dict):
    """rest api get method
    Args:
        kwargs (dict): dictionary with {pkey:value} pairs
    Returns:
        list,int : list of entries matching query, status code
    """        
    sql = f"SELECT * FROM {table._table_}"
    first_condition = True
    k = {}
    for key,val in kwargs.items():
        if val is not None and key!="_api_key":
            if type(val)==str:
                query_val = val
            # elif type(val) == UUID:
            #     query_val = val.bytes
            else:
                query_val = str(val)
            k[key]=query_val
            if first_condition == True:
                sql += f' WHERE {key}=${key}'
                first_condition = False
            else:
                sql += f' AND {key}=${key}'
    entries = table.select_by_sql(sql,k)
    return_entries = list()
    for entry in entries:
        dict_entry = entry.to_dict(related_objects=True)
        for col_name in dict_entry:
            if type(dict_entry[col_name]) in table._database_.entities.values():
                if len(type(dict_entry[col_name])._pk_attrs_)>1:
                    dict_entry[col_name] = dict_entry[col_name].to_dict()
                else:
                    dict_entry[col_name] = getattr(dict_entry[col_name], type(dict_entry[col_name])._pk_attrs_[0].name)
        return_entries.append(dict_entry)

    return return_entries