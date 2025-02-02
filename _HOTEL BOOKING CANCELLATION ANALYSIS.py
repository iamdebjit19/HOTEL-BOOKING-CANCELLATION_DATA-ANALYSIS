#!/usr/bin/env python
# coding: utf-8

# # HOTEL BOOKING CANCELLATION ANALYSIS

# --- by DEBJIT GHOSH

# In recent years, City Hotel and Resort Hotel have seen high cancellation rates. Each hotel is now dealing with a number of issues as a result, including fewer revenues and less than ideal hotel room use. Consequently, lowering cancellation rates is both hotels' primary goal in order to increase their efficiency in generating revenue, and for us to offer thorough business advice to address this problem.

# The analysis of hotel booking cancellations as well as other factors that have no bearing on their business and yearly revenue generation are the main topics of this report.

# # Research Question 

# 1. What are the variables that affect hotel reservation cancellations ? 
# 2. How can we make hotel reservations cancellations better ? 
# 3. How will hotels be assisted in making pricing and promotional decisions ? 

# # Hypothesis

# 1. More cancellations occur when prices are higher.
# 2. When there is a longer waiting list , customers tend to cancel more frequently.
# 3. The majority of clients are coming from offline travel agents to make their reservations.

# # Importing Libraries

# In[2]:


import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 
import warnings
warnings.filterwarnings('ignore')


# # Loading the dataset

# In[4]:


df = pd.read_csv(r'C:\Users\HP\Downloads\hotel_bookings.csv',encoding='unicode_escape')


# # Exploratory Data Analysis and Data Cleaning 

# In[5]:


df.head()


# In[6]:


df.tail()


# In[7]:


df.shape


# There are 119390 rows , and 32 columns present in the dataset.

# In[8]:


df.columns


# In[9]:


df.info()


# # Converting date column into date-time format

# In[10]:


df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'])


# In[11]:


df.info()


# In[12]:


df.describe(include='object')  


# In[14]:


for col in df.describe(include='object').columns: 
    print(col)
    print(df[col].unique())
    print('-'*50)


# In[15]:


df.isnull().sum()


# In[16]:


df.drop(['company','agent'],axis=1,inplace=True)
df.dropna(inplace=True)


# In[17]:


df.isnull().sum()


# In[18]:


df.describe()


# In[19]:


df['adr'].plot(kind='box')


# In[20]:


df=df[df['adr']<5000]


# In[21]:


df.describe()


# # Data Analysis and Visualization 

# In[24]:


cancelled_perc = df['is_canceled'].value_counts(normalize=True)
print(cancelled_perc)

plt.figure(figsize = (6,5))
plt.title('Reservation status count')
plt.bar(['Not canceled','Canceled'],df['is_canceled'].value_counts(),edgecolor='k' , width=0.7)
plt.show()


# Around 62.8% of the hotel bookings are not cancelled , where as around 37.1% of the hotel bookings are cancelled.

# In[51]:


plt.figure(figsize=(8, 4))
ax1 = sns.countplot(x='hotel', hue='is_canceled', data=df, palette='Blues')

# Set legend with custom labels
legend_labels, _ = ax1.get_legend_handles_labels()
ax1.legend(legend_labels, ['Not Canceled', 'Canceled'], bbox_to_anchor=(1, 1))

# Add title and axis labels
plt.title('Reservation Status in Different Hotels', size=20)
plt.xlabel('Hotel', size=14)
plt.ylabel('Number of Reservations', size=14)

# Display the plot
plt.show()


# In[26]:


resort_hotel = df[df['hotel'] == 'Resort Hotel']
resort_hotel['is_canceled'].value_counts(normalize = True)


# In[27]:


city_hotel = df[df['hotel'] == 'City Hotel']
city_hotel['is_canceled'].value_counts(normalize = True)


# * For resort hotels , around 72% of the hotel bookings are not getting cancelled , where as around 27.9% i.e. almost 28% of the hotel bookings are getting cancelled. 
# 
# * For city hotels , around 58.2% of the hotel bookings are not being cancelled , on the other hand , around 41.7% i.e. almost 42% of the hotel bookings are being cancelled. 

# In[28]:


resort_hotel = resort_hotel.groupby('reservation_status_date')[['adr']].mean()
city_hotel = city_hotel.groupby('reservation_status_date')[['adr']].mean()


# In[30]:


plt.figure(figsize=(20,8))
plt.title('Average Daily Rate in City and Resort Hotel',fontsize=30)
plt.plot(resort_hotel.index,resort_hotel['adr'], label ='Resort Hotel')
plt.plot(city_hotel.index,city_hotel['adr'], label ='City Hotel')
plt.legend(fontsize=20)
plt.show()


# In[31]:


df['month'] = df['reservation_status_date'].dt.month
plt.figure(figsize = (16,8))
ax1 = sns.countplot(x='month', hue='is_canceled',data=df , palette ='bright')
legend_labels,_ = ax1.get_legend_handles_labels()
ax1.legend(bbox_to_anchor =(1,1))
plt.title('Reservation status per month', size=20)
plt.xlabel('month')
plt.ylabel('number of reservations')
plt.legend(['not canceled','canceled'])
plt.show()


