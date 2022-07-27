"""

Module df_tools has tools for working with Pandas Dataframes.
Module should be used in a Jupyter Notebook.

import df_tools as d

"""
import importlib
import webbrowser
import pandas as pd

import __main__
# display = __main__.display

def reload():
    """Reloads module"""
    if 'd' in __main__.__dict__:
        importlib.reload(__main__.__dict__['d'])
    else:
        print("Module not reloaded. Import df_tools as d")

__version__ = 1.22


def infos(dfs):
    """Executes info for a list of dataframes"""
    for df in dfs:
        info(df)


def obj_name(df):
    """TODO"""
    ret = "df_foo"
    return ret


def info(df, transpose=False):
    """Prints dataframes size and displays few rows"""
    print(f"{obj_name(df)} {df.shape[0]} rows, {df.shape[1]} columns")
    if transpose:
        display(df.head(3).T)
    else:
        display(df.head(3))

def join_cols(df):
    """Join columns if columns are in multiple levels"""
    df.columns = [c[0] + ('_' + c[1] if c[1] != '' else '') for c in df.columns]


def check_cols(df_1, df_2, index_cols=None, verbose=False):
    """Checks columns of two dataframes. Returns
    - columns only in first
    - columns only in second
    - columns in both """
    if index_cols is None:
        index_cols = []
    cols_1 = [c for c in df_1.columns if not c in df_2.columns]
    cols_2 = [c for c in df_2.columns if not c in df_1.columns]
    cols_12 = [c for c in df_1.columns if c in df_2.columns and not c in index_cols]
    if verbose:
        if not cols_1 > 0:
            only_1_txt = '\n'.join(cols_1)
            print(f"----------- Only in 1 --------------------\n{only_1_txt}")
    if verbose:
        if not cols_2 > 0:
            only_2_txt = '\n'.join(cols_2)
            print(f"----------- Only in 2 --------------------\n{only_2_txt}")
    if verbose:
        if not cols_12 > 0:
            only_12_txt = '\n'.join(cols_12)
            print(f"----------- in both   --------------------\n{only_12_txt}")
    return cols_1, cols_2, cols_12

def test_index(df_1_in, df_2_in, index_cols, verbose=False):
    """Compares dataframes indexes and returns
    rows in the first dataframe thats index does not exist in the second dataframe
    rows in the second dataframe thats index does not exist in the first dataframe
      """
    df_1 = df_1_in.reset_index()
    df_2 = df_2_in.reset_index()
    df_1['original_index'] = df_1.index
    df_2['original_index'] = df_2.index
    cols = ['original_index']
    df_jn = df_1.set_index(index_cols)[cols].join(df_2.set_index(index_cols)[cols], lsuffix='_1', rsuffix='_2', how='outer').reset_index()
    missing_1 = df_1.loc[df_1.original_index.isin(df_jn.loc[df_jn.original_index_2.isna()].original_index_1)]
    missing_2 = df_2.loc[df_2.original_index.isin(df_jn.loc[df_jn.original_index_1.isna()].original_index_2)]
    if verbose:
        print(f"missing df_1 {missing_1.shape[0]} missing df_2 {missing_2.shape[0]}")
    return missing_1, missing_2, df_jn



def join(df_1, df_2, index_cols, how='inner'):
    """Joins df_1 and df_2 with index_cols"""
    jn = df_1.set_index(index_cols).join(df_2.set_index(index_cols), lsuffix='_1', rsuffix='_2', how=how).reset_index()
    return jn


def test_col(df_1, df_2, index_cols, col, verbose=False, return_all=False):
    """Joins df_1 and df_2 with index_cols and sompares given columns. Returns rows that differs"""
    cols = [col]
    jn = df_1.fillna('__NONE__').set_index(index_cols)[cols].join(df_2.fillna('__NONE__').set_index(index_cols)[cols], lsuffix='_df_1', rsuffix='_df_2', how='inner').reset_index()
    jn.loc[:, 'col'] = col
    jn.columns = index_cols +  ['1', '2', 'col']
    if jn['1'].dtype in ['float64'] or jn['2'].dtype in ['float64']:
        jn['1'] = jn['1'].astype(float)
        jn['2'] = jn['2'].astype(float)
    if jn['1'].dtype != jn['2'].dtype:
        if verbose:
            print(f'The dtypes are not same!')
        jn['1'] = jn['1'].astype(str).str.replace(' 00:00:00', '')
        jn['2'] = jn['2'].astype(str)
    jn.loc[jn['1'].astype(str) == '-1', '1'] = ''
    if verbose:
        print(f'{jn.dtypes}')
    jn.fillna('', inplace=True)
    if return_all:
        return jn
    else:
        return jn.loc[jn['1'] != jn['2']].copy(), jn.shape[0]

