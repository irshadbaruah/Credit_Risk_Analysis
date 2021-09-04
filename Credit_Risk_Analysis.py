#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[3]:


#Facts:

#average card balance is Rs 1000
#each card has an interest rate of 15%
#membership fee is Rs 20 per card
#loss rate is 3% (NOTE: what are the interpretations of this ? state your assumption CLEARLY when solving )
#Rs 25 operating cost per card
#Rs 10 affiliation fee per card (cost to the group organization itself, so that their members get this awesome card program)
#6.5% cost of funds (that credit card company must pay to the bank where it gets money)
#bill/statement is issued on 1st of every month
#credit-free period = 15 days from the bill/statement issue date.



# Initialization of the given parameters

# There are 1000 customers
total_cust = 1000 

# Overall percentage is 100%
# Let us assume 95% customers paid on time
cust_no_delay = 95/100

# Let us assume 2% paid 30 days after due date
cust_30_days = 2/100 

# Let us assume 2% paid 45 days after due date
cust_45_days = 2/100

# And assuming 1% paid 60 days after due date
cust_60_days = 1/100

# Monthly average balance of the customer
month_bal = 1000

# Given the membership fees of each card is Rs 20 
mem_fee = 12 * 20 * total_cust

# affiliation fee per card is Rs 10
affil_fee = 12 * 10 * total_cust

# Interest rate is 15%
int_rate = 15/100 

# Rs 25 is operating cost per card
operating_cost = 12 * 25 * 1000 

# 3% loss due to non-payment of credit card bills
loss_rate = 3/100 

# Per year calculation where cost of funds is 6.5%
cost_of_funds = 12 * total_cust * 1000 * 6.5/1200


# In[4]:


#Scenario 1:
    #i) The interest rate is simple interest. 
    #ii) Interest is calculated on a daily basis. 
    #iii) The average card balance is the average end of month balance. 
    #iv) All members are more than a year old.
    
    # Dividing the customers according to their required categories

day = 30
categories = 4
category_type = []

for cust_category in range(categories):
    if cust_category == 0:
        category_type.append('Pay the bill within the credit-free period')
    else:
        category_type.append('Paying %d days after the last due date'%day)
        day+=15     

Data_Calculations=pd.DataFrame({'Category':category_type},index=np.arange(1,categories+1))
Data_Calculations


# In[5]:


# Interest after 'N' days can be calculated as 
# 'N'= N*outstanding balance*Interest rate per year/365

def interest_calc(payment_days):
    
    # Let the billing cycle starts from 1st of every month

    # Let us assume average day of transaction as 15th of billing cycle
    average_day_trans = 15 
    
    # No interest for the category of customer who paid their bill on time
    if payment_days == category_type[0]:
        Int_per_card=0

    # Category of customer who pay 30 days after the last due date, Interest on them
    elif payment_days == category_type[1]:
        Int_per_card = (average_day_trans + 15 + 30) * month_bal * int_rate/365

    # Category of customer who pay 45 days after the last due date, Interest on them
    elif payment_days == category_type[2]:
        Int_per_card = (average_day_trans + 15 + 45) * month_bal * int_rate/365
        
    # Category of customer who pay 60 days after the last due date, Interest on them
    else:
        Int_per_card = (average_day_trans + 15 + 60) * month_bal * int_rate/365
        
    return Int_per_card 
    
def total_int(column):
    
    payment_days = column[0]
    interest_per_card = column[1]
    
    if payment_days == category_type[0]:
        total_interest = 0 

    # Calculation of interest who are late by 30 days
    elif payment_days == category_type[1]:
        total_interest = 12 * interest_per_card * cust_30_days * total_cust

    # Calculation of interest who are late by 30 days
    elif payment_days == category_type[2]:
        total_interest = 12 * interest_per_card * cust_45_days * total_cust

   # Calculation of interest who are late by 60 days, remove these category of customers 
    else:
        total_interest = 12 * interest_per_card * cust_60_days * total_cust
        
    return total_interest

# Profit/loss margin
def PnL_check(): 
    if net_profit_loss >= 0:
        return 'Profit margin in percentage'
    else:
        return 'Loss margin in percentage'


# In[6]:


Data_Calculations['Estimated_Interest_on_Default']=Data_Calculations['Category'].apply(interest_calc).round(2)
Data_Calculations['Total_Interest_1Year']=Data_Calculations[['Category','Estimated_Interest_on_Default']].apply(total_int,axis=1)
Data_Calculations['Fixed_Late_Fee_charge']=Data_Calculations['Estimated_Interest_on_Default'].apply(lambda x: 0 if x==0 else 50)
Data_Calculations


# In[7]:


