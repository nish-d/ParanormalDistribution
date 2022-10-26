
import matplotlib.pyplot as plt
import numpy as np

def target_encoding(train_df, cat_cols, target_feature):
    target_std = train_df[target_feature].std()
    for col in cat_cols:
        encoded_std = train_df.groupby(col)[target_feature].mean().std()
        if target_std < encoded_std:
            train_df[col] = train_df.groupby(col)[target_feature].transform('mean')


def target_encoding_test(train_df, cat_cols, target_feature, test_df):
    target_std = train_df[target_feature].std()
    for col in cat_cols:
        encoded_std = train_df.groupby(col)[target_feature].mean().std()
        if target_std < encoded_std:
            test_df[col] = train_df.groupby(col)[target_feature].transform('mean')

def target_encoding_price(train_df, cat_cols, target_feature = 'price_per_sqft'):
    target_std = train_df[target_feature].std()
    for col in cat_cols:
        encoded_std = train_df.groupby(col)[target_feature].mean().std()
        if target_std < encoded_std:
            train_df[col] = train_df.groupby(col)[target_feature].transform('mean')

def target_encoding_test_price(train_df, cat_cols, test_df, target_feature = 'price_per_sqft'):
    target_std = train_df[target_feature].std()
    for col in cat_cols:
        encoded_std = train_df.groupby(col)[target_feature].mean().std()
        if target_std < encoded_std:
            test_df[col] = train_df.groupby(col)[target_feature].transform('mean')

def plot_variance(pca, width = 8, dpi = 100):
    #create figure
    fig, axs = plt.subplots(1, 2)
    n = pca.n_components_
    grid = np.arange(1, n + 1)
    #Explained variance
    evr = pca.explained_variance_ratio_
    axs[0].bar(grid, evr)
    axs[0].set(xlabel = 'Component', title = '% Explained Variance', ylim = (0.0, 1.0))
    #Cumulative Variance
    cv = np.cumsum(evr)
    axs[1].plot(np.r_[0, grid], np.r_[0, cv], 'o-')
    axs[1].set(xlabel = 'Component', title = '% Cumulative Variance', ylim = (0.0, 1.0))
    #Set Up Figure
    fig.set(figwidth = 12, dpi = 100)
    return axs