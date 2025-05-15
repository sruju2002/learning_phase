# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
from snowflake.snowpark.session import session

session = session.builder.configs(st.secrets["connections"]["snowflake"]).create()

# Write directly to the app
st.title(f":cup_with_straw: Customize your smoothie! :cup_with_straw: ")
st.write(
  """Choose the fruits you want in custom Smoothie!
  """
)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on the Smoothie will be:  ", name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose upto 5 Ingredeints:', my_dataframe,max_selections=5
)
if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
    #st.write(ingredients_string)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

time_to_insert= st.button('Submit Order')

#st.write(my_insert_stmt)


if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")

cnx=st.connection("snowflake")
session=cnx.session()

