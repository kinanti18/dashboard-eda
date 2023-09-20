import pandas as pd 
import streamlit as st
import plotly.express as px


# Load the datasets (replace these with your dataset paths)
customers_df = pd.read_csv('https://raw.githubusercontent.com/kinanti18/dashboard-eda/main/data/dataset_clean/customers_df.csv')
orders_df = pd.read_csv('https://raw.githubusercontent.com/kinanti18/dashboard-eda/main/data/dataset_clean/orders_df.csv')
products_df = pd.read_csv('https://raw.githubusercontent.com/kinanti18/dashboard-eda/main/data/dataset_clean/products_df.csv')
order_items_df = pd.read_csv('https://raw.githubusercontent.com/kinanti18/dashboard-eda/main/data/dataset_clean/order_items_df.csv')
order_payments_df = pd.read_csv('https://raw.githubusercontent.com/kinanti18/dashboard-eda/main/data/dataset_clean/order_payments_df.csv')
order_reviews_df = pd.read_csv('https://raw.githubusercontent.com/kinanti18/dashboard-eda/main/data/dataset_clean/order_reviews_df.csv')
sellers_df = pd.read_csv('https://raw.githubusercontent.com/kinanti18/dashboard-eda/main/data/dataset_clean/sellers_df.csv')


# Title and subheader
st.title("E-commerce Data Analysis")

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["Customer Analysis", "Product Analysis", "Order Analysis", 
"Seller Analysis", "Payment Analysis", "Review Analysis", "Delivery Performance", "Translation Analysis"])

#============================Customer Analysis============================#
#============================Start============================#
with tab1:
    #----------------------------------------------------------------#
    # Question 1: What is the geographical distribution of customers (by zip code, city, state)?
    st.subheader("Geographical Distribution of Customers")

    # Create a bar plot to show the count of customers by state
    st.write("Geographical Distribution by State")
    state_counts = customers_df['customer_state'].value_counts()
    st.bar_chart(state_counts)
    st.divider() 

    # Create a bar plot to show the count of customers by city
    st.write("Geographical Distribution by City")
    city_counts = customers_df['customer_city'].value_counts()
    st.bar_chart(city_counts)
    st.divider() 

    # Create a bar plot to show the count of customers by zip code
    st.write("Geographical Distribution by Zip Code")
    customer_zip_code_prefix_counts = customers_df['customer_zip_code_prefix'].value_counts()
    st.bar_chart(customer_zip_code_prefix_counts)
    st.divider() 

    #----------------------------------------------------------------#
    # Question 2: What are the most common customer states or cities?
    st.subheader("Most Common Customer States and Cities")

    # Calculate the most common customer states 
    common_states = customers_df['customer_state'].value_counts().head(3)

    # Calculate the most common customer city 
    common_cities = customers_df['customer_city'].value_counts().head(3)

    # Create bar plots for common states and cities
    st.write("Most Common Customer States")
    st.bar_chart(common_states)
    st.divider() 
    st.write("Most Common Customer Cities")
    st.bar_chart(common_cities)
    st.divider() 
    #----------------------------------------------------------------#
    # Question 3: What is the average order value per customer?
    st.subheader("Average Order Value per Customer")
    
    # Merge the 'orders_df' and 'payments_df' on 'order_id' to get order payment details
    merged_df = pd.merge(orders_df, order_payments_df, on='order_id')

    # Calculate the total payment (order value) for each order
    merged_df['total_payment'] = merged_df['payment_value']

    # Group orders by 'customer_id' and calculate the average order value per customer
    average_order_value = merged_df.groupby('customer_id')['total_payment'].mean().reset_index()
    average_order_value.columns = ['Customer ID', 'Average Order Value']

    fig = px.histogram(average_order_value, x="Average Order Value", nbins=20)
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    st.divider() 
#============================End============================#

#============================Product Analysis============================#
#============================Start============================#

