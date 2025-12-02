import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sales_data(rows=500):
    """Generate realistic sales data"""
    np.random.seed(42)
    
    products = ['Laptop', 'Phone', 'Tablet', 'Monitor', 'Keyboard', 'Mouse', 'Headphones', 'Webcam']
    regions = ['North America', 'Europe', 'Asia', 'South America', 'Africa']
    categories = ['Electronics', 'Accessories', 'Computing']
    sales_channels = ['Online', 'Retail', 'Wholesale']
    
    start_date = datetime(2023, 1, 1)
    
    data = []
    for i in range(rows):
        date = start_date + timedelta(days=random.randint(0, 700))
        product = random.choice(products)
        quantity = random.randint(1, 100)
        base_price = random.randint(50, 2000)
        discount = random.choice([0, 0.05, 0.1, 0.15, 0.2])
        
        data.append({
            'Date': date,
            'Product': product,
            'Category': random.choice(categories),
            'Region': random.choice(regions),
            'Sales_Channel': random.choice(sales_channels),
            'Quantity': quantity,
            'Unit_Price': base_price,
            'Discount': discount,
            'Revenue': quantity * base_price * (1 - discount),
            'Cost': quantity * base_price * 0.6,
            'Customer_Satisfaction': round(random.uniform(3.5, 5.0), 1)
        })
    
    df = pd.DataFrame(data)
    df['Profit'] = df['Revenue'] - df['Cost']
    df['Date'] = pd.to_datetime(df['Date'])
    
    return df

def generate_hr_data(rows=200):
    """Generate HR/Employee data"""
    departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations']
    positions = ['Junior', 'Mid-Level', 'Senior', 'Lead', 'Manager', 'Director']
    
    data = []
    for i in range(rows):
        years_exp = random.randint(0, 20)
        base_salary = random.randint(40000, 150000)
        
        data.append({
            'Employee_ID': f'EMP{i+1000}',
            'Department': random.choice(departments),
            'Position': random.choice(positions),
            'Years_Experience': years_exp,
            'Salary': base_salary,
            'Performance_Score': round(random.uniform(2.5, 5.0), 1),
            'Projects_Completed': random.randint(0, 50),
            'Training_Hours': random.randint(0, 100),
            'Satisfaction_Score': round(random.uniform(3.0, 5.0), 1),
            'Remote_Work_Days': random.randint(0, 5)
        })
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    # Generate sample datasets
    sales_df = generate_sales_data(500)
    sales_df.to_excel('sample_sales_data.xlsx', index=False)
    print("✅ Generated sample_sales_data.xlsx")
    
    hr_df = generate_hr_data(200)
    hr_df.to_excel('sample_hr_data.xlsx', index=False)
    print("✅ Generated sample_hr_data.xlsx")
