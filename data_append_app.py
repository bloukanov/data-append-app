import streamlit as st
import pandas as pd
import datetime as dt
# import numpy as np


## SESSION STATE INITIALIZATIONS
if "fillna_counter" not in st.session_state:
    st.session_state.fillna_counter = 0

if "val_replace_counter" not in st.session_state:
    st.session_state.val_replace_counter = 0

def increment(counter):
    st.session_state[counter] +=1

st.title('Data Appends')

st.header('Base data')
base = st.file_uploader('Upload here', type={"csv", "txt"},key = 1)

if base is not None:
    base_df = pd.read_csv(base)

    st.caption('Data sample')

    strip_ws = st.checkbox("Strip whitespace", value = True)
    if strip_ws:
    # strip whitespace
        for col in base_df.columns:
            try: 
                base_df[col] = base_df[col].str.strip()
            except:
                pass
    st.write(base_df.head())
    

st.subheader('Fill missing values')
if base is not None:
    vars_to_fill = st.multiselect('Select columns with missing values to fill',base_df.columns)
    vars_filling = st.text_input('Enter values to fill in the same order, separated by commas')
    fillna_button = st.button('Fill missing values',on_click=increment,kwargs={'counter':'fillna_counter'})

else: st.write('Awaiting inputs..')
# if 'vars_to_fill' in locals() and 'vars_filling' in locals():
if 'fillna_button' in locals():

    # st.write(vars_to_fill)
    # st.write(vars_filling)


    if st.session_state.fillna_counter > 0:
        # st.write(pd.Series(vars_filling.split(','),index=vars_to_fill).to_dict())
        base_df.fillna(pd.Series(vars_filling.split(','),index=vars_to_fill),inplace=True)
        st.write('Value counts:')
        st.write(base_df.count())
        for var in vars_to_fill:
            st.write(pd.Series(base_df[var].unique()).sort_values())

    # st.session_state.fillna_counter


st.subheader('Values to replace')
if base is not None:
    vars_to_replace = st.multiselect('Select variable(s) whose value you wish to replace',base_df.columns)
    vals_to_replace = st.text_input('''Enter values to be replaced separated by commas for a single variable, 
    separated by a semicolon between variables. No extra spaces!''')
    vals_replacing = st.text_input('''Enter replacement values separated by commas for a single variable, 
    separated by a semicolon between variables. No extra spaces!''')
    replacevars_button = st.button('Replace values',on_click=increment,kwargs={'counter':'val_replace_counter'})
else: st.write('Awaiting inputs..')


# Can also use replace to fill NAs (np.nan)

if 'replacevars_button' in locals():
    if st.session_state.val_replace_counter > 0:

        _vals_to_replace_list = vals_to_replace.split(';')
        vals_to_replace_list = [x.split(',') for x in _vals_to_replace_list]
        for ls in vals_to_replace_list:
            for i in range(len(ls)):
                try:
                    ls[i] = float(ls[i])
                except:
                    pass

        _vals_replacing_list = vals_replacing.split(';')
        vals_replacing_list = [x.split(',') for x in _vals_replacing_list]
        for ls in vals_replacing_list:
            for i in range(len(ls)):
                try:
                    ls[i] = float(ls[i])
                except:
                    pass

        df_map = {vars_to_replace[i]: pd.Series(vals_replacing_list[i],index=vals_to_replace_list[i]).to_dict() for i in range(len(vars_to_replace))}
        # print(df_map)
        st.write(df_map)

        base_df.replace(df_map,inplace=True)

        for var in vars_to_replace:
            st.write(pd.Series(base_df[var].unique()).sort_values())

        st.session_state.replacevars_button = True


st.header('Map data')
map = st.file_uploader("Upload here", type = {'csv','txt'},key = 2)
if map is not None:
    map_df = pd.read_csv(map)
    st.caption('Data sample')
    st.write(map_df.head())


st.header('Columns for join')
if 'base_df' in locals():
    base_join = st.multiselect('Base join column(s)',base_df.columns)
else: st.write('Awaiting inputs..')

if 'map_df' in locals():
    map_join = st.multiselect('Map join column(s)',map_df.columns)
else: st.write('Awaiting inputs..')

if 'base_join' in locals() and 'map_join' in locals():
    merge_button = st.button('Merge')

if 'merge_button' in locals():
    if merge_button:
        result = base_df.merge(map_df,left_on = base_join,right_on = map_join,how='left')
    

# def get_table_download_link(df):
#     """Generates a link allowing the data in a given panda dataframe to be downloaded
#     in:  dataframe
#     out: href string
#     """
#     import base64
#     import datetime as dt
#     b64 = base64.b64encode(df).decode()
#     return f'<a href="data:file/txt;base64,{b64}" download="data_append_{dt.datetime.now().strftime("%Y%m%d%H%M%S")}.csv"><input type="button" value="Download result"></a>'



@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')


st.header('Result')

if 'result' in locals():
    st.caption('Data sample')
    st.write(result.head())
    csv = convert_df(result)
    # st.markdown(get_table_download_link(result.to_csv(index=False).encode()), unsafe_allow_html=True)
    st.download_button(
        label="Download result",
        data=csv,
        file_name=f'data_append_{dt.datetime.now().strftime("%Y%m%d%H%M%S")}.csv',
        mime='text/csv'
    )

else: st.write('Awaiting inputs..')


# st.caption('Please reach out to Bogdan Loukanov (loukanob@mskcc.org) with any questions or issues.')