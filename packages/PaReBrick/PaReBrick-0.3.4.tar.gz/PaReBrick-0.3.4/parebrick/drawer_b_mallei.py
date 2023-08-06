from parebrick.utils.data.parsers import parse_infercars_to_df
from parebrick.utils.data.stats import distance_between_blocks_distribution
from parebrick.utils.data.unique_gene_filters import filter_dataframe_unique

from collections import Counter

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import argparse
import os


def blocks_length_dist(df):
    return [end_ - start_ for start_, end_ in zip(df['chr_beg'], df['chr_end'])]


def lengths_between(state, log):
    plt.figure()
    distance_between_2d = []
    for chr, df_chr in df.groupby('chr'):
        if state == 'after':
            df_filtered = filter_dataframe_unique(df_chr)
            ds = distance_between_blocks_distribution(df_filtered)
        else:
            ds = distance_between_blocks_distribution(df_chr)
        for d in ds:
            distance_between_2d.append([chr, d])

    distance_between_df = pd.DataFrame(data=distance_between_2d, columns=['chromosome', 'distance'])
    sns.histplot(distance_between_df, bins=50, log_scale=(False, log), x='distance', hue='chromosome', element="step")

    plt.ylabel('Number of blocks')
    plt.xlabel('Length in nucleotides')
    plt.title(f'Length of fragments not covered by {"common" if state == "after" else "any"} blocks')

    plt.tight_layout()
    plt.xlim(xmin=0)

    plt.savefig(out_folder + f'lengths_between_{state}_filtering{"_log" if log else ""}.pdf')
    # plt.show()


def get_most_probable_block(df_block):
    cnt = Counter(df_block.chr)
    if len(cnt) == 1:
        return cnt.most_common(1)[0][0]
    else:
        (most1, freq1), (most2, freq2) = cnt.most_common(2)
        if freq1 / freq2 < 10:
            return most1 + ';' + most2
        else:
            return most1


def number_of_genomes_weighted(weighted, log):
    plt.figure()
    vs, ws, chroms = [], [], []

    for _, df_block in df.groupby('block'):
        # print(_, get_most_probable_block(df_block))
        vs.append(len(df_block.species.unique()))
        chroms.append(get_most_probable_block(df_block))
        lens = [row['chr_end'] - row['chr_beg'] for _, row in df_block.iterrows()]
        ws.append(np.mean(lens))

    df_draw = pd.DataFrame([[v, chr] for v, chr in zip(vs, chroms)], columns=['genomes', 'chromosome'])

    bins = 50 if max(vs) > 50 else max(vs)
    if weighted:
        # plt.hist(vs, bins=bins, weights=ws, log=log, alpha=0.7)
        sns.histplot(df_draw, x='genomes', weights=ws, hue='chromosome', bins=bins, log_scale=(False, log), element="step")
    else:
        # sns.histplot(vs, bins=bins, log_scale=(False, log), kde_kws={'alpha': 0.7})
        sns.histplot(df_draw, x='genomes', hue='chromosome', bins=bins, log_scale=(False, log), element="step")
        sns.histplot(df_draw, x='genomes', hue='chromosome', bins=bins, log_scale=(False, log), element="step")

    plt.ylabel('Length of fragments that are present\n in n genomes, nucleotides'
               if weighted else 'Number of blocks')
    plt.xlabel('Number of genomes')
    plt.title(f'{"Weighted f" if weighted else "F"}requency of synteny blocks')
    # plt.legend(loc='best')

    plt.xlim(xmin=0, xmax=max(vs))
    plt.tight_layout()
    plt.savefig(out_folder + f'blocks_frequency{"_weighted" if weighted else ""}{"_log" if log else ""}.pdf')
    # plt.show()


def block_length(log):
    plt.figure()
    df['length'] = df.chr_end - df.chr_beg

    sns.histplot(df, x='length', hue='chr', bins=50, log_scale=(False, log), element="step")

    plt.ylabel('Number of blocks')
    plt.xlabel('Length in nucleotides')
    plt.xlim(xmin=0)
    plt.title(f'Distribution of synteny blocks length')

    # plt.legend(loc=1)

    plt.tight_layout()
    plt.savefig(out_folder + f'block_lengths_distribution{"_log" if log else ""}.pdf')
    # plt.show()


def scatter_len_genomes_count():
    plt.figure()

    d2 = []
    for block, df_block in df.groupby('block'):
        lens = [row['chr_end'] - row['chr_beg'] for _, row in df_block.iterrows()]
        d2.append([len(df_block.species.unique()), np.mean(lens), get_most_probable_block(df_block)])

    draw_df = pd.DataFrame(d2, columns=['Number of genomes', 'Mean length of block', 'Chromosome'])
    sns.scatterplot(data=draw_df, x='Number of genomes', y='Mean length of block', hue='Chromosome', s=10)

    plt.title(f'Occurrence of synteny blocks vs its length')

    plt.tight_layout()
    plt.savefig(out_folder + f'scatter_number_length.pdf')