# Calculation of profit generation for scenario 1
Expenses=cost_of_funds+operating_cost+(loss_rate*total_cust*month_bal)
Earnings=mem_fee+affil_fee+np.sum(Data_Calculations['Total_Interest_1Year'])+(12*max(Data_Calculations['Fixed_Late_Fee_charge'])*5/100*total_cust)

# Margin earned
margin=Earnings-Expenses

# Net profit loss margin
net_profit_loss=margin/Expenses*100
    
report=pd.DataFrame({'Total yearly card balance':12*month_bal*total_cust,'Earnings':Earnings,'Expenses':Expenses,
              'Margin':margin,PnL_check():net_profit_loss.round(2)},index=[' '])
report


# In[8]:


#Scenario 2: 
#i) The interest rate is compounded quarterly. 
#ii) Interest is calculated on a monthly basis. 
#iii) Membership grows at 5% month on month. 
#iv) Card balance grows at 5% per month for each member. 
#v) The average card balance is the average end of month balance.


#Calculation of scenario 2
# Return new membership fee for each month

def membership_calc(mem_fee,monthly_growth):
    
    monthly_mem_fee=[]
    
    for months in total_months:
        monthly_mem_fee.append(mem_fee)
        new_mem_fee = mem_fee+mem_fee * (monthly_growth)
        mem_fee = new_mem_fee
        
    return monthly_mem_fee

# Return new balance for each month

def month_bal_calc(average_bal,monthly_growth):
    
    avg_month_bal = []
    
    for months in total_months:
        avg_month_bal.append(average_bal)
        new_month_bal = average_bal + average_bal * (monthly_growth)
        average_bal = new_month_bal
        
    return avg_month_bal


# In[9]:


# Prameters are

# Month from 1 to 12
total_months=np.arange(1,13)

# Membership fees is given as Rs 20
mem_fee = 20 

# Affiliation fee is given as Rs 10
affil_fee = 10 

# Month on month growth is 5%  
monthly_growth = 0.05

# Balance started with 1000
average_bal = 1000

# Late fee is taken Rs 50
late_fee = 50

# calling the above functions

per_month_fee = membership_calc(mem_fee,monthly_growth)
bal_per_month = month_bal_calc(average_bal,monthly_growth)


# In[10]:


Data_Calc_scenario2=pd.DataFrame({'Month':total_months,'Month_on_Month_Bal':bal_per_month,'Membership_Fee':per_month_fee},index=[' ' for index in total_months]).round(2)
Data_Calc_scenario2


# In[11]:


#Interest after 'N' months is = N*[outstanding balance * (1 + Interest rate per year / 4)^4 - outstanding balance]/12
#(https://economictimes.indiatimes.com/wealth/borrow/why-paying-the-minimum-amount-due-on-credit-cards-can-make-you-fall-into-a-debt-trap/articleshow/71064891.cms?from=mdr)

def interest_calc(month_bal):

    # Compound interest quarterly and caculation of compound interest monthly
    Int_per_card = (month_bal*(1+int_rate/4)**4-month_bal)/12    
    return np.round(Int_per_card,2)

# Cut out the number of active accounts when customers do not pay within 60 days after duedate

def active_customers():
    
    active_cust=[]

    # Let there are 1000 Customers
    total_cust = 1000 

    # As we assum 1% pay their due after 60 days
    cust_60_days = 1/100

    for month in total_months:
        if month>3:
            update_customers = total_cust-cust_60_days*total_cust
            active_cust.append(int(update_customers))    
            total_cust = update_customers
        else:
            active_cust.append(int(total_cust)) 
            
    return active_cust

def int_30days(columns):
    
    int_month = columns[0]
    customers = columns[1]

    # Average day of transaction for a month
    avg_day_trans = 15 

    # Credit free period is taken as 15 days
    billing_period = 15  
    
    return np.ceil((avg_day_trans+billing_period+30)/30)*cust_30_days*customers*int_month

def int_45days(columns):
    
    int_month = columns[0]
    customers = columns[1]

    #Average day of transaction for a month
    avg_day_trans = 15 

    # Credit free period is 15 days
    billing_period = 15  
    
    return np.ceil((avg_day_trans+billing_period+45)/30)*cust_45_days*customers*int_month

def int_60days(columns):
    
    int_month=columns[0]
    customers=columns[1]

    # Average day of transaction for a month
    avg_day_trans = 15 

    # Credit free period is 15 days
    billing_period = 15  
    
    return np.ceil((avg_day_trans+billing_period+60)/30)*cust_60_days*customers*int_month

def total_charge(columns):
    
    return columns[0] + columns[1] + columns[2] + columns[3]    

