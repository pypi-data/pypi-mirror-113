import seaborn as sns
import matplotlib.pyplot as plt

from pathlib import Path

def heatmap(dataframe, outdir, method='pearson'):
    plt.figure(figsize=(15, 13))
    sns.heatmap(dataframe.corr(method=f"{method}"), annot=True, vmin=-1, vmax=1, cmap='coolwarm', fmt=".2f")
    plt.title(f"{method}")
    plt.savefig(Path(outdir).joinpath(f'corr_{method}.png'))
