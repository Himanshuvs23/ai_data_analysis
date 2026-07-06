# Import Libraries
import pandas as pd
from typing import List, Dict

# Import global constants
from config.settings import (
    HIGH_CARDINALITY_THRESHOLD,
    HIGH_OUTLIER_THRESHOLD,
    MEDIUM_OUTLIER_THRESHOLD,
    HIGH_MISSING_THRESHOLD,
    MEDIUM_MISSING_THRESHOLD,
    MODERATE_IMBALANCE_THRESHOLD,
    HIGH_IMBALANCE_THRESHOLD,
    NOTABLE_CORRELATION_THRESHOLD,
    STRONG_CORRELATION_THRESHOLD
)

def get_skewness_label(
    skewness: float
) -> str:
    if (skewness <= -1):
        label = "Highly left-skewed"
    elif (skewness > -1 and skewness < -0.5):
        label = "Moderately left-skewed"
    elif (skewness >= -0.5 and skewness <= 0.5):
        label = "Approximately symmetric"
    elif (skewness > 0.5 and skewness < 1):
        label = "Moderately right-skewed"
    elif(skewness >= 1):
        label = "Highly right-skewed"
    return label

def get_outlier_summary(
    df: pd.DataFrame,
    numerical_columns: List[str]
) -> Dict:
    column_report = {}
    total_high_severity_columns = 0
    total_medium_severity_columns = 0
    total_low_severity_columns = 0
    for col in numerical_columns:
        series = df[col].dropna()

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)
        outlier_mask = (
            (series < lower_bound) | (series > upper_bound)
        )

        number_of_outliers = int(outlier_mask.sum())
        outlier_percentage = round(
            (number_of_outliers / len(series)) * 100, 2
        )

        severity = None
        if outlier_percentage <= MEDIUM_OUTLIER_THRESHOLD:
            severity = "Low"
            total_low_severity_columns += 1
        elif outlier_percentage <= HIGH_OUTLIER_THRESHOLD:
            severity = "Moderate"
            total_medium_severity_columns += 1
        else:
            severity = "High"
            total_high_severity_columns += 1

        if severity:
            column_report[col] = {
                "outlier_percentage": outlier_percentage,
                "severity": severity
            }
    
    summary = {
        "total_outlier_columns": (total_high_severity_columns + total_medium_severity_columns + total_low_severity_columns),
        "total_high_severity_columns": total_high_severity_columns,
        "total_medium_severity_columns": total_medium_severity_columns,
        "total_low_severity_columns": total_low_severity_columns,
        "any_high_severity": True if total_high_severity_columns > 0 else False
    }
    return {
        'summary': summary,
        'columns': column_report
    }

def get_missing_summary(
    df: pd.DataFrame
) -> Dict:
    # Missing Value Report
    column_report = {}
    num_columns_with_missing_values = 0
    high_severity_present = False
    max_missing_pct = 0
    for col in df.columns:
        missing_pct = float(round((df[col].isna().sum() / len(df)) * 100, 2))
        max_missing_pct = max(max_missing_pct, missing_pct)
        severity = None
        if missing_pct <= MEDIUM_MISSING_THRESHOLD:
            severity = "Low"
        elif missing_pct < HIGH_MISSING_THRESHOLD:
            severity = "Moderate"
        else:
            severity = "High"
            high_severity_present = True
        
        if severity != None:
            column_report[col] = {
                "missing_percentage": missing_pct,
                "severity": severity
            }
            num_columns_with_missing_values += 1

    summary = {
        "total_missing_columns": num_columns_with_missing_values,
        "max_missing_percentage": max_missing_pct,
        "any_high_severity": high_severity_present,
    }

    return {
        'summary': summary,
        'columns': column_report
    }

def get_correlation_summary(
    df: pd.DataFrame,
    numerical_columns: List[str],
    strong_threshold: float = STRONG_CORRELATION_THRESHOLD,
    notable_threshold: float = NOTABLE_CORRELATION_THRESHOLD
) -> Dict:
    correlation_matrix = df[numerical_columns].corr().round(3)
    strong_correlated_pairs = []
    notable_correlated_pairs = []
    columns = correlation_matrix.columns.tolist()

    for i in range(len(columns)):
        for j in range(i + 1, len(columns)):
            corr_value = correlation_matrix.iloc[i, j]
            pair = {
                "col1": columns[i],
                "col2": columns[j],
                "correlation": round(float(corr_value), 3)
            }
            if abs(corr_value) >= strong_threshold:
                strong_correlated_pairs.append(pair)
            elif abs(corr_value) >= notable_threshold:
                notable_correlated_pairs.append(pair)
            # Below 0.1 → Silently dropped

    return {
        "summary": {
            "any_strong_correlation": len(strong_correlated_pairs) > 0,
            "strong_threshold": strong_threshold,
            "total_strong_pairs": len(strong_correlated_pairs),
        },
        "strong_correlated_pairs": strong_correlated_pairs,
        "notable_correlated_pairs": notable_correlated_pairs
    }

def get_class_balance(
    df: pd.DataFrame,
    target: str
) -> Dict:
    target_distribution = {
        str(k): round(v, 3)
        for k, v in (
            df[target].value_counts(normalize = True).items()
        )
    }

    values = list(target_distribution.values())
    highest_distribution = max(values)
    lowest_distribution = min(values)
    
    distribution_diff = abs(highest_distribution - lowest_distribution) * 100
    class_imbalance_severity = None
    is_imbalanced = True
    if distribution_diff <= MODERATE_IMBALANCE_THRESHOLD:
        class_imbalance_severity = "Normal"
        is_imbalanced = False
    elif distribution_diff <= HIGH_IMBALANCE_THRESHOLD:
        class_imbalance_severity = "Moderate"
    else:
        class_imbalance_severity = "High"
    
    return {
        "summary": {
            "target_column": target,
            "imbalance_severity": class_imbalance_severity,
            "is_imbalanced": is_imbalanced
        },
        "distribution": target_distribution
    }

def get_categorical_summary(
    df: pd.DataFrame,
    categorical_columns: List[str],
    high_cardinality_threshold: float = HIGH_CARDINALITY_THRESHOLD
) -> Dict:
    columns = {}
    high_cardinality = []
    binary = []

    for column in categorical_columns:
        unique_values = df[column].nunique()
        is_high_cardinality = unique_values > high_cardinality_threshold

        columns[column] = {
            "unique_values": unique_values,
            "is_high_cardinality": is_high_cardinality,
        }

        if is_high_cardinality:
            high_cardinality.append(column)
        else:
            columns[column]["distribution"] = {
                str(k): round(v, 3)
                for k, v in df[column].value_counts(normalize=True).items()
            }
            if unique_values == 2:
                binary.append(column)

    return {
        "summary": {
            "total_categorical_columns": len(categorical_columns),
            "high_cardinality_columns": high_cardinality,
            "binary_columns": binary,
        },
        "columns": columns
    }

def get_numerical_summary(
    df: pd.DataFrame,
    numerical_columns: List[str]
) -> Dict:
    columns = {}
    for col in numerical_columns:
        series = df[col].dropna()
        skew = round(float(series.skew()), 3)
 
        columns[col] = {
            "mean": round(float(series.mean()), 2),
            "median": round(float(series.median()), 2),
            "std": round(float(series.std()), 2),
            "min": round(float(series.min()), 2),
            "max": round(float(series.max()), 2),
            "skewness": skew,
            "skewness_label": get_skewness_label(skew),
        }
 
    return {
        "summary": {
            "total_numerical_columns": len(numerical_columns),
        },
        "columns": columns
    }