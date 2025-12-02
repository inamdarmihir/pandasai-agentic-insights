# 🎬 Demo Guide

## Quick Demo (5 minutes)

### Step 1: Setup (1 min)

```bash
# Start Qdrant
docker run -p 6333:6333 qdrant/qdrant

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=sk-your-key
```

### Step 2: Generate Sample Data (30 sec)

```bash
python utils/data_generator.py
```

This creates:
- `sample_sales_data.xlsx` - 500 rows of sales data
- `sample_hr_data.xlsx` - 200 rows of employee data

### Step 3: Launch App (30 sec)

```bash
streamlit run app.py
```

Or use the startup script:
```bash
# Windows
start.bat

# Linux/Mac
chmod +x start.sh
./start.sh
```

### Step 4: Try These Queries (3 min)

#### Sales Analysis Queries

1. **Basic Stats**
   ```
   What is the total revenue?
   ```

2. **Top Performers**
   ```
   Show me the top 5 products by profit
   ```

3. **Regional Analysis**
   ```
   Which region has the highest average customer satisfaction?
   ```

4. **Trend Analysis**
   ```
   Show revenue trends by month
   ```

5. **Correlation**
   ```
   Is there a correlation between discount and revenue?
   ```

6. **Advanced**
   ```
   What's the profit margin by sales channel and region?
   ```

#### HR Data Queries

1. **Salary Analysis**
   ```
   What's the average salary by department?
   ```

2. **Performance**
   ```
   Show employees with performance score above 4.5
   ```

3. **Experience vs Salary**
   ```
   Plot the relationship between years of experience and salary
   ```

## Expected Results

### Query: "What is the total revenue?"

**Analysis Output:**
```
Total Revenue: $45,234,567.89
```

**AI Insights:**
```
Based on the analysis:

1. Revenue Performance: The total revenue of $45.2M indicates strong 
   business performance across all regions.

2. Key Drivers: The data shows Electronics category contributes 60% 
   of total revenue, with Laptops being the top product.

3. Recommendations:
   - Focus marketing efforts on high-performing products
   - Investigate low-performing regions for improvement opportunities
   - Consider expanding successful product lines
```

### Query: "Show top 5 products by profit"

**Analysis Output:**
```
Product      Profit
Laptop       $8,234,567
Phone        $6,123,456
Monitor      $4,567,890
Tablet       $3,456,789
Headphones   $2,345,678
```

**AI Insights:**
```
Profit Analysis:

1. Product Mix: Laptops generate 35% of total profit despite 
   representing only 20% of sales volume - indicating high margins.

2. Opportunity: Headphones show strong profit despite lower revenue,
   suggesting potential for volume expansion.

3. Action Items:
   - Increase inventory for high-margin products
   - Bundle low-margin items with high-margin products
   - Review pricing strategy for mid-tier products
```

## Agent Workflow Demo

Watch the agents work:

1. **Router Agent** 
   - Receives query
   - Searches Qdrant for relevant past interactions
   - Adds context to query

2. **Analyzer Agent**
   - Uses PandasAI to execute analysis
   - Returns structured data

3. **Insight Generator**
   - Takes analysis results
   - Generates business insights using GPT-4
   - Formats recommendations

4. **Memory Manager**
   - Stores interaction in Qdrant
   - Creates embeddings for future retrieval

## Memory Search Demo

After running several queries, try:

1. Go to "Agent Memory" tab
2. Click "Search Memory"
3. Enter: "revenue"
4. See all past revenue-related queries and insights

## Auto Insights Feature

Click "Auto Insights" button to get:
- Data quality assessment
- Key trends and patterns
- Anomaly detection
- Business recommendations
- Next steps suggestions

## Advanced Features

### Context-Aware Queries

Try this sequence:

1. "What's the total revenue?"
2. "Break it down by region"
3. "Now show me the trend over time"

The agents remember context from previous queries!

### Multi-Step Analysis

```
"Compare the performance of Online vs Retail channels, 
then identify which products perform best in each channel, 
and finally recommend optimization strategies"
```

The agents will:
1. Analyze channel performance
2. Break down by product
3. Generate strategic recommendations

## Troubleshooting

### Qdrant Connection Error
```bash
# Check if Qdrant is running
curl http://localhost:6333

# Restart Qdrant
docker restart <container-id>
```

### OpenAI API Error
- Verify API key in `.env`
- Check API quota/billing
- Ensure internet connection

### PandasAI Error
- Check data format (no special characters in column names)
- Ensure numeric columns are properly typed
- Try simpler queries first

## Performance Tips

1. **Large Datasets**: For files > 10MB, consider sampling
2. **Complex Queries**: Break into smaller steps
3. **Memory**: Clear Qdrant collection periodically for fresh start

## Next Steps

- Try your own Excel/CSV files
- Experiment with different query types
- Explore the agent memory
- Customize agents in `agents/orchestrator.py`
- Add new agent types for specialized tasks

---

**Pro Tip**: The more you interact, the smarter the system becomes 
as it builds context in Qdrant memory! 🧠