def pan_blocks(permutations=10_000):
    nbsss, pnsss, cnsss, xss, chrs = [], [], [], [], []
    colors = 'indianred', 'slateblue'
    for chr, df_chr in df.groupby('chr'):

        block_sets = [set(df_sp.block.unique()) for _, df_sp in df_chr.groupby('species')]
        nbss, pnss, cnss = [], [], []

        for _ in range(permutations):
            block_sets = np.random.permutation(block_sets)
            nbs, pns, cns = [], [], []
            accumulate_set = set()
            accumulate_set_intersect = set(df.block.unique())
            for bs in block_sets:
                left = bs - accumulate_set
                nbs.append(len(left))
                accumulate_set |= bs
                accumulate_set_intersect &= bs
                pns.append(len(accumulate_set))
                cns.append(len(accumulate_set_intersect))

            nbss.append(nbs)
            pnss.append(pns)
            cnss.append(cns)

        nbss = np.array(nbss)
        xs = list(range(1, len(block_sets) + 1))

        nbsss.append(nbss)
        pnsss.append(pnss)
        cnsss.append(cnss)
        chrs.append(chr)
        xss.append(xs)

    def new_blocks():
        plt.figure()
        for nbss, xs, chr, color in zip(nbsss, xss, chrs, colors):

            plt.plot(xs, np.median(nbss, axis=0), label=f'chr:{chr} median (different permutations)', c=color)

            plt.fill_between(xs, np.percentile(nbss, 5, axis=0), np.percentile(nbss, 95, axis=0),
                                 alpha=0.4, color=color, label=f'90% confidence interval')

        plt.xlabel('Number of genomes')
        plt.ylabel('New blocks')
        plt.title('New blocks as a function of number of genomes')
        plt.legend(loc='upper right')

        plt.ylim(ymax=np.percentile(nbsss[0], 100, axis=0)[1], ymin=0)
        plt.xlim(xmin=1, xmax=max(xss[0]))

        # plt.subplots_adjust(top=0.99, right=0.99)
        plt.tight_layout()
        plt.savefig(out_folder + 'new_blocks.pdf')
        # plt.show()

    def pan():
        plt.figure()
        for pnss, xs, chr, color in zip(pnsss, xss, chrs, colors):
            plt.plot(xs, np.median(pnss, axis=0), label=f'chr:{chr} median (different permutations)', c=color)
            plt.fill_between(xs, np.percentile(pnss, 5, axis=0), np.percentile(pnss, 95, axis=0),
                             alpha=0.4, color=color, label=f'90% confidence interval')
            # for perc in range(5, 50, 5):
            #     plt.fill_between(xs, np.percentile(pnss, perc, axis=0), np.percentile(pnss, 100 - perc, axis=0),
            #                      alpha=0.1, color=color)

        plt.xlabel('Number of genomes')
        plt.ylabel('Pan-blocks count')
        plt.title('Pangenome')
        plt.legend(loc='lower right')

        # plt.ylim(ymin=np.percentile(pnss, 5, axis=0)[0])
        plt.xlim(xmin=1, xmax=max(xss[0]))
        # plt.subplots_adjust(top=0.99, right=0.99)
        plt.tight_layout()
        plt.savefig(out_folder + 'pan_blocks.pdf')
        # plt.show()

    def core():
        plt.figure()
        for cnss, xs, chr, color in zip(cnsss, xss, chrs, colors):
            plt.plot(xs, np.median(cnss, axis=0), label=f'chr:{chr} median (different permutations)', c=color)
            plt.fill_between(xs, np.percentile(cnss, 5, axis=0), np.percentile(cnss, 95, axis=0),
                             alpha=0.4, color=color, label=f'90% confidence interval')
            # for perc in range(5, 50, 5):
            #     plt.fill_between(xs, np.percentile(pnss, perc, axis=0), np.percentile(pnss, 100 - perc, axis=0),
            #                      alpha=0.1, color=color)

        plt.xlabel('Number of genomes')
        plt.ylabel('Core-blocks count')
        plt.title('Coregenome')
        plt.legend(loc='best')

        # plt.ylim(ymin=np.percentile(pnss, 5, axis=0)[0])
        plt.xlim(xmin=1, xmax=max(xss[0]))
        # plt.subplots_adjust(top=0.99, right=0.99)
        plt.tight_layout()
        plt.savefig(out_folder + 'core_blocks.pdf')
        # plt.show()

    new_blocks()
    pan()
    core()

def main():
    global out_folder, df

    parser = argparse.ArgumentParser(
        description='Building charts for pan-genome analysis based on synteny blocks.')

    parser.add_argument('--infercars_file', '-f', required=True,
                      help='Path to file in infercars format, can be found in main script output')

    parser.add_argument('--output', '-o', default='parebrick_charts', help='Path to output folder.')

    args = parser.parse_args()
    d = vars(args)

    file, out_folder = d['infercars_file'], d['output']

    if out_folder[-1] != '/': out_folder += '/'
    os.makedirs(out_folder, exist_ok=True)

    df = parse_infercars_to_df(file)
    df = df[df.apply(lambda x: x['species'] != 'BUMA.0721.00028', axis=1)]

    sns.set(style="whitegrid", font="serif")

    print('Plotting lengths between blocks')
    lengths_between('before', log=False)
    lengths_between('after', log=False)

    print('Plotting number of genomes in blocks')
    number_of_genomes_weighted(weighted=False, log=False)
    number_of_genomes_weighted(weighted=True, log=False)

    print('Plotting blocks length distribution')
    block_length(log=False)

    print('Plotting scatter for occurrence of synteny blocks vs its length')
    scatter_len_genomes_count()

    print('Plotting pan-genome plots')
    pan_blocks()

if __name__ == "__main__":
    main()