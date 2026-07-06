
    # Data Quality Report
    **Dataset:** Space Titanic
    **Generated:** 2026-07-06 14:18
    **Rows:** 8693 | **Columns:** 14

    ---

    ## Executive Summary
     In the Space Titanic dataset comprising 8693 rows and 14 columns, data quality is generally acceptable with some notable exceptions. The most pressing issue lies in the high prevalence of outliers across five numerical columns, particularly 'spa', 'foodcourt', 'shoppingmall', 'vrdeck', and 'roomservice', which may significantly skew analysis results due to their extreme values.

Additionally, a low level of missing values is observed, with no sensitive or identifier columns affected. Given the uniform distribution of these gaps, an imputation strategy could be considered for a more complete dataset.

The dataset also exhibits significant skewness in several numerical columns, indicating that a small group of individuals or entities are consuming or spending much more than the majority. To mitigate the impact of outliers and skewed distributions on statistical analysis and model performance, it is recommended to either cap extreme values or apply log-transformations to these highly skewed columns.

Overall, while the dataset size is substantial, the presence of high-severity outliers and skewness in several numerical columns necessitates careful data preprocessing before further analysis. A more in-depth investigation may be required to understand the underlying causes and ensure accurate results.

    ---

    ## 1. Missing Values
    The Space Titanic dataset exhibits a low level of missing values across its 14 columns, with a maximum missing percentage of 2.5%. The missingness is relatively uniform across the columns, suggesting that there may be a common cause for the data gaps. However, it's worth noting that no sensitive or identifier columns (passengerid and name) have missing values. Given the low severity and uniform distribution of missing values, an imputation strategy could be considered to fill in the gaps, ensuring a more complete dataset for analysis.

    ![Missing Values](plots/missing_values.png)

    ---

    ## 2. Outliers
    The data quality report indicates a high severity of outliers in the analyzed dataset, with 5 out of 6 numerical columns exhibiting such anomalies. This suggests that a significant portion of the data is deviating significantly from the norm, which could potentially skew the overall analysis. Among these high-severity outliers are the 'spa', 'foodcourt', 'shoppingmall', 'vrdeck', and 'roomservice' columns, with outlier percentages ranging from 21.01% to 21.86%. These extreme values may not necessarily be data errors but rather natural outliers representing a small group of heavy spenders or unusual behavior in these categories. In contrast, the 'age' column has a low-severity outlier, indicating a single data point that deviates from the rest but is unlikely to significantly impact the analysis. Given the high prevalence of outliers, it would be advisable to either cap extreme values or apply log-transformations to normalize the data before further analysis. However, a more in-depth investigation may be required to understand the underlying causes and ensure accurate results.

    ![Outliers](plots/outliers.png)

    ---

    ## 3. Distributions
    The data analysis reveals a significant skewness in several numerical columns, indicating that the distribution of values is heavily skewed to the right. Specifically, columns such as spa, foodcourt, shoppingmall, vrdeck, and roomservice exhibit highly right-skewed distributions, with mean values significantly higher than their respective medians. This suggests that a small group of individuals or entities are spending or consuming much more than the majority. For instance, in the case of spa, it implies that most passengers spend nothing, while a few spend substantially more. Similarly, columns like age and foodcourt show an approximately symmetric distribution. It is noteworthy that all columns have min values equal to 0, implying that there are no negative values in any of these datasets. Given the high skewness and outlier percentages observed, it is recommended to either log-transform or standardize these highly skewed columns to reduce their impact on statistical analysis and improve model performance.

    ![Distributions]()

    ---

    ## 4. Correlations
    In this analysis, there are no strong correlations present among the numerical columns, as indicated by a threshold of 0.5 and no strong_correlated_pairs reported. However, some notable correlations were identified that may still hold valuable insights. For instance, a moderate correlation exists between 'spa' and both 'foodcourt' (0.222) and 'vrdeck' (0.154), suggesting that individuals who frequent spas might also be more likely to visit these other amenities. Similarly, there is a correlation between 'foodcourt' and 'age' (0.13), indicating that older individuals may be more inclined to use the food court. Additionally, 'vrdeck' and 'age' show a correlation of 0.101, implying a slight relationship where younger individuals might be more likely to utilize virtual reality technology. The absence of strong correlations is a positive finding, as it indicates that these features carry independent information, which can help in building robust models without multicollinearity concerns.

    ![Correlations](plots/correlation_heatmap.png)

    ---

    ## 5. Categorical Features
    The dataset contains a total of 5 categorical columns, with one high cardinality column, 'cabin', which has an unusually large number of unique values (6560). High cardinality columns like this require special handling methods such as target encoding to prevent issues during machine learning model training. Two binary columns, 'vip' and 'cryosleep', are present in the dataset. The 'vip' column is heavily imbalanced with 97.7% of passengers not being VIP, while 'cryosleep' shows a more even distribution between those who did (35.8%) and did not (64.2%) use cryosleep. The remaining columns, 'homeplanet', 'destination', and 'name', have moderate cardinality and show that the majority of passengers are from Earth (54.2%), traveling to TRAPPIST-1e (69.5%), and have unique names.

    ![Categorical]()

    ---

    ## 6. Class Balance
    The target column 'transported' in the dataset exhibits a balanced distribution with 50.4% instances labeled as 'True' and 49.6% as 'False'. Given the normal imbalance severity, no resampling or class weighting is required at this time to ensure fair model training.

    ![Class Balance](plots/class_balance.png)

    ---

    ## Appendix — Dataset Profile
    ```json
    {
  "number_of_rows": 8693,
  "number_of_columns": 14,
  "columns": [
    "passengerid",
    "homeplanet",
    "cryosleep",
    "cabin",
    "destination",
    "age",
    "vip",
    "roomservice",
    "foodcourt",
    "shoppingmall",
    "spa",
    "vrdeck",
    "name",
    "transported"
  ],
  "features": {
    "numerical_columns": [
      "spa",
      "foodcourt",
      "shoppingmall",
      "vrdeck",
      "age",
      "roomservice"
    ],
    "categorical_columns": [
      "vip",
      "homeplanet",
      "destination",
      "cryosleep",
      "cabin"
    ],
    "column_dtypes": {
      "passengerid": "object",
      "homeplanet": "object",
      "cryosleep": "object",
      "cabin": "object",
      "destination": "object",
      "age": "float64",
      "vip": "object",
      "roomservice": "float64",
      "foodcourt": "float64",
      "shoppingmall": "float64",
      "spa": "float64",
      "vrdeck": "float64",
      "name": "object",
      "transported": "bool"
    },
    "missing_values_percentages": {
      "passengerid": 0.0,
      "homeplanet": 2.31,
      "cryosleep": 2.5,
      "cabin": 2.29,
      "destination": 2.09,
      "age": 2.06,
      "vip": 2.34,
      "roomservice": 2.08,
      "foodcourt": 2.11,
      "shoppingmall": 2.39,
      "spa": 2.11,
      "vrdeck": 2.16,
      "name": 2.3,
      "transported": 0.0
    }
  },
  "number_of_duplicate_rows": 0,
  "target_column": "transported",
  "target_column_dtype": "bool",
  "target_column_summary": {
    "number_of_unique_values": 2,
    "value_distribution": {
      "True": 0.504,
      "False": 0.496
    }
  },
  "dataset_name": "Space Titanic",
  "sensitive_columns": [
    "name",
    "passportid"
  ],
  "identifier_columns": [
    "passengerid",
    "name"
  ]
}
    ```
    