with tab2:
    #----------------------------------------------------------------#
    # Question 4: What are the top-selling product categories?
    st.subheader("Top-Selling Product Categories")
    # Merge the 'order_items_df' and 'products_dataset_df' on 'product_id' to get product details
    merged_df = pd.merge(order_items_df, products_df, on='product_id')

    # Group products by 'product_category_name' and calculate the total quantity sold in each category
    top_selling_categories = merged_df.groupby('product_category_name')['order_item_id'].sum().reset_index().head(10)
    top_selling_categories.columns = ['Product Category', 'Total Quantity Sold']

    # Sort the categories by total quantity sold in descending order to find the top sellers
    top_selling_categories = top_selling_categories.sort_values(by='Total Quantity Sold', ascending=False)

    fig = px.histogram(top_selling_categories, x="Product Category", nbins=20)
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    st.divider() 
#============================End============================#

#============================Order Analysis============================#
#============================Start============================#
with tab3:
    #----------------------------------------------------------------#
    # Question 5: How long does it take on average for an order to be delivered?
    st.subheader("Average Delivery Time")
    
    # Convert the relevant date columns to datetime objects
    orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'])
    orders_df['order_delivered_customer_date'] = pd.to_datetime(orders_df['order_delivered_customer_date'])

    # Calculate the delivery time for each order in days
    orders_df['delivery_time'] = (orders_df['order_delivered_customer_date'] - orders_df['order_purchase_timestamp']).dt.days

    # Calculate the average delivery time
    average_delivery_time = orders_df['delivery_time'].mean()
    
    st.write(f"Average Delivery Time: {average_delivery_time}")
    st.divider() 
    #----------------------------------------------------------------#
    # Question 6: What is the average number of items per order?
    st.subheader("Average Number of Items per Order")
    # Calculate average number of items per order
    avg_items_per_order = order_items_df.groupby('order_id')['order_item_id'].count().mean()
    # Display the result
    st.write(f"Average Number of Items per Order: {avg_items_per_order:.2f}")
    st.divider() 
    
    #----------------------------------------------------------------#
    # Question 7: What is the typical payment method used by customers?
    st.subheader("Typical Payment Method")
    # Calculate the most common payment method
    common_payment_method = order_payments_df['payment_type'].mode().values[0]
    # Display the result
    st.write(f"Most Common Payment Method: {common_payment_method}")
    st.divider() 
#============================End============================#


#============================Seller Analysis============================#
#============================Start============================#
with tab4:
#----------------------------------------------------------------#
    # Question 8: Who are the top-performing sellers in terms of sales and customer satisfaction?
    st.subheader("Top-Performing Sellers")

    # Merge the 'order_items_df' and 'order_reviews_df' on 'order_id' to get order item details and review scores
    merged_df = pd.merge(order_items_df, order_reviews_df, on='order_id')

    # Group sellers by 'seller_id' and calculate total sales and average review score
    seller_performance = merged_df.groupby('seller_id').agg({'order_item_id': 'sum', 'review_score': 'mean'}).reset_index()
    seller_performance.columns = ['Seller ID', 'Total Sales', 'Average Review Score']

    # Sort sellers by total sales in descending order
    top_sellers_sales = seller_performance.sort_values(by='Total Sales', ascending=False).head(10)

    # Sort sellers by average review score in descending order
    top_sellers_satisfaction = seller_performance.sort_values(by='Average Review Score', ascending=False).head(10)
    
    # Create chart
    fig = px.histogram(top_sellers_satisfaction, x="Seller ID", nbins=20)
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    st.divider() 
#----------------------------------------------------------------#
    # Question 9: What is the geographical distribution of sellers?
    st.subheader("Geographical Distribution of Sellers")
    # Group sellers by state and count the number of sellers in each state
    seller_distribution = sellers_df['seller_state'].value_counts().reset_index()
    seller_distribution.columns = ['State', 'Number of Sellers']
    
    # Create chart
    fig = px.histogram(seller_distribution, x="State", nbins=20)
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    st.divider() 
#============================End============================#