# Profit/loss margin
def PnL_check(): 
    if net_profit_loss>=0:
        return 'Profit margin in percentage'
    else:
        return 'Loss margin in percentage'


# In[12]:


Data_Calc_scenario2['Interest_Relative_to_Balance']=Data_Calc_scenario2['Month_on_Month_Bal'].apply(interest_calc)
Data_Calc_scenario2.insert(4,'Active_customers',active_customers(),True)
Data_Calc_scenario2['Total_Fixed_Late_Fee']=Data_Calc_scenario2['Active_customers'].apply(lambda cust: (1-cust_no_delay)*cust*late_fee)
Data_Calc_scenario2['Total_Interest_30days_late']=Data_Calc_scenario2[['Interest_Relative_to_Balance','Active_customers']].apply(int_30days,axis=1)
Data_Calc_scenario2['Total_Interest_45days_late']=Data_Calc_scenario2[['Interest_Relative_to_Balance','Active_customers']].apply(int_45days,axis=1)
Data_Calc_scenario2['Total_Interest_60days_late']=Data_Calc_scenario2[['Interest_Relative_to_Balance','Active_customers']].apply(int_60days,axis=1)
Data_Calc_scenario2['Total_Late_Charges_Collected']=(Data_Calc_scenario2.iloc[:,5:]).apply(total_charge,axis=1)
Data_Calc_scenario2


# In[13]:


# Calculation of all the factors of the year

# Loss rate on outstanding balance over the year

loss = 0
for month_bal,total_cust in zip(Data_Calc_scenario2['Month_on_Month_Bal'],Data_Calc_scenario2['Active_customers']):
    loss = loss+(loss_rate/12)*total_cust*month_bal  

# total membership fee over the year
    total_mem_fee = 0
for mem_fee,total_cust in zip(Data_Calc_scenario2['Membership_Fee'],Data_Calc_scenario2['Active_customers']):
    total_mem_fee = total_mem_fee+mem_fee*total_cust
    
# total affiliation fee over the year 
    total_affil_fee = 0
for total_cust in Data_Calc_scenario2['Active_customers']:
    total_affil_fee = total_affil_fee + affil_fee * total_cust
    
# Total Average Balance for the financial year
    
card_bal = np.sum(Data_Calc_scenario2['Month_on_Month_Bal']*Data_Calc_scenario2['Active_customers'])
    
# Calculation of Expenses and Earnings

Expenses = cost_of_funds + operating_cost + loss
Earnings = total_mem_fee+total_affil_fee + np.sum(Data_Calc_scenario2['Total_Late_Charges_Collected'])

# Margin earned above or below total amount spent
margin = Earnings-Expenses 
net_profit_loss = margin/Expenses*100
    
Report=pd.DataFrame({'Total yearly card balance':card_bal,'Earnings':Earnings,'Expenses':Expenses,
              'Margin':margin,PnL_check():net_profit_loss.round(2)},index=[' '])
#Printing out the results
Report


# In[ ]:


#Profit margin in percentage for Scenario 1 is 3.23%
#Profit margin in percentage for Scenario 2 is 18%
#Profit margin ratio of scenario 1 to scenario 2 is almost 1:6
#Scenario 2 can contribute higher profits as compared to scenario 1
#Senario 2 generete 6 times more compared to senario 1
#Q3: Is a borrower with a low balance more or less likely to default then a borrower with a high balance? Why ? explain clearly

#Ans---A borrower with a low balance is more likely to default. Various factors might effect

#He might not have a good credit score
#Might havve alow income source. So there is a high propability that the borrower with a low balance might default
#Q5: What numbers can the financial institution change to convince the affiliated group not to want to purchase, while still not going into a loss? Give a range of what the new numbers are (min and max)

#Ans----Credit lending company can show that a higher percentage of people are defaulters

#Q6: What is the extra cost(if any) company will have to incur if the customer delays the payment of the credit card bill after the due date?

#Ans---Extra cost will be incurred by the company if the customers defaults on the payments. Otherwise greater interest will be generated.

#Q7: Is it beneficial for the company if the customer pays the credit card bill after the due date? (express your views as a business strategy analyst with a short example)

#Ans ---Definitely it is beneficial for the company if the customer pays the bill after the due date but the rate of profit can differ. For example, if a customer pays the bill within the credit free period which is between day 1 and 15 then the company won’t have any profit but if the customer pays after 15 days then every extra date has interest on principal amount.

#Q. Which information variables you will use to calculate the credit card limit and the risk associated with it for an individual customer? Also, give the reason for your choice. (Example-Bureau score)

#Ans --

#A proper background check
#CIBIL score
#History of past default

