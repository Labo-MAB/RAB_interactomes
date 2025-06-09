from collections import defaultdict
import re
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import upsetplot as ups

# Functions definition
def colname_to_mi(colname):
    " Convert column names to multiindex tuples "
    rab, rep = colname.split(' ')
    guanosine = re.match("[TD]", rep).group()
    num = rep[-1]
    return (rab, guanosine, num)


def get_orthologs(file):
    " Read the orthologs file from DIOPT and return a dictionary of orthologs "
    orthologs = pd.read_excel(file, header=1, 
                              usecols=['Search Term', 'Human Symbol', 'Weighted Score', 'Rank'],
                              index_col='Search Term')
    orthologs = orthologs[orthologs['Human Symbol'].notnull()] # Remove possible row with no human orthologs
    orthologs = orthologs[~orthologs.index.duplicated(keep='first')] # For duplicate gene names, keep best match
    return orthologs['Human Symbol'].to_dict()


def defaultdict_to_regular(d):
    " Convert multilayered defaultdict to regular dict"
    if isinstance(d, defaultdict):
        d = {k: defaultdict_to_regular(v) for k, v in d.items()}
    return d


def get_go_terms(go_dict, genes, set_of_interest='Jean'):
    " From a dictionary of GO terms, "
    go_terms = []
    for gene in genes:
        try:
            go_terms.extend(go_dict[gene])
        # No GO annotation, skip
        except KeyError:
            pass
    return list(np.unique(go_terms))

def get_annotation_stats(go_dict, genes):
    " Count the number of annotated and unannotated genes "
    annotated = np.intersect1d(genes, list(go_dict)).shape[0]
    unannotated = len(genes) - annotated
    return {'unannotated': unannotated, 'annotated': annotated}


def plot_upset(data, title=None, dataset_of_interest='This study', intersection_type='strict'):
    " Plot common interactors regardless of the capturing Rab "
    
    def total_intersections(data):
        " Prepare data to upset plot the total intersections between datasets "
        cat_serie = [pd.Series(True, index=list(elements), name=name)
                    for name, elements in data.items()]
        df = pd.concat(cat_serie, axis=1)
        df.where(df.notnull(), False, inplace=True)

        # Create
        mi = pd.MultiIndex.from_product([[True, False]]*len(data), names=data.keys())
        mi = mi.drop([idx for idx in mi if sum(idx) == 0])
        data = pd.Series(index=mi, name='id')
        
        idx_names = np.array(data.index.names)
        for idx in data.index:
            usecols = [name for name in idx_names[list(idx)]]
            data[idx] = np.unique(df.index[df[usecols].all(axis=1)]).shape[0]
        
        # workaround to get the good value for the total size of each datasets
        totals_idx = [idx for idx in data.index if sum(idx) == 1]
        for idx in totals_idx:
            target_total = data[idx]
            related_subsets = [subset_idx for subset_idx in data.index
                            if np.array(subset_idx)[np.array(idx)].any()]
            bad_total = data[related_subsets].sum()
            corrected_total = target_total - (bad_total - target_total)
            data[idx] = corrected_total

        
        return data

    # Transform data according to the desired intersection type
    transform_data = {'strict': ups.from_contents, 'total': total_intersections}
    data = transform_data[intersection_type](data)
    
    
    upsetplot = ups.UpSet(data=data, show_counts=True,
                          sort_categories_by='input',
                          min_degree=1 if intersection_type == 'strict' else 2)
    
    if isinstance(dataset_of_interest, str):
        upsetplot.style_categories([d for d in data if d != dataset_of_interest],
                                bar_facecolor='#5D5D5D', bar_edgecolor='#000000')
    elif isinstance(dataset_of_interest, list):
        upsetplot.style_categories([d for d in data if d not in dataset_of_interest],
                                bar_facecolor='#5D5D5D', bar_edgecolor='#000000')
    else:
        raise TypeError("dataset_of_interest should be a string or a list of strings")
    
    upsetplot.style_categories(dataset_of_interest, bar_facecolor='#709B92', bar_edgecolor='#0E6655')
    upsetplot.style_subsets(absent=dataset_of_interest, facecolor='#5D5D5D', edgecolor='#000000')
    upsetplot.style_subsets(present=dataset_of_interest, facecolor='#709B92', edgecolor='#0E6655')
    fig = upsetplot.plot()

    # Rotate counts and adjust position
    for child in fig['intersections'].get_children():
        if isinstance(child, mpl.text.Text):
            x, y = child.get_position()
            new_y  = y + fig['intersections'].transAxes.transform((1, -0.9))[1]
            child.set(horizontalalignment='left', rotation=40, position=(x-0.2, new_y))
            
    if title:
        plt.suptitle(title, y=1.03)
    return fig


def plot_stacked_bar(stacked_data, category_name):
    " From a dictionary of go annotations stats, make a stacked bar plot "
    def split_text(text):
        " Split dataset name into two lines "
        return re.sub(r' (?=\()|(?<=\)) ', '\n', text)
        
    def get_xaxis_coord(fig):
        " Get axes coordinate to draw common xaxis "
        xdata = [fig.axes[0].get_position().get_points()[0][0],
        fig.axes[-1].get_position().get_points()[1][0]]
        ydata = [fig.axes[0].get_position().get_points()[0][1]]*2
        return xdata, ydata
    
    colors = {'face': {'unannotated': '#EC7063', 'annotated': '#709B92'},
            'edge': {'unannotated': '#C0392B', 'annotated': '#0E6655'}} 
    ncol = len(stacked_data)
       
    fig, axes = plt.subplots(1, ncol, sharey=True, )
    for col, (ds, data) in zip(range(ncol), stacked_data.items()):
        ax = axes[col]
        
        for frame_pos in ['bottom', 'top', 'right']:
            ax.spines[frame_pos].set_visible(False)
            
        if col != 0:
            ax.spines['left'].set_visible(False)
            ax.tick_params(left=False)
            
        ax.set_title(split_text(ds), y=-0.1, fontsize=9, rotation=45,
                     va='top', ha='center')
        bottom = np.zeros(3)
        for label, values in data.items():
            ax.bar(category_name.keys(), values, width=0.9, bottom=bottom, 
                   label=label, color=colors['face'][label],
                   edgecolor=colors['edge'][label])
            bottom += values
            
    ax.legend(loc='upper right')
    xdata, ydata = get_xaxis_coord(fig)
    fig.add_artist(mpl.lines.Line2D(xdata, ydata, color='black', linewidth=0.9))
    return fig


def non_filtered_proportion(scores, threshold):
    " Get the proportion of non filtered bait-interactor pairs "
    return scores[scores >= threshold].shape[0] / scores.shape[0] * 100