# * The maximum number of hotel bookings were cancelled in the month of January , the minimum number of hotel bookings were cancelled in the month of August.
# 
# * The maximum number of hotel bookings , which were not cancelled , was in the month of August , where as the minimum number of hotel bookings which were not cancelled was in the month December. 
# 

# In[38]:


if all(col in df.columns for col in ['month', 'adr', 'is_canceled']):
    # Filter and group the data
    filtered_data = df[df['is_canceled'] == 1]
    grouped_data = filtered_data.groupby('month', as_index=False)['adr'].sum()
    
    # Plotting
    plt.figure(figsize=(15, 8))
    plt.title('ADR per Month', fontsize=30)
    sns.barplot(x='month', y='adr', data=grouped_data)
    plt.show()
else:
    print("Error: Ensure 'month', 'adr', and 'is_canceled' columns exist in the DataFrame.")


# In[36]:


cancelled_data = df[df['is_canceled'] == 1]
top_10_country = cancelled_data['country'].value_counts()[:10]
plt.figure(figsize = (8,8))
plt.title('Top 10 countries with reservation canceled')
plt.pie(top_10_country , autopct = '%.2f' , labels = top_10_country.index)
plt.show()


# * The maximum number of hotel booking cancellations is from Portugal. 
# * To resolve this issue , we can suggest the hotel to faciliate promotional discounts , increase various facilities etc in Portugal only.

# In[37]:


df['market_segment'].value_counts()


# In[39]:


df['market_segment'].value_counts(normalize = True)


# * The maximum number of the customers are booking hotels via online travel agents (56402) which is almost 47.4%. 

# In[41]:


cancelled_data['market_segment'].value_counts()


# In[42]:


cancelled_data['market_segment'].value_counts(normalize = True)


# * The maximum number of hotel booking cancellations are from those booking category which were done via online travel agents (20738) i.e. almost 46.9% ~ 47% . 

# In[47]:


cancelled_data = df[df['is_canceled'] == 1]  # Fixed: is_canceled == 1 for canceled bookings
cancelled_df_adr = cancelled_data.groupby('reservation_status_date')[['adr']].mean()
cancelled_df_adr.reset_index(inplace=True)
cancelled_df_adr.sort_values('reservation_status_date', inplace=True)

not_cancelled_data = df[df['is_canceled'] == 0]  # Fixed: is_canceled == 0 for not canceled bookings
not_cancelled_df_adr = not_cancelled_data.groupby('reservation_status_date')[['adr']].mean()
not_cancelled_df_adr.reset_index(inplace=True)
not_cancelled_df_adr.sort_values('reservation_status_date', inplace=True)

# Ensure reservation_status_date is in datetime format for proper plotting
cancelled_df_adr['reservation_status_date'] = pd.to_datetime(cancelled_df_adr['reservation_status_date'])
not_cancelled_df_adr['reservation_status_date'] = pd.to_datetime(not_cancelled_df_adr['reservation_status_date'])

# Plotting
plt.figure(figsize=(20, 6))
plt.title('Average Daily Rate Over Time', fontsize=20)
plt.plot(not_cancelled_df_adr['reservation_status_date'], not_cancelled_df_adr['adr'], label='Not Cancelled', color='green')
plt.plot(cancelled_df_adr['reservation_status_date'], cancelled_df_adr['adr'], label='Cancelled', color='red')
plt.xlabel('Reservation Status Date', fontsize=14)
plt.ylabel('ADR (Average Daily Rate)', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True)
plt.show()


# In[48]:


cancelled_df_adr = cancelled_df_adr[(cancelled_df_adr['reservation_status_date']>'2016') & (cancelled_df_adr['reservation_status_date']<'2017-09')]
not_cancelled_df_adr = not_cancelled_df_adr[(not_cancelled_df_adr['reservation_status_date']>'2016') & (not_cancelled_df_adr['reservation_status_date']<'2017-09')]                                                                                                        


# In[50]:


plt.figure(figsize=(20, 6))
plt.title('Average Daily Rate Over Time', fontsize=20)
plt.plot(not_cancelled_df_adr['reservation_status_date'], not_cancelled_df_adr['adr'], label='Not Cancelled', color='green')
plt.plot(cancelled_df_adr['reservation_status_date'], cancelled_df_adr['adr'], label='Cancelled', color='red')
plt.xlabel('Reservation Status Date', fontsize=14)
plt.ylabel('ADR (Average Daily Rate)', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True)
plt.show()


# * Average daily rate is mostly influencing the cancellation rate.

# # Suggestions

# 1. Cancellation rates rise as the price does. In order to prevent cancellations of reservations,hotels could work on their pricing strategies and try to lower the rates for specific hotels based on locations. They can also provide some discounts to the consumers.
# 
# 2. As the ratio of the cancellation and not cancellation of the resort hotel is higher in the resort hotel than the city hotels.So the hotels should provide a reasonable discount on the room prices on weekends or on holidays.
# 
# 3. In the month of January, hotels can start campaigns or marketing with a reasonable amount to increase their revenue as the cancellation is highest in this month.
# 
# 4. They can also increase the quality of their hotels and their services mainly in Portugal to reduce the cancellation rate.
