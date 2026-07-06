# AI Data Analyst Report


**Dataset:** Space Titanic

**Generated:** 2026-07-06 17:53

**Rows:** 8693 | **Columns:** 14

---

## Executive Summary
 In the Space Titanic dataset comprising 8693 rows and 14 columns, data quality is generally satisfactory with only minor issues. The most pressing concern involves a significant number of high severity outliers in six columns, primarily affecting roomservice, foodcourt, vrdeck, spa, and shoppingmall categories, representing substantial deviations from the norm. This suggests the presence of a small group of heavy spenders rather than data errors.

Another notable finding is the low level of missing values across all columns, with a maximum of 2.5%. While no sensitive or identifier columns have missing values, an imputation strategy could be considered to fill in the gaps and ensure a more complete dataset for analysis.

The dataset also exhibits highly right-skewed distributions in several numerical columns, indicating that most users spend little or nothing while a small group spends significantly more. To address these issues, it may be beneficial to consider log-transforming or standardizing these highly skewed columns to better represent the data and reduce the impact of outliers.

Overall, the dataset presents a balanced distribution for the target column 'transported', with 50.4% instances labeled as 'True' and 49.6% as 'False'. Given the generally clean state of the data, it is recommended to address the identified outlier and skewness issues before proceeding with further analysis or modeling.

---

## 1. Missing Values
The Space Titanic dataset exhibits a low level of missing values across its 14 columns, with a maximum missing percentage of 2.5%. The missingness is relatively uniform across the columns, suggesting that there may be a common cause for the data gaps. However, it's worth noting that no sensitive or identifier columns (passengerid and name) have missing values. Given the low severity and uniform distribution of missing values, an imputation strategy could be considered to fill in the gaps, ensuring a more complete dataset for analysis.

![Missing Values](plots/missing_values.png)

---

## 2. Outliers
The data quality report reveals a significant number of high severity outliers, accounting for 83.33% of the total outlier columns. Specifically, six out of the total six outlier columns are classified as high severity, indicating substantial deviations from the norm in the roomservice, foodcourt, vrdeck, spa, and shoppingmall categories. On the other hand, only one column, age, has a low severity outlier, representing a minor anomaly. The high percentage of outliers in several columns suggests the presence of a small group of heavy spenders rather than data errors, as the median values for these columns are zero. It is essential to distinguish between true outliers, which may indicate data errors, and natural outliers, representing valid extreme values. To address this issue, it would be beneficial to either cap the values at a certain threshold or apply log-transformations to normalize the distribution. Further investigation may also be necessary to ensure the accuracy of the data in high severity columns.

![Outliers](plots/outliers.png)

---

## 3. Distributions
The data analysis reveals a significant skewness in several numerical columns, indicating that the distribution of values is heavily skewed to the right. Specifically, the roomservice, foodcourt, vrdeck, spa, and shoppingmall columns exhibit highly right-skewed distributions, as evidenced by their high skewness scores and zero median values. This suggests that most users in these categories spend little or nothing, while a small group of users spend significantly more. The mean values for these columns are substantially higher than the medians, further emphasizing this trend. It is worth noting that all columns have a minimum value of zero, implying that no activity was recorded for some users in these categories. This aligns with the high outlier percentage reported in the Outliers Context section, suggesting that a significant number of users are not engaging or are not being accurately represented in these datasets. To address these issues, it may be beneficial to consider log-transforming or standardizing these highly skewed columns to better represent the data and reduce the impact of outliers.

**box_roomservice**

![box_roomservice](plots/box_roomservice_vs_transported.png)

**box_foodcourt**

![box_foodcourt](plots/box_foodcourt_vs_transported.png)

**box_vrdeck**

![box_vrdeck](plots/box_vrdeck_vs_transported.png)

**box_spa**

![box_spa](plots/box_spa_vs_transported.png)

**box_shoppingmall**

![box_shoppingmall](plots/box_shoppingmall_vs_transported.png)

**hist_roomservice**

![hist_roomservice](plots/histogram_roomservice.png)

**hist_foodcourt**

![hist_foodcourt](plots/histogram_foodcourt.png)

**hist_vrdeck**

![hist_vrdeck](plots/histogram_vrdeck.png)

**hist_age**

![hist_age](plots/histogram_age.png)

**hist_spa**

![hist_spa](plots/histogram_spa.png)

**hist_shoppingmall**

![hist_shoppingmall](plots/histogram_shoppingmall.png)


---

## 4. Correlations
In this analysis, there are no strong correlations present among the numerical columns, as indicated by a total of zero strong-correlated pairs and a false any_strong_correlation value. However, some notable correlations were identified that may provide insights into the data. For instance, a moderate positive correlation exists between the 'foodcourt' and 'vrdeck' usage, suggesting that guests who spend more time in one area might also be inclined to spend more time in the other. Similarly, there is a modest positive correlation between 'foodcourt', 'spa', and 'age'. This could imply that older guests may prefer spending their time at the food court or spa more than younger guests. Lastly, a weak positive correlation was found between 'vrdeck' and 'age', as well as between 'vrdeck' and 'spa', and between 'age' and 'spa'. These findings suggest that there might be some relationship among these variables, but it is not strong enough to raise concerns about multicollinearity. Overall, this is a positive finding, indicating that the features carry independent information.

![Correlations](plots/correlation_heatmap.png)

---

## 5. Categorical Features
The dataset contains a total of 5 categorical columns, with one high cardinality column, 'cabin', which has 6560 unique values, indicating a need for special handling such as target encoding to avoid losing valuable information during preprocessing. The binary columns, 'vip' and 'cryosleep', show significant imbalance, with 'vip' having only 2.3% of passengers being VIP, while 'cryosleep' has 35.8% of passengers in cryosleep. In terms of homeplanet distribution, the majority of passengers are from Earth (54.2%), followed by Europa (25.1%) and Mars (20.7%). The destination column shows that most passengers are headed to TRAPPIST-1e (69.5%), with a smaller percentage going to 55 Cancri e (21.1%) and PSO J318.5-22 (9.4%). These distributions provide insights into the origin and destination of the passengers in this dataset.

**bar_vip**

![bar_vip](plots/bar_vip_vs_transported.png)

**bar_homeplanet**

![bar_homeplanet](plots/bar_homeplanet_vs_transported.png)

**bar_cryosleep**

![bar_cryosleep](plots/bar_cryosleep_vs_transported.png)

**bar_destination**

![bar_destination](plots/bar_destination_vs_transported.png)


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
      "roomservice",
      "foodcourt",
      "vrdeck",
      "age",
      "spa",
      "shoppingmall"
    ],
    "categorical_columns": [
      "cabin",
      "vip",
      "homeplanet",
      "cryosleep",
      "destination"
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