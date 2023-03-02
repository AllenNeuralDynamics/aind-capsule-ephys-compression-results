import pandas as pd
import numpy as np


def is_notebook() -> bool:
    """Checks if Python is running in a Jupyter notebook

    Returns
    -------
    bool
        True if notebook, False otherwise
    """
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False


### PLOTTING UTILS ###
def prettify_axes(axs, label_fs=15):
    """Makes axes prettier by removing top and right spines and fixing label fontsizes.

    Parameters
    ----------
    axs : list
        List of matplotlib axes
    label_fs : int, optional
        Label font size, by default 15
    """
    if not isinstance(axs, (list, np.ndarray)):
        axs = [axs]

    axs = np.array(axs).flatten()

    for ax in axs:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        ax.set_xlabel(ax.get_xlabel(), fontsize=label_fs)
        ax.set_ylabel(ax.get_ylabel(), fontsize=label_fs)


### STATS UTILS ###
def cohen_d(x, y):
    """Computes the Cohen's d coefficient between samples x and y

    Parameters
    ----------
    x : np.array
        Sample x
    y : np.array
        Sample y

    Returns
    -------
    float
        the Cohen's d coefficient
    """
    nx = len(x)
    ny = len(y)
    dof = nx + ny - 2
    print(np.mean(x), np.mean(y))
    return (np.mean(x) - np.mean(y)) / np.sqrt(((nx-1)*np.std(x, ddof=1) ** 2 + (ny-1)*np.std(y, ddof=1) ** 2) / dof)


def stat_test(df, column_group_by, test_columns, sig=0.01, verbose=False):
    """Performs statistical tests and posthoc analysis (in case of multiple groups).

    If the distributions are normal with equal variance, it performs the ANOVA test and
    posthoc T-tests (parametric).
    Otherwise, the non-parametric Kruskal-Wallis and posthoc Conover's tests are used.

    Parameters
    ----------
    df : pandas.DataFrame
        The input dataframe
    column_group_by : str
        The categorical column used for grouping
    test_columns : list
        The columns containing real values to test for differences.
    sig : float, optional
        Significance level, by default 0.01
    verbose : bool, optional
        If True output is verbose, by default False

    Returns
    -------
    dict
        The results dictionary containing, for each metric:

        - "pvalue" :  the p-value for the multiple-sample test
        - "posthoc" : DataFrame with posthoc p-values
        - "cohens": DataFrame with Cohen's d coefficients for significant posthoc results
        - "parametric": True if parametric, False if non-parametric
    """
    from scipy.stats import kruskal, f_oneway, shapiro, levene, ttest_ind, mannwhitneyu
    import scikit_posthocs as sp

    df_gb = df.groupby(column_group_by)
    results = {}
    parametric = False
    for metric in test_columns:
        if verbose:
            print(f"\nTesting metric {metric}\n")
        results[metric] = {}
        samples = ()
        for i, val in enumerate(np.unique(df[column_group_by])):
            df_val = df_gb.get_group(val)
            if verbose:
                print(f"Sample {i+1}: {val} - n. {len(df_val)}")
            samples += (df_val[metric].values,)
        # shapiro test for normality
        for sample in samples:
            _, pval_n = shapiro(sample)
            if pval_n < sig:
                parametric = True
                if verbose:
                    print("Non normal samples: using non parametric tests")
                break
        # levene test for equal variances
        if not parametric:
            _, pval_var = levene(*samples)
            if pval_var < sig:
                if verbose:
                    print("Non equal variances: using non parametric tests")
                parametric = True
        if len(samples) > 2:
            if verbose:
                print("Population test")
            parametric = True
            if parametric:
                test_fun = kruskal
                ph_test = sp.posthoc_conover
            else:
                test_fun = f_oneway
                ph_test = sp.posthoc_ttest
            # run test:
            _, pval = test_fun(*samples)
            pval_round = pval
            if pval < sig:
                # compute posthoc and cohen's d
                posthoc = ph_test(df, val_col=metric, group_col=column_group_by, p_adjust='holm',
                                  sort=False)

                # here we just consider the bottom triangular matrix and just keep significant values
                pvals = np.tril(posthoc.to_numpy(), -1)
                pvals[pvals == 0] = np.nan
                pvals[pvals >= sig] = np.nan

                # cohen's d are computed only on significantly different distributions
                ph_c = pd.DataFrame(pvals, columns=posthoc.columns, index=posthoc.index)
                pval_round = ph_c.copy()
                cols = ph_c.columns.values
                cohens = ph_c.copy()
                for index, row in ph_c.iterrows():
                    val = row.values
                    ind_non_nan, = np.nonzero(~np.isnan(val))
                    for col_ind in ind_non_nan:
                        x = df_gb.get_group(index)[metric].values
                        y = df_gb.get_group(cols[col_ind])[metric].values
                        cohen = cohen_d(x, y)
                        cohens.loc[index, cols[col_ind]] = cohen
                        pval = ph_c.loc[index, cols[col_ind]]
                        if pval < 1e-10:
                            exp = -10
                        else:
                            exp = int(np.ceil(np.log10(pval)))
                        pval_round.loc[index, cols[col_ind]] = f"<1e{exp}"
                if verbose and is_notebook():
                    print("Post-hoc")
                    display(posthoc)
                    print("Post-hoc")
                    display(pval_round)
                    print("Cohen's d")
                    display(cohens)
            else:
                if verbose:
                    print("Non significant")
                posthoc = None
                pval_round = None
                cohens = None
        else:
            posthoc = None
            if verbose:
                print("2-sample test")
            if parametric:
                test_fun = ttest_ind
            else:
                test_fun = mannwhitneyu
            _, pval = test_fun(*samples)
            if pval < sig:
                cohens = cohen_d(*samples)
                if verbose:
                    if pval < 1e-10:
                        pval_round = "<1e-10"
                    else:
                        exp = int(np.ceil(np.log10(pval)))
                        pval_round = f"<1e{exp}"
                    print(f"P-value {pval_round} ({pval}) - effect size: {np.round(cohens, 3)}")
            else:
                if verbose:
                    print("Non significant")
                pval_round = None
                cohens = None

        results[metric]["pvalue"] = pval
        results[metric]["pvalue-round"] = pval_round
        results[metric]["posthoc"] = posthoc
        results[metric]["cohens"] = cohens
        results[metric]["parametric"] = parametric
        
    return results
