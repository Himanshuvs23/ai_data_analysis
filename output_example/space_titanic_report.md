# AI Data Analyst Report

**Dataset:** Space Titanic
**Generated:** 2026-07-06 15:32
**Rows:** 8693 | **Columns:** 14

---

## Executive Summary
 In the Space Titanic dataset comprising 8693 rows and 14 columns, data quality is generally satisfactory with only minor issues to address. The most pressing concern involves a significant number of outliers across six numerical columns, particularly in spa, foodcourt, vrdeck, shoppingmall, and roomservice, where high severity outliers account for approximately half of the total observations. These extreme values may represent heavy spenders or unusual events, necessitating careful distinction between true outliers (data errors) and natural outliers (valid extreme values).

Additionally, the dataset exhibits a low level of missing values across its columns, with a maximum missing percentage of 2.5%. Given the uniform distribution of these gaps, an imputation strategy could be considered to fill in the data for more comprehensive analysis.

The overall data distribution is highly right-skewed, with six out of the total six numerical columns clustered around lower values and a small number of observations having significantly higher values. This skewed distribution may mask important patterns or relationships within the data and could potentially benefit from either log transformation, standardization, or keeping the data as-is depending on the specific goals and assumptions of the analysis.

Lastly, the target column 'transported' in the dataset shows a balanced distribution with 50.4% instances labeled as 'True' and 49.6% as 'False', indicating no need for resampling or class weighting at this time to ensure fair model training.

In summary, while the Space Titanic dataset is generally clean, addressing the high number of outliers in the high severity columns and considering an imputation strategy for missing values are recommended to ensure accurate and comprehensive analysis.

---

## 1. Missing Values
The Space Titanic dataset exhibits a low level of missing values across its 14 columns, with a maximum missing percentage of 2.5%. The missingness is relatively uniform across the columns, suggesting that there may be a common cause for the data gaps. However, it's worth noting that no sensitive or identifier columns (passengerid and name) have missing values. Given the low severity and uniform distribution of missing values, an imputation strategy could be considered to fill in the gaps, ensuring a more complete dataset for analysis.

![Missing Values](plots/missing_values.png)

---

## 2. Outliers
The data quality report reveals a significant number of outliers across six numerical columns, with high severity outliers accounting for half of the total. Specifically, five columns - spa, foodcourt, vrdeck, shoppingmall, and roomservice - exhibit high outlier percentages ranging from 21.01% to 21.86%. These findings suggest a substantial presence of extreme values that deviate significantly from the rest of the data distribution. However, it is important to note that these outliers do not necessarily indicate data errors but rather may represent a small group of heavy spenders or unusual events. In contrast, only one column - age - shows low severity outliers with an outlier percentage of 0.9%. It is crucial to distinguish between true outliers (data errors) and natural outliers (valid extreme values). To address the high number of outliers in the high severity columns, it is recommended to either cap the values at a certain threshold or apply log-transformation to normalize the data distribution. Further investigation may be necessary to understand the nature of these outliers and ensure their accuracy.

![Outliers](plots/outliers.png)

---

## 3. Distributions
The numerical data distributions exhibit significant skewness, with six out of the total six numerical columns being highly right-skewed. This indicates that most values in these columns are clustered around the lower end, while a small number of observations have significantly higher values. For instance, in columns such as spa, foodcourt, vrdeck, shoppingmall, and roomservice, the mean values are substantially greater than the medians, suggesting that a minority of individuals or entities spend considerably more than the majority. This skewed distribution could potentially mask important patterns or relationships within the data. Furthermore, it is noteworthy that all columns have at least one observation with a minimum value of zero, which may indicate missing or zero-valued data in these columns. The high number of outliers and the highly skewed distributions suggest that further analysis might benefit from either log transformation, standardization, or possibly keeping the data as-is depending on the specific goals and assumptions of the analysis.

![Distributions]()

---

## 4. Correlations
In this analysis, there are no strong correlations present among the numerical columns, as indicated by a total of zero strong-correlated pairs and a false any_strong_correlation value. However, several notable correlations were identified that may provide insights into the data. For instance, a moderate positive correlation exists between the 'spa' and 'age' columns, suggesting that older individuals might be more likely to use spa facilities. Similarly, there is a strong positive relationship between 'spa' and 'foodcourt', as well as 'spa' and 'vrdeck', implying that those who frequent the spa may also spend time in these areas. Additionally, there is a moderate positive correlation between 'foodcourt' and 'vrdeck', indicating that individuals who spend time in one area are likely to spend time in the other. This lack of strong correlations can be considered a positive finding, as it suggests that the features carry independent information.

![Correlations](plots/correlation_heatmap.png)

---

## 5. Categorical Features
The dataset contains a total of 5 categorical columns, with one high cardinality column, 'cabin', which has an unusually large number of unique values (6560). High cardinality columns like this require special handling methods such as target encoding to prevent issues during machine learning model training. Two binary columns, 'vip' and 'cryosleep', are present in the dataset. The 'vip' column is heavily imbalanced with 97.7% of passengers not being VIP, while 'cryosleep' shows a more balanced distribution between those who did (35.8%) and did not (64.2%) use cryosleep. The remaining columns, 'homeplanet', 'destination', display dominant categories that suggest the majority of passengers are Earthlings traveling to TRAPPIST-1e.

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
      "age",
      "foodcourt",
      "vrdeck",
      "shoppingmall",
      "roomservice"
    ],
    "categorical_columns": [
      "vip",
      "cryosleep",
      "homeplanet",
      "destination",
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