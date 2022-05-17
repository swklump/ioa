from pandas import DataFrame

def get_elementname(root,prefix,var):
    element_name = root[0].attrib[var]
    if prefix in element_name:
        element_name = element_name.replace(prefix, '').strip()
    return element_name

def get_vals_other(var_list, cols_list, child, element_name, df):
    for k in range(len(var_list)):
        if var_list[k] == element_name:
            pass
        else:
            try:
                var_list[k] = child.attrib[var_list[k]]
            except KeyError:
                var_list[k] = ''

    df = df.append(DataFrame([var_list], columns=cols_list), ignore_index=True)

    return df