def test_cols(df_1, df_2, index_cols, cols_pass=None, verbose=False):
    """Test column values"""
    if cols_pass is None:
        cols_pass = ['päivitetty', 'muutosaika', 'muuttaja', 'muutoshetki', 'ymparisto', 'original_index']
    _, _, cols = check_cols(df_1, df_2, index_cols)
    ret = None
    for col in cols:
        if col in cols_pass:
            continue
        ret_iter, row_count = test_col(df_1, df_2, index_cols, col)
        if verbose:
            print(col, ret_iter.shape[0], row_count)
        if ret is None:
            ret = ret_iter
        else:
            ret = ret.append(ret_iter)
    return ret

def as_str(df):
    """Changes dtype as str for all columns in a dataframe"""
    for col in df.columns:
        df[col] = df[col].astype(str)

def test_vals(test, index_cols):
    """Use only with dataframe returned by function test_cols. Makes groupby for test dataframe."""
    ret = test.groupby(['1', '2', 'col']).agg({index_cols[0] : ['count', 'min', 'max']}).reset_index()
    join_cols(ret)
    ret.columns = ['1', '2', 'col', 'cnt', 'example_min', 'example_max']
    ret.sort_values('cnt', ascending=False, inplace=True)
    return ret

def test_col_vals(df_1, df_2, col, verbose=False):
    """Detect separate values that are in only first, only secon or in both of given dataframes"""
    cols_1 = set(df_1[col])
    cols_2 = set(df_2[col])
    only_1 = list(cols_1 - cols_2)
    only_2 = list(cols_2 - cols_1)
    both = list(cols_1 & cols_2)
    if verbose:
        print(len(only_1), len(only_2), len(both))
    return only_1, only_2, both

def value_counts(df, cols, count_col='cnt', sort='descending'):
    """Creates group by given columns with row counts"""
    col = [c for c in df.columns if not c in cols][0]
    ret = df.fillna('NULL').groupby(cols)[col].count()
    ret = ret.to_frame().reset_index()
    ret.columns = cols + [count_col]
    if sort == 'ascending':
        ret.sort_values('cnt', inplace=True)
    if sort == 'descending':
        ret.sort_values('cnt', ascending=False, inplace=True)
    return ret

def value_examples(df, cols, example_col):
    """Creates group by given columns with max and min value for example column"""
    ret = df.fillna('NULL').groupby(cols).agg({example_col : ['min', 'max', 'count']})
    ret = ret.reset_index()
    ret.columns = cols + ['example_min', 'example_max', 'count']
    return ret

def as_integer(sr, default=-1):
    return sr.fillna(default).astype(int)

def value_analysis(df, verbose=False, example_count=3):
    """Analyses dataframe values. Return dataframe with column names as rows"""
    ret = pd.DataFrame(df.columns).set_index(0)
    for col in df.columns:
        vals = df[col].astype(str).fillna('__NONE__').value_counts()
        ret.loc[col, 'separate_values'] = len(vals)
        ret.loc[col, 'null_values'] = df[col].isna().sum()
        for i in range(example_count):
            if i + 1 > len(vals):
                continue
            ret.loc[col, f'val_{i}'] = vals.index[i]
            ret.loc[col, f'cnt_{i}'] = vals[i]
        if verbose:
            print(col)
    int_cols = ['separate_values', 'null_values']
    for col in int_cols:
        ret[col] = as_integer(ret[col])
    for i in range(example_count):
        ret[f'cnt_{i}'] = as_integer(ret[f'cnt_{i}'], default=0)
    return ret

def values(df, verbose=False, encoding='utf-8', name='temp'):
    """"Generates html page for df values and counts"""
    ret = []
    for col in df.columns:
        if verbose:
            print(col)
        ret.append(f'<h2>{col}</h2>')
        vals = df[col].astype(str).value_counts(dropna=False).to_frame().iloc[:50].to_html()
        ret.append(vals)
    with open(f'C:/temp/{name}.html', 'w', encoding=encoding, errors='ignore') as f:
        f.write("".join(ret))
    webbrowser.open(f'C:/temp/{name}.html')

def lower(df):
    """Transform dataframe columns to lower case"""
    df.columns = df.columns.map(lambda x: x.lower())

def from_clipboard(case='lower', header=None):
    """returns contents of the clipboard as a dataframe"""
    # ret_raw = pyperclip.paste()
    if header is None:
        ret = pd.read_clipboard()
    else:
        ret = pd.read_clipboard(header=None)
        ret.columns = header
    if case == 'lower':
        lower(ret)
    return ret


def cols_as_sql(df, prefix=''):
    print("\n    " + "\n    ,".join([prefix + c for c in df.columns]))


print(f"df_tools version {__version__} loaded.")
