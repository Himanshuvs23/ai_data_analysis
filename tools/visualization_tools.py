# Import Libraries
import numpy as np
import pandas as pd
import seaborn as sns
from pathlib import Path

# Change backend for Matplotlib
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from typing import List, Iterable, Tuple, Optional

def plot_bar(
    values: List[float],
    labels: List[str],
    x_label: str,
    y_label: str,
    title: str,
    output_dir: str,
    file_name: str,
    color: str = "steelblue",
    alpha: float = 0.7,
    fig_size: Tuple[int, int] = (10, 6)
) -> str:
    plt.figure(figsize = fig_size)
    bars = plt.bar(labels, values, color = color, alpha = alpha)

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{height:.1f}",
            ha = "center",
            va = "bottom",
            fontsize = 9,
        )

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks(rotation = 45, ha = "right")
    plt.tight_layout()
    
    relative_path = f"plots/{file_name}.png"
    save_path = str(Path(output_dir) / relative_path)
    plt.savefig(save_path)
    plt.close()
    return relative_path

def plot_correlation_heatmap(
    df: pd.DataFrame,
    columns: List[str],
    output_dir: str,
    file_name: str,
    title: str = 'Correlation Heatmap',
    fig_size: tuple[int, int] = (8, 8)
) -> str:
    corr_matrix = df[columns].corr()
    plt.figure(figsize = fig_size)
    sns.heatmap(
        corr_matrix,
        annot = True,
        fmt = '.2f',
        cmap = 'coolwarm',
        vmin = -1,
        vmax = 1,
        square = True,
        linewidths = 0.5
    )
    plt.title(title)
    plt.tight_layout()
    
    relative_path = f"plots/{file_name}.png"
    save_path = str(Path(output_dir) / relative_path)
    plt.savefig(save_path)
    plt.close()
    return relative_path

def plot_histogram(
    series: pd.Series,
    col_name: str,
    output_dir: str,
    file_name: str,
    num_bins: int = 30,
    color: str = "steelblue",
    alpha: float = 0.7,
    fig_size: Tuple[int, int] = (10, 6)
) -> str:
    bins = np.linspace(series.min(), series.max(), num_bins + 1)
    bin_centers = (bins[:-1] + bins[1:]) / 2
    counts, _ = np.histogram(series, bins = bins)

    plt.figure(figsize = fig_size)
    plt.hist(series, bins = bins, color = color, alpha = alpha, edgecolor = "black", linewidth = 1)
    plt.plot(bin_centers, counts, color = color, linestyle = "--", linewidth = 1.5)

    plt.xlabel(col_name)
    plt.ylabel("Count")
    plt.title(f"Distribution - {col_name}")
    plt.xticks(bins, rotation = 45)
    plt.tight_layout()

    relative_path = f"plots/{file_name}.png"
    save_path = str(Path(output_dir) / relative_path)
    plt.savefig(save_path)
    plt.close()
    return relative_path

def plot_stacked_bar_by_target(
    feature: Iterable,
    target: Iterable,
    x_label: str,
    y_label: str,
    title: str,
    output_dir: str,
    file_name: str,
    colors: List[str] = None,
    alpha: float = 0.8,
    rotation: int = 0,
    fig_size: Tuple[int, int] = (10, 6)
) -> str:
    cross_tab = pd.crosstab(feature, target, normalize = 'index') * 100
    ax = cross_tab.plot(
        kind = 'bar',
        stacked = True,
        edgecolor = 'black',
        figsize = fig_size,
        color = colors,
        alpha = alpha
    )
    for bars in ax.containers:
        for bar in bars:
            height = bar.get_height()
            if height > 2:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_y() + height / 2,
                    f"{height:.1f}%",
                    ha = 'center',
                    va = 'center',
                    fontsize = 9
                )
    
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks(rotation = rotation)
    plt.tight_layout()
    
    relative_path = f"plots/{file_name}.png"
    save_path = str(Path(output_dir) / relative_path)
    plt.savefig(save_path)
    plt.close()
    return relative_path

def plot_box_by_target(
    feature: Iterable,
    target: Iterable,
    x_label: str,
    y_label: str,
    title: str,
    output_dir: str,
    file_name: str,
    log_scale: bool = False,
    colors: List[str] = None,
    alpha: float = 0.6,
    fig_size: Tuple[int, int] = (10, 6)
) -> str:
    feature = feature.reset_index(drop = True)
    target = target.reset_index(drop = True)

    if log_scale:
        feature = feature.fillna(0) + 1
        y_label = f"{y_label} (log scale)"
        title = f"{title} (Log Scale)"

    classes = sorted(target.unique())
    data = [feature[target == cls] for cls in classes]

    if colors is None:
        colors = ['blue', 'orange', 'green', 'red'][:len(classes)]

    plt.figure(figsize = fig_size)
    bp = plt.boxplot(
        data,
        labels = classes,
        patch_artist = True,
        medianprops = dict(color = 'black'),
        whiskerprops = dict(color = 'black'),
        capprops = dict(color = 'black'),
        flierprops = dict(markeredgecolor = 'black')
    )
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(alpha)

    if log_scale:
        plt.yscale('log')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.tight_layout()

    relative_path = f"plots/{file_name}.png"
    save_path = str(Path(output_dir) / relative_path)
    plt.savefig(save_path)
    plt.close()
    return relative_path

def plot_grouped_bar_by_target(
    feature: Iterable,
    target: Iterable,
    x_label: str,
    y_label: str,
    title: str,
    output_dir: str,
    file_name: str,
    fig_size: Tuple[int, int] = (10, 6)
) -> str:
    cross_tab = (pd.crosstab(feature, target) / len(target)) * 100
    plt.figure(figsize = fig_size)
    cross_tab.plot(
        kind = 'bar',
        width = 0.8,
        edgecolor = 'black'
    )

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend(title = target.name)
    plt.xticks(rotation = 0)
    plt.tight_layout()
    
    relative_path = f"plots/{file_name}.png"
    save_path = str(Path(output_dir) / relative_path)
    plt.savefig(save_path)
    plt.close()
    return relative_path

def plot_2d_scatter_by_class(
    x: pd.Series,
    y: pd.Series,
    target: pd.Series,
    output_dir: str,
    file_name: str,
    title: Optional[str] = None,
    figsize: tuple = (10, 6),
    alpha: float = 0.3,
    s: int = 1,
    colors: Optional[dict] = None,
    labels: Optional[dict] = None
) -> str:
    unique_classes = sorted(target.unique())

    default_colors = {cls: color for cls, color in zip(unique_classes, ['blue', 'orange', 'red'])}
    default_labels = {cls: str(cls) for cls in unique_classes}

    colors = colors or default_colors
    labels = labels or default_labels

    plt.figure(figsize = figsize)
    for cls in unique_classes:
        mask = (target == cls).values
        plt.scatter(
            x[mask],
            y[mask],
            c = colors[cls],
            label = labels[cls],
            alpha = alpha,
            s = s
        )
    
    plt.xlabel(x.name)
    plt.ylabel(y.name)
    plt.title(title or f'{x.name} vs {y.name}')
    plt.legend()
    plt.tight_layout()
    
    relative_path = f"plots/{file_name}.png"
    save_path = str(Path(output_dir) / relative_path)
    plt.savefig(save_path)
    plt.close()
    return relative_path