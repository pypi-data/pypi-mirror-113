####
# title: feat.py
#
# language: Python3.8
# date: 2020-06-00
# license: GPL>=v3
# author: Jenny, bue
#
# description:
#   python3 script for single cell feature extraction
####

# libraries
from jinxif import config
from jinxif import basic
from jinxif import thresh
import json
#import matplotlib as mpl
#mpl.use('agg')
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import scipy
from skimage import io, measure, segmentation
import subprocess
import sys
import time

# PIL is backend from skimage io
import PIL
PIL.Image.MAX_IMAGE_PIXELS = None

# development
#import importlib
#importlib.reload()

# global var
s_path_module = os.path.abspath(os.path.dirname(__file__))
#s_path_module = re.sub(r'jinxif$','', s_path_module)


# functions
##################################################################
# segmentation partition and intensity based feature extraction #
##################################################################

def _extract_feat(
        ai_labels,
        ai_intensity_image,
        ls_properties = ['centroid','mean_intensity','area','eccentricity']
    ):
    '''
    version: 2021-06-16
    used

    input:
        ai_labels: numpy array with cell labels.
        ai_intensity_image: numpy array with intensity values.
        ls_properties: list of properties to extract with measure.regionprops_table.

    output:
        df_prop: dataframe with the extracted features, here called properties.

    description:
        given labels and intensity image, extract features to dataframe
    '''
    l_props = measure.regionprops_table(
        label_image = ai_labels,
        intensity_image = ai_intensity_image,
        properties = ls_properties
    )
    df_prop = pd.DataFrame(l_props)
    return(df_prop)


def _contract_label(
        ai_labels,
        i_distance = 3,
    ):
    '''
    version: 2021-06-16
    used {_subcellular_regions}

    input:
        ai_labels: numpy array with cell labels.
        i_distance: integer distance of pixels the cells should be shrunken.

    output:
        ai_rim_labels: numpy array with cell labels defining the shrunken rim.

    description:
        contract labels by a fixed number of pixels.
        function gives the shrunke rim back!
    '''
    ai_shrunk_labels = ai_labels.copy()
    ab_boundaries = segmentation.find_boundaries(ai_labels, mode='outer')
    ai_shrunk_labels[ab_boundaries] = 0
    ab_foreground = ai_shrunk_labels != 0
    ar_distances, (ai_i, ai_j) = scipy.ndimage.distance_transform_edt(
        ab_foreground,
        return_indices=True,
    )
    ab_mask = ab_foreground & (ar_distances <= i_distance)
    ai_shrunk_labels[ab_mask] = ai_shrunk_labels[ai_i[ab_mask], ai_j[ab_mask]]
    ai_rim_labels = ai_labels - ai_shrunk_labels
    return(ai_rim_labels)


def _expand_label(
        ai_labels,
        i_distance = 3,
    ):
    '''
    version: 2021-06-16
    used {_subcellular_regions, combine_labels}

    input:
        ai_labels: numpy array with cell labels.
        i_distance: integer distance of pixels the cells sould be expanded.

    output:
        ai_ring_labels: numpy array with cell labels defining the grown rim.
        ai_grown_labels: numpy array with cell labels defining the whole grown cell.

    description:
        expand the nucelar labels by a fixed number of pixels
    '''
    ai_shrunk_labels = ai_labels.copy()
    ab_boundaries = segmentation.find_boundaries(ai_labels, mode='outer') #thick
    ai_shrunk_labels[ab_boundaries] = 0
    ab_background = ai_shrunk_labels == 0
    ar_distances, (ai_i, ai_j) = scipy.ndimage.distance_transform_edt(
        ab_background,
        return_indices=True,
    )
    ai_grown_labels = ai_labels.copy()
    ab_mask = ab_background & (ar_distances <= i_distance)
    ai_grown_labels[ab_mask] = ai_shrunk_labels[ai_i[ab_mask], ai_j[ab_mask]]
    ai_ring_labels = ai_grown_labels - ai_shrunk_labels
    #ai_ring_labels = ai_grown_labels[ai_grown_labels != ai_shrunk_labels]
    return(ai_ring_labels, ai_grown_labels)


def _straddle_label(
        ai_labels,
        i_distance = 3,
    ):
    '''
    version: 2021-06-16
    used {_subcellular_regions}

    input:
        ai_labels: numpy array with cell labels.
        i_distance: integer distance of pixels the cells sould be straddled.

    output:
        ai_membrane_labels: numpy array with membranes label.
        ai_grown_labels: numpy array with cell labels defining the whole grown cell?
        ai_shrunk_labels: numpy array with cell labels defining the whole shrunken cell.

    description:
        expand and contract labels by a fixed number of pixels
    '''
    # bue 20210609: could maybe be solved by calling contract_lable and expand_label
    ai_shrunk_labels = ai_labels.copy()
    ai_grown_labels = ai_labels.copy()
    ab_boundaries = segmentation.find_boundaries(ai_labels, mode='outer')
    ai_shrunk_labels[ab_boundaries] = 0
    ab_foreground = ai_shrunk_labels != 0
    ab_background = ai_shrunk_labels == 0
    ar_distances_f, (ai_i, ai_j) = scipy.ndimage.distance_transform_edt(
        ab_foreground,
        return_indices = True
    )
    ar_distances_b, (ai_i, ai_j) = scipy.ndimage.distance_transform_edt(
        ab_background,
        return_indices=True
    )
    ab_mask_f = ab_foreground & (ar_distances_f <= i_distance)
    ab_mask_b = ab_background & (ar_distances_b <= i_distance + 1)
    ai_shrunk_labels[ab_mask_f] = 0
    ai_grown_labels[ab_mask_b] = ai_grown_labels[ai_i[ab_mask_b], ai_j[ab_mask_b]]
    ai_membrane_labels = ai_grown_labels - ai_shrunk_labels
    #ai_membrane_labels = ai_grown_labels[ai_grown_labels != ai_shrunk_labels]
    return(ai_membrane_labels, ai_grown_labels, ai_shrunk_labels)


def _subcellular_regions(
        ai_labels,
        i_distance_short = 2,
        i_distance_long = 5,
    ):
    '''
    version: 2021-06-16
    used
    bue 2021-06-16: maybe slight memory overkill.

    input:
        ai_labels: numpy array with cell labels.
        i_distance_short: shorter integer distance of pixels the cells sould be processed.
        i_distance_long: longer integer distance of pixels the cells sould be processed.

    output:
        dtai_loc_sl: dictionary of tuples of numpy arrays with short and long numpay array cell label result.

    description:
        calculate subcellular segmentation regions from nuclei or cell segmentation mask.
    '''
    ai_membrane_short = _contract_label(ai_labels, i_distance=i_distance_short)
    ai_membrane_long = _contract_label(ai_labels, i_distance=i_distance_long)
    ai_ring_short, ai_grown_short = _expand_label(ai_labels, i_distance=i_distance_short)
    ai_ring_long, ai_grown_long = _expand_label(ai_labels, i_distance=i_distance_long)
    ai_straddle_short, _, ai_shrunk_short = _straddle_label(ai_labels, i_distance=i_distance_short)
    ai_straddle_long, _, ai_shrunk_long = _straddle_label(ai_labels, i_distance=i_distance_long)
    dtai_loc_sl={
        'membrane': (ai_membrane_short, ai_membrane_long),
        'ring': (ai_ring_short, ai_ring_long),
        'straddle': (ai_straddle_short, ai_straddle_long),
        'grown': (ai_grown_short, ai_grown_long),
        'shrunk': (ai_shrunk_short, ai_shrunk_long)
    }
    return(dtai_loc_sl)


def _label_difference(
        ai_nuc_labels,
        ai_cell_labels,
    ):
    '''
    version: 2021-06-16
    used

    input:
        ai_nuc_labels: numpy array with nucleus cell labels.
        ai_cell_labels: numpy array with whole cell cell labels.

    output:
        ai_ring_rep: numpy array with cytoplasm cell labels.

    description:
        given matched nuclear and cell label IDs,
        return cell_labels minus nuc_labels.
    '''
    ab_overlap = ai_cell_labels == ai_nuc_labels
    ai_ring_rep = ai_cell_labels.copy()
    ai_ring_rep[ab_overlap] = 0
    return(ai_ring_rep)


def extract_features(
        s_slide,
        # specify input and output directory
        s_segdir = config.d_nconv['s_segdir'],  #'./Segmentation/',
        s_format_segdir_cellpose = config.d_nconv['s_format_segdir_cellpose'],  #'{}{}_CellposeSegmentation/',  # s_segdir, s_slide
        s_afsubdir =  config.d_nconv['s_afsubdir'],  #'./SubtractedRegisteredImages/',
        s_format_afsubdir = config.d_nconv['s_format_afsubdir'],  #'{}{}/',  # s_afsubdir, s_slide_pxscene
    ):
    '''
    version: 2021-06-16
    used

    input:
        s_slide: slide id to extract segmentaion feature from
        s_segdir: directory where segmentation basin, feature extraction, and xy cell position files can be found.
        s_format_segdir_cellpose: segmentation directory cellpose segmentation subridrectory.
        s_afsubdir: dictionary where to find af subtracted tiff images.
        s_format_afsubdir: subdirectory structure of s_afsubdir.

    output:
        whole slide all feature csv file.

    description:
        loads config.es_markerpartition_standard, the segmentation results, the input images, and the channels images.
        extract centroid, area, eccentricity, and mean intensity for nuclei and cytoplasm cell partition
        and mean intensity of the top 25% of pixel from the membrane cell partition,
        from each image.
    '''
    # fetch and process marker_partition standard
    es_marker_nuc = set()
    es_marker_nucmem = set()
    es_marker_cell = set()
    es_marker_cytomem = set()
    for s_markerpartition in config.es_markerpartition_standard:
        if s_markerpartition.endswith('_Nuclei'):
           es_marker_nuc.add(s_markerpartition.replace('_Nuclei',''))
        elif s_markerpartition.endswith('_Nucmem'):
           es_marker_nucmem.add(s_markerpartition.replace('_Nucmem',''))
        elif s_markerpartition.endswith('_Ring'):
           es_marker_cell.add(s_markerpartition.replace('_Ring',''))
        elif s_markerpartition.endswith('_Cytomem'):
           es_marker_cytomem.add(s_markerpartition.replace('_Cytomem',''))
        else:
           sys.exit('Error @ feat.extract_features: config.es_markerpartition_standard marker with non-standard cell partition detected {s_markerpartition}.\nstanadrd are _Nuclei, _Nucmem, _Ring, _Cytomem,')

    # generate empty output variable
    df_feat = pd.DataFrame()

    # each slide
    #for s_slide in ls_slide:
    s_path_seg = s_format_segdir_cellpose.format(s_segdir, s_slide)

    # each slide_pxscene
    for s_file in sorted(os.listdir(s_path_seg)):
        print(f'check: {s_file} ...')

        # find matched nucleus cell segmentation label file
        o_match = re.search(config.d_nconv['s_regex_tiff_celllabel_nuccellmatched'], s_file)
        if not (o_match is None):
            # extract slide_pxscene and nucles diameter
            #s_slide_pxscene = s_slide_fscene.replace('-Scene-', '_scene')  # BUE: caused by ulgle filename convention
            s_slide = o_match[config.d_nconv['di_regex_tiff_celllabel_nuccellmatched']['s_slide']]
            s_pxscene = o_match[config.d_nconv['di_regex_tiff_celllabel_nuccellmatched']['s_pxscene']]
            s_seg_markers = o_match[config.d_nconv['di_regex_tiff_celllabel_nuccellmatched']['s_seg_markers']]
            i_nuc_diam = int(o_match[config.d_nconv['di_regex_tiff_celllabel_nuccellmatched']['i_nuc_diam']])
            i_cell_diam = int(o_match[config.d_nconv['di_regex_tiff_celllabel_nuccellmatched']['i_cell_diam']])
            s_slide_pxscene = f'{s_slide}_{s_pxscene}'

            # load files
            print(f'processing: seg_markers {s_seg_markers}, min nuc_diam {i_nuc_diam}[px], min cell diam {i_cell_diam}[px], slide_pxscene {s_slide_pxscene}')
            ai_dapi = io.imread(s_path_seg + config.d_nconv['s_format_png_nucprojection'].format(s_slide_pxscene, i_nuc_diam))
            ai_nuc_labels = io.imread(s_path_seg + config.d_nconv['s_format_tiff_celllabel_nuc'].format(s_slide_pxscene, i_nuc_diam))
            ai_cell_labels = io.imread(s_path_seg + config.d_nconv['s_format_tiff_celllabel_nuccellmatched'].format(s_slide_pxscene, s_seg_markers, i_nuc_diam, i_cell_diam))

            # extract nuclear features
            df_feat_pxscene = _extract_feat(
                ai_labels = ai_nuc_labels,
                ai_intensity_image = ai_dapi,
                ls_properties = (['label']),
            )
            #df_feat_pxscene.columns = [f'{s_item}_segmented-nuclei' for s_item in df_feat_pxscene.columns]
            df_feat_pxscene.columns = ['cellid'] # bue: this is the label or jenny called it label_segmented-nuclei
            df_feat_pxscene.index = [f'{s_slide_pxscene}_cell{s_item}' for s_item in df_feat_pxscene.loc[:,'cellid']]
            df_feat_pxscene['slide'] = s_slide
            df_feat_pxscene['slide_scene'] = s_slide_pxscene

            # get standard subcellular regions
            ai_cyto_labels = _label_difference(ai_nuc_labels, ai_cell_labels)
            dtai_loc_nuc = _subcellular_regions(
                ai_labels = ai_nuc_labels,
                i_distance_short = 2, # this is the stanadard
                i_distance_long = 5, # this is the standard
            )
            dtai_loc_cell = _subcellular_regions(
                ai_labels = ai_cell_labels,
                i_distance_short = 2, # this is the stanadard
                i_distance_long = 5, # this is the standard
            )
            dai_loc_nuccell = {
                # nucleus
                'nuclei': ai_nuc_labels,  # or nuclei25
                'nucadj2': dtai_loc_nuc['straddle'][0],
                # nucleus membrane
                'nucmem': dtai_loc_nuc['membrane'][0], # or nucmem25
                # cytoplasm
                'perinuc5': dtai_loc_nuc['ring'][1],
                'cytoplasm': ai_cyto_labels,
                # cytoplasm membrane
                'cellmem': dtai_loc_cell['membrane'][0],  # or cellmem25
                'exp5': dtai_loc_nuc['grown'][1],  # or exp5nucmembrane25
                # cell
                'cell': ai_cell_labels,
                'celladj2': dtai_loc_cell['straddle'][0]
            }
            dai_loc_nuccellmem = {
                # nucleus
                'nuclei25': ai_nuc_labels,
                # nucleus membrane
                'nucmem25': dtai_loc_nuc['membrane'][0],
                # cytoplasm membrane
                'cellmem25': dtai_loc_cell['membrane'][0],
                'exp5nucmembrane25': dtai_loc_nuc['grown'][1],
            }

            # for each image file (one per slide_pxscene, round, channel)
            s_path_afsub = s_format_afsubdir.format(s_afsubdir, s_slide_pxscene)
            df_img_marker = basic.parse_tiff_reg(s_wd=s_path_afsub)
            #df_img_marker = df_img.loc[df_img.slide_scene == s_slide_pxscene, :]  # this are all markers
            for s_index in df_img_marker.index:
                s_marker = df_img_marker.loc[s_index,'marker']
                print(f'extract {s_marker} form: {s_index}')

                # loade file
                ai_intensity_image = io.imread(f'{df_img_marker.index.name}{s_index}')

                # dapi marker
                # bue: dapi marker are already labeld by round when parsing the filename

                # any marker
                for s_loc, ai_loc in sorted(dai_loc_nuccell.items()):
                    df_marker_loc = _extract_feat(
                        ai_labels = ai_loc,
                        ai_intensity_image = ai_intensity_image,
                        ls_properties = ['label', 'mean_intensity']
                    )
                    df_marker_loc.columns = [
                        f'{s_marker}_{s_loc}_label',
                        f'{s_marker}_{s_loc}',
                    ]
                    df_marker_loc.index = [f'{s_slide_pxscene}_cell{s_label_id}' for s_label_id in df_marker_loc.loc[:,f'{s_marker}_{s_loc}_label']]
                    df_feat_pxscene = pd.merge(df_feat_pxscene, df_marker_loc, left_index=True, right_index=True, how='left', suffixes=('',f'{s_marker}_{s_loc}'))

                # nucleus or cell marker
                if (s_marker in es_marker_nuc) or (s_marker in es_marker_cell) or (s_marker.startswith(config.d_nconv['s_marker_dapi'])):
                    for s_loc, ai_loc in sorted(dai_loc_nuccell.items()):
                        df_marker_loc = _extract_feat(
                            ai_labels = ai_loc,
                            ai_intensity_image = ai_intensity_image,
                            ls_properties = ['label', 'area', 'eccentricity']
                            #ls_properties = ['mean_intensity','centroid','area','eccentricity','label']
                        )
                        df_marker_loc.columns = [
                            'label',
                            f'{s_marker}_{s_loc}_area',
                            f'{s_marker}_{s_loc}_eccentricity',
                        ]
                        df_marker_loc.index = [f'{s_slide_pxscene}_cell{s_label_id}' for s_label_id in df_marker_loc.loc[:,'label']]
                        df_marker_loc.drop('label', axis=1, inplace=True)
                        df_feat_pxscene = pd.merge(df_feat_pxscene, df_marker_loc, left_index=True, right_index=True, how='left', suffixes=('',f'{s_marker}_{s_loc}'))

                # only nucleus marker
                if ((s_marker in es_marker_nuc) and not (s_marker in es_marker_cell)) or (s_marker.startswith(config.d_nconv['s_marker_dapi'])):
                    for s_loc, ai_loc in sorted(dai_loc_nuccell.items()):
                        df_marker_loc = _extract_feat(
                            ai_labels = ai_loc,
                            ai_intensity_image = ai_intensity_image,
                            ls_properties = ['label', 'centroid']
                            #ls_properties = ['mean_intensity','centroid','area','eccentricity','label']
                        )
                        df_marker_loc.columns = [
                            'label',
                            f'{s_marker}_{s_loc}_centroid-0',
                            f'{s_marker}_{s_loc}_centroid-1',
                        ]
                        df_marker_loc.index = [f'{s_slide_pxscene}_cell{s_label_id}' for s_label_id in df_marker_loc.loc[:,'label']]
                        df_marker_loc.drop('label', axis=1, inplace=True)
                        df_feat_pxscene = pd.merge(df_feat_pxscene, df_marker_loc, left_index=True, right_index=True, how='left', suffixes=('',f'{s_marker}_{s_loc}'))

                # only cell marker
                if (s_marker in es_marker_cell) and not (s_marker in es_marker_nuc):
                    for s_loc, ai_loc in sorted(dai_loc_nuccell.items()):
                        df_marker_loc = _extract_feat(
                            ai_labels = ai_loc,
                            ai_intensity_image = ai_intensity_image,
                            ls_properties = ['label','euler_number']
                            #ls_properties = ['mean_intensity', 'euler_number', 'area', 'eccentricity', 'label']
                        )
                        df_marker_loc.columns = [
                            'label',
                            f'{s_marker}_{s_loc}_euler',
                        ]
                        df_marker_loc.index = [f'{s_slide_pxscene}_cell{s_label_id}' for s_label_id in df_marker_loc.loc[:,'label']]
                        df_marker_loc.drop('label', axis=1, inplace=True)
                        df_feat_pxscene = pd.merge(df_feat_pxscene, df_marker_loc, left_index=True, right_index=True, how='left', suffixes=('',f'{s_marker}_{s_loc}'))

                # only membrane marker (which are always nucleus or cell marker too)
                if (s_marker in es_marker_nucmem) or (s_marker in es_marker_cytomem):
                    for s_loc, ai_loc in sorted(dai_loc_nuccellmem.items()):
                        df_prop = _extract_feat(
                            ai_labels = ai_loc,
                            ai_intensity_image = ai_intensity_image,
                            ls_properties = ['intensity_image','image','label']
                        )
                        df_marker_loc = pd.DataFrame(columns = [f'{s_marker}_{s_loc}'])
                        for s_idx in df_prop.index:
                            s_label_id = df_prop.loc[s_idx, 'label']
                            ai_intensity_image_small = df_prop.loc[s_idx, 'intensity_image']
                            ai_image = df_prop.loc[s_idx, 'image']
                            ai_pixels = ai_intensity_image_small[ai_image]
                            ai_pixels25 = ai_pixels[ai_pixels >= np.quantile(ai_pixels, .75)]
                            df_marker_loc.loc[s_label_id, f'{s_marker}_{s_loc}'] = ai_pixels25.mean()
                        df_marker_loc.index = [f'{s_slide_pxscene}_cell{s_label_id}' for s_label_id in df_marker_loc.index]
                        df_feat_pxscene = pd.merge(df_feat_pxscene, df_marker_loc, left_index=True, right_index=True, how='left', suffixes=('',f'{s_marker}_{s_loc}'))

            # update slide output by slide_pxscene output
            df_feat = df_feat.append(df_feat_pxscene)

    # write slide output to file
    df_feat.index.name = 'index'
    df_feat.to_csv(s_path_seg + config.d_nconv['s_format_csv_centroid_shape_meanintenisty'].format(s_slide))
    #break


###################################
#  combine nucleus and cell label #
###################################

def load_cellpose_features_df(
        es_slide,
        s_segdir = config.d_nconv['s_segdir'],  #'./Segmentation/',
        s_format_segdir_cellpose = config.d_nconv['s_format_segdir_cellpose'],  #'{}{}_CellposeSegmentation/',  # s_segdir, s_slide
    ):
    '''
    version: 2021-06-16

    input:
        es_slide:  list of slides from which cellpose segmented feature data should be loaded.
        s_segdir: directory where segmentation basin, feature extraction, and xy cell position files can be found.
        s_format_segdir_cellpose: segmentation directory cellpose segmentation subridrectory.

    output:
        df_mi: cellpose segmented feature dataframe.

    description:
        load all full feature dataframes in slide list.
    '''
    df_mi = pd.DataFrame()
    for s_slide in sorted(es_slide):
        print('Loading:', config.d_nconv['s_format_csv_centroid_shape_meanintenisty'].format(s_slide))
        df_mi_slide = pd.read_csv(s_format_segdir_cellpose.format(s_segdir, s_slide) + config.d_nconv['s_format_csv_centroid_shape_meanintenisty'].format(s_slide), index_col=0)
        df_mi = df_mi.append(df_mi_slide)
    # output
    return(df_mi)


#def _fill_cellpose_nas(
def _patch_nucleus_without_cytoplasm(
        df_mi,
        i_thresh_manual, # = 1000,
        s_thresh_marker = 'Ecad',
    ):
    '''
    version: 2021-07-07

    input:
        df_mi: cellpose segmented feature dataframe.
        i_thresh_manual: integer to specify s_thresh_marker threshold value.
        s_thresh_marker: string which specifies the marker to be used cytoplasm detetction.
            default is ecad, since segmentation is usualy run on ecad. adjust if necessary.

    output:
        df_mi: updated input dataframe.

    description:
        some nuclei don't have a cytoplasm, replace NA with perinuc5
    '''
    # since segmentation was run on ecad, use ecad threshold
    print(f'Finding {s_thresh_marker} negative cells ...') # {sorted(df_mi.columns[df_mi.columns.str.contains(s_thresh_marker)])}
    ls_neg_cells = df_mi.loc[(df_mi.loc[:,f'{s_thresh_marker}_cytoplasm'] < i_thresh_manual), :].index.tolist()
    df_mi[f'{s_thresh_marker}_negative'] = df_mi.index.isin(ls_neg_cells)

    # replace cells without cytoplasm (ecad) with perinuc 5
    print(f'For cells that are {s_thresh_marker} negative:')
    es_marker_perinuc5 = set(df_mi.columns[df_mi.columns.str.endswith('_perinuc5')])
    es_marker_cyto = set(s_markerpartition_standard.replace('_Ring','') for s_markerpartition_standard in config.es_markerpartition_standard if s_markerpartition_standard.endswith('_Ring'))
    for s_marker in sorted(es_marker_cyto):
        s_marker_perinuc5 = f'{s_marker}_perinuc5'
        s_marker_cytoplasm = f'{s_marker}_cytoplasm'
        print(f'Replace  {s_marker_cytoplasm} nas with {s_marker_perinuc5}')
        if s_marker_perinuc5 in es_marker_perinuc5:
            df_mi.loc[ls_neg_cells, s_marker_cytoplasm] = df_mi.loc[ls_neg_cells, s_marker_perinuc5]


# def combine_labels
def feature_correct_labels(
        s_slide,
        i_thresh_manual,  # 1000,
        s_thresh_marker = 'Ecad',
        # file system
        s_segdir = config.d_nconv['s_segdir'],  #'./Segmentation/',
        s_format_segdir_cellpose = config.d_nconv['s_format_segdir_cellpose'],  #'{}{}_CellposeSegmentation/',  # s_segdir, s_slide
        s_afsubdir = config.d_nconv['s_afsubdir'],  #'./SubtractedRegisteredImages/',
        s_format_afsubdir = config.d_nconv['s_format_afsubdir'],  #'{}{}/',  # s_afsubdir, s_slide_pxscene
    ):
    '''
    version: 2021-06-16

    input:
        s_slide:  slide id from which nucleus and cell segmentation labels tiffs should be combined.
        i_thresh_manual: integer to specify s_thresh_marker threshold value.
        s_thresh_marker: string which specifies the marker to be used cytoplasm detetction.
        s_segdir: directory where segmentation basin, feature extraction, and xy cell position files can be found.
        s_format_segdir_cellpose: segmentation directory cellpose segmentation subridrectory.
        s_afsubdir: dictionary where to find af subtracted tiff images.
        s_format_afsubdir: subdirectory structure of s_afsubdir.

    output:
        combined cell basins file, specified by s_format_tiff_celllabel_nuccellmatchedfeat.
        s_format_json_celltouch_segmentation json files to keep track of touching cells
        or cells with more then one nuleus!

    description:
        load cell labels; delete cells that were not used for cytoplasm (i.e. ecad neg).
        nuc labels, expand to perinuc 5 and then cut out the cell labels.
        save final celln_exp5_CellSegmentationBasins.tif basins file.
        keep track of cells that are completely coverd by another cell or more: counts as touching.
    '''

    # load mean intensity segmentation feature datatframe
    df_mi = load_cellpose_features_df(
        es_slide = {s_slide},
        s_segdir = s_segdir,
        s_format_segdir_cellpose = s_format_segdir_cellpose,
    )

    # get cells without cytoplasm
    # in this function only needed becaue {s_thresh}_negative column is needed.
    _patch_nucleus_without_cytoplasm(
        df_mi = df_mi,
        i_thresh_manual = i_thresh_manual,
        s_thresh_marker = s_thresh_marker,
    )

    # each slide_pxscene
    #for s_slide in ls_slide:
    ddls_touch = {}
    s_path_seg = s_format_segdir_cellpose.format(s_segdir, s_slide)

    # load fiels
    #for s_slide_pxscene in sorted(df_mi.loc[df_mi.slide==s_slide, 'slide_scene'].unique()):
    for s_file in sorted(os.listdir(s_path_seg)):
        print(f'check: {config.d_nconv["s_regex_tiff_celllabel_nuccellmatched"]} {s_file} ...')

        # find matched nucleus cell segmentation label file
        o_match = re.search(config.d_nconv['s_regex_tiff_celllabel_nuccellmatched'], s_file)
        if not (o_match is None):
            # extract slide_pxscene and nucles diameter
            # bue: actually position depends on the s_regex_tiff_celllabel_nuccellmatched regex
            # bue: clould be resolved with additional dict
            #s_slide_pxscene = s_slide_fscene.replace('-Scene-','_scene')  # BUE: caused by ulgle filename convention
            s_slide = o_match[1]
            s_pxscene = o_match[2]
            s_seg_markers = o_match[3]
            i_nuc_diam = int(o_match[4])
            i_cell_diam = int(o_match[5])
            s_slide_pxscene = f'{s_slide}_{s_pxscene}'
            s_slide_fscene = s_slide_pxscene

            # load files
            print(f'Processing combined segmentaiton labels for {s_slide_pxscene}')
            ai_label_nuc = io.imread(s_path_seg + config.d_nconv['s_format_tiff_celllabel_nuc'].format(s_slide_fscene, i_nuc_diam))
            ai_label_cell = io.imread(s_path_seg + config.d_nconv['s_format_tiff_celllabel_nuccellmatched'].format(s_slide_fscene, s_seg_markers, i_nuc_diam, i_cell_diam))

            # set non-ecad cell labels to zero
            ai_cell_zero = df_mi.loc[(df_mi.slide_scene == s_slide_pxscene) & df_mi.loc[:,f'{s_thresh_marker}_negative'],'cellid'].values
            ai_mask = np.isin(ai_label_cell, ai_cell_zero)
            ai_label_cell[ai_mask] = 0

            # expand nuclei for non-ecad cells
            # bue : _patch_nucleus_without_cytoplasm only takes care of the feature value not the segmentation mask.
            _, ai_label_nucexp = _expand_label(ai_label_nuc, i_distance=5) # bue: this default long distance!
            ai_label_nucexp[ai_label_cell > 0] = 0

            # combine calls and expanded nuclei
            ai_label_cellnucexp = ai_label_nucexp + ai_label_cell

            # save ai_label_cellnucexp to file at s_segdir not s_path_seg
            io.imsave(s_path_seg + config.d_nconv['s_format_tiff_celllabel_nuccellmatchedfeat'].format(s_slide_fscene, s_seg_markers, i_nuc_diam, i_cell_diam), ai_label_cellnucexp)

            # figure out the covered cells...labels + combined
            # some Jenny magic!
            ai_not_zero_pixels =  np.array([ai_label_nuc.ravel() !=0, ai_label_cellnucexp.ravel() !=0]).all(axis=0)
            ai_tups = np.array([ai_label_cellnucexp.ravel()[ai_not_zero_pixels], ai_label_nuc.ravel()[ai_not_zero_pixels]]).T # combined over nuclei
            ai_unique_rows = np.unique(ai_tups, axis=0)

            # generate cell touching dictionary
            dei_touch = {}
            for i_cell, i_touch in ai_unique_rows:
                if i_cell != i_touch:
                    if i_cell in dei_touch:
                        dei_touch[i_cell].add(i_touch)
                    else:
                        dei_touch[i_cell] = {i_touch}
            dls_touch = {}
            for i_cell, ei_touch in dei_touch.items():
                dls_touch.update({str(i_cell): [str(i_touch) for i_touch in sorted(ei_touch)]})
            ddls_touch.update({s_slide_pxscene: dls_touch})

        # save ddls_touch as json file at s_segdir not s_path_seg
        with open(s_segdir + config.d_nconv['s_format_json_celltouch_segmentation'].format(s_slide), 'w') as f:
            json.dump(ddls_touch, f)


###############################
#  filter and patch features #
################################

def filter_cellpose_xy(
        es_slide,
        ds_centroid = {
            'DAPI2_nuclei_centroid-0': 'DAPI_Y',
            'DAPI2_nuclei_centroid-1': 'DAPI_X',
            'DAPI2_nuclei_area':'nuclei_area',
            'DAPI2_nuclei_eccentricity':'nuclei_eccentricity',
        },
        s_segdir = config.d_nconv['s_segdir'],  #'./Segmentation/',
        s_format_segdir_cellpose = config.d_nconv['s_format_segdir_cellpose'],  #'{}{}_CellposeSegmentation/',  # s_segdir, s_slide
    ):
    '''
    version: 2021-06-16

    input:
        es_slide: set of sideids that should be processed
        ds_centroid: dictinonaty which defiend original nucleus segmentation centroid,
            area and eccentricity columns (value) and how they should be stanard named (key).
            the default dictionary is cellpose compatible.
        s_segdir: directory where segmentation basin, feature extraction, and xy cell position files can be found.
        s_format_segdir_cellpose: segmentation directory cellpose segmentation subridrectory.

    output:
        one features CentroidXY csv file per slide, saved at s_segdir.

    description:
        filter out nuclei centoids, area, and eccentricity from the
        mean intensity data frame file form a marker.
        default: use DAPI2.
    '''
    # handle input
    ls_coor = ['slide','slide_scene','cellid']  # feat.load_cellpose_features_df takes care of that
    ls_standard = sorted(ds_centroid.values())

    # process
    df_mi = load_cellpose_features_df(
        es_slide = es_slide,
        s_segdir=s_segdir,
        s_format_segdir_cellpose=s_format_segdir_cellpose
    )
    df_mi.rename(ds_centroid, axis=1, inplace=True)
    df_xy = df_mi.loc[:, ls_coor+ls_standard]
    for s_slide in sorted(es_slide):
        df_xy_slide = df_xy.loc[df_xy.slide == s_slide, :]
        print(f'filter_cellpose_xy {s_slide}: for quality control make sure centroids dont have too many NAs: {round(df_xy_slide.isna().sum().sum() / (df_xy_slide.shape[0] * df_xy_slide.shape[1]), 3)}[fraction]')
        df_xy_slide = df_xy_slide.dropna(axis=0, how='any')
        # output at s_segdir not s_path_seg
        df_xy_slide.to_csv(s_segdir + config.d_nconv['s_format_csv_controidxy'].format(s_slide))


#def fill_bright_nas(
def _patch_weak_membrane_marker(
        df_mi,
        s_thresh_marker = 'Ecad',
    ):
    '''
    version: 2021-06-16

    input:
        df_mi: data frame with segmentation feature mean intensity values,
            already processed with fill_celpose_na
            which introduces {s_thresh_marker}_negative column.
        s_thresh_marker: this specifies cells with cytoplasm (tumor cells).

    output:
        df_mi: updated df_mi dataframe,

    description:
        enhance nucmem and cytomem marker in dataframe by
        replaceing {s_marker}_cellmem25 non-tumor cells (no cytoplasm segmented) and
        tumor cells with nas for this marker with {s_marker}_exp5nucmembrane25.
    '''
    # fetch membrane markers
    es_marker_nucmem = set(s_markerpartition_standard.replace('_Nucmem','') for s_markerpartition_standard in config.es_markerpartition_standard if s_markerpartition_standard.endswith('_Nucmem'))
    es_marker_cytomem = set(s_markerpartition_standard.replace('_Cytomem','') for s_markerpartition_standard in config.es_markerpartition_standard if s_markerpartition_standard.endswith('_Cytomem'))

    # intersect with pannel markers
    es_marker_pannel = set([s_marker.split('_')[0] for s_marker in df_mi.columns])
    #es_marker_pannel.discard(f'{s_thresh_marker}_negative')
    es_marker_nucmem = es_marker_nucmem.intersection(es_marker_pannel)
    es_marker_cytomem = es_marker_cytomem.intersection(es_marker_pannel)
    print('nucleus membran marker found:', sorted(es_marker_nucmem))
    print('cytoplasm membranmarker found:', sorted(es_marker_cytomem))

    # get non-tumor cells
    es_neg = set(df_mi[(df_mi.loc[:,f'{s_thresh_marker}_negative']) & (df_mi.index.isin(df_mi.index))].index)

    # for each membrane marker enhance nan and non-tumor cells
    for s_marker in es_marker_nucmem:
        print(f'replace {s_marker}_nucmem25 in non-tumor cells and nas with {s_marker}_exp5nucmembrane25')
        es_na = set(df_mi.loc[df_mi.loc[:,f'{s_marker}_nucmem25'].isna(), :].index)  # nas cells
        ls_replace = sorted(es_neg.union(es_na))
        df_mi.loc[ls_neg, f'{s_marker}_nucmem25'] = df_mi.loc[ls_neg, f'{s_marker}_exp5nucmembrane25']  # non-tumor cells

    for s_marker in es_marker_cytomem:
        print(f'replace {s_marker}_cellmem25 in non-tumor cells and nas with {s_marker}_exp5nucmembrane25')
        es_na = set(df_mi.loc[df_mi.loc[:,f'{s_marker}_cellmem25'].isna(), :].index)  # nas cells
        ls_replace = sorted(es_neg.union(es_na))
        df_mi.loc[ls_replace, f'{s_marker}_cellmem25'] = df_mi.loc[ls_replace, f'{s_marker}_exp5nucmembrane25']  # non-tumor cells


# def shrunk_seg_regions(
def _patch_cytoplasm_bleedthrough(
        df_mi,
        es_shrunk_markerpartition,  # list of shrunken marker that should replace perinuc5
        s_thresh_marker = 'Ecad',  # this specifies tumor cells, the cells to be shrunken.
        es_slidepxscene_cellline = set(),  # celllines will be enforced as tumor and as such be shrunken.
    ):
    '''
    version: 2021-06-16

    input:
        df_mi: data frame with segmentation feature mean intensity values,
            already processed with fill_celpose_na
            which introduces f'{s_thresh_marker}_negative' column.
        es_shrunk_markerpatrition: set of shrunken marker partition that should
            for tumor cells (s_thresh_marker) replace corresponding perinuc5.
        s_thresh_marker: this specifies tumor cells, the cells to be shrunken.
        es_slidepxscene_cellline: celllines will be enforced as tumorcells {s_thresh_marker}
            and as such any marker defined in es_shrunk_markerpatrition will be shrunken.

    output:
        df_mi: updated input dataframe

    description:
        shrunks the perinuc5 segmentation region from tumor cells with the marker_partition specidied in es_shrunk_marker (e.g. CD44_perinuc2, Vim_perinuc2).
        the columns specified in es_shrunk_markerpartition have already to exist in df_mi.
        only helps bleed trough a little.
    '''
    # some basic cell typeing
    es_ecad_cell = set(df_mi.loc[~df_mi.loc[:,f'{s_thresh_marker}_negative'],:].index)
    es_celline_cell = set(df_mi.loc[df_mi.slide_scene.isin(es_slidepxscene_cellline),:].index)
    es_tumor_cell = es_ecad_cell.union(es_celline_cell)
    #es_stromal_cell = set(df_mi.loc[~df_mi.index.isin(es_tumor_cell),:].index)

    # relplace tumor cell CD44 and Vim with shrunken area (only helps bleed trough a little)
    print('For markers with stromal to tumor bleedthrough, use shrunken segmentation region:')
    for s_markerpartition in es_shrunk_markerpartition:
        print(f'replace {s_markerpartition.split("_")[0]}_perinuc5 in tumor cells with {s_markerpartition}')
        df_mi.loc[es_tumor_cell, f'{s_markerpartition.split("_")[0]}_perinuc5'] = df_mi.loc[es_tumor_cell, f'{s_markerpartition}']


#def filter_loc_cellpose(
def _filter_cellpartition(
        df_mi,
        es_cytoplasm_marker,  # have not to specify cell partition
        es_custom_markerpartition, # have to specify cell partition
        b_filter_na = True,
    ):
    '''
    version: 2021-06-16

    input:
        df_mi: data frame with segmentation feature mean intensity values,
            possibly though not necessary  processed with fill_celpose_na.
        es_cytoplasm_marker: set of strings to specify cytoplasm marker.
            pannel dependent, usually all cancer cell marker.
            the marker do not have to define the exact partition.
            IN ECAD positive cells.
        es_custom_markerpartition: set of strings to specify marker with specific patritions
            that should be kept, other then _Nuclei, _Ring or the specified cytoplasm markers.
            the marker have to define the exact original partition.
        b_filter_na: boolean to specify if any rows with a NA should be droped.
            default is True.

    output:
        df_filter: filtered and cell partition re-standartisized df_mi data frame .

    description:
        filter df_mi for standard cell partition (Nuclei and Ring) and
        cytoplasm (es_cytoplasm_marker) other (es_custom_markerpartition) cell partitions as specified.
        will original partition fetched rename to: nuclei, perinuc5, and cytoplasm.
        only es_custom_markerpartition will keep there original cell partition name.
    '''
    # const
    ls_coor = ['slide', 'slide_scene', 'cellid']

    # handle input
    es_cyto = set([s_marker.split('_')[0] for s_marker in es_cytoplasm_marker])
    es_custom = set([s_marker.split('_')[0] for s_marker in es_custom_markerpartition])

    # get all markers, exclude cellmebrane marker
    # bue: 25 is the only accepted standard and all cell membrane marker are somewhere else
    #ls_marker = df_mi.columns[(df_mi.dtypes == float) & ~df_mi.columns.str.contains('25') & ~df_mi.columns.str.contains('mean')]
    ls_marker = df_mi.columns[(df_mi.dtypes == float)]
    es_marker = set([s_marker.split('_')[0] for s_marker in ls_marker if not re.search(r'R\d+Qc\d+', s_marker)])
    print('df_mi markers:', sorted(es_marker))

    # filter for secific marker
    es_dapi = set([s_marker.split('_')[0] for s_marker in ls_marker if s_marker.startswith('DAPI')])
    es_nuc = set([s_marker.split('_')[0] for s_marker in config.es_markerpartition_standard if s_marker.endswith('_Nuclei')]).intersection(es_marker)  # bue: why is this not straight _nuclei?
    es_ring = (set([s_marker.split('_')[0] for s_marker in config.es_markerpartition_standard if s_marker.endswith('_Ring')]) - es_cyto).intersection(es_marker)  # bue: why os this not straigt _perinuc?
    es_left = es_marker - es_dapi - es_nuc - es_ring - es_cyto - es_custom
    print('Nuclear markers:', sorted(es_nuc))
    print('Ring markers:', sorted(es_ring))
    print('Cytoplasm markers:', sorted(es_cyto))
    print('Custom markers:', sorted(es_custom))
    print('Markers with DAPI, Nuclei, or Ring, or Cyto, or Custom not specified: take both nuclei and ring', sorted(es_left))

    # sanity check
    es_all = es_dapi | es_nuc | es_ring | es_left | es_cyto | es_custom
    es_missing = es_all.difference(es_marker)
    if len(es_missing) > 0:
        sys.exit(f'Error @ featfilter.filter_loc_cellpose : some markers mentioned in es_cyto_marker or es_custom_markerpartition are missing in df_mi. {es_missing}')

    # filter
    ls_nuc = [s_marker + '_nuclei' for s_marker in sorted(es_left | es_nuc | es_dapi)]
    ls_perinuc = [s_marker + '_perinuc5' for s_marker in sorted(es_left | es_ring)]   # bue: this should maybe not always be 5?
    ls_cyto = [s_marker + '_cytoplasm' for s_marker in sorted(es_cyto)]
    ls_all = ls_nuc + ls_perinuc + ls_cyto + sorted(es_custom_markerpartition)  # bue: custom stays with original partition label
    df_filter = df_mi.loc[:,ls_coor+ls_all]

    # filter na
    if b_filter_na:
        df_filter.dropna(axis=0, how='any', inplace=True)
        print(f'NAs row filtered: {df_mi.shape[0] - df_filter.shape[0]}')

    # output
    return(df_filter)


def drop_marker(
        df_mi, # mean intensity values
        es_marker_todrop,
    ):
    '''
    version: 2021-06-16

    input:
        df_mi: data frame with segemnted feature mean intensity value.
        es_marker_todrop: marker appearing after the last round.

    output:
        df_mi: updated input dataframe

    description:
        drop markers from a datafarme
    '''
    # kick all columns from a marker
    print(f'columns before drop: {df_mi.shape[1]}')
    for s_marker in es_marker_todrop:
        es_drop = set(df_mi.columns[df_mi.columns.str.contains(s_marker)])
        df_mi.drop(es_drop, axis=1, inplace=True)
    print(f'columns before drop: {df_mi.shape[1]}')


#def filter_dapi_cellpose(
def _filter_dapi_positive(
        df_mi,
        dfb_thresh,
        es_dapipartition_filter,
        s_segdir = config.d_nconv['s_segdir'],  #'./Segmentation/',
        #s_format_segdir_cellpose = '{}{}_CellposeSegmentation/',  # s_segdir, s_slide
        s_qcdir = config.d_nconv['s_qcdir'],  #'./QC/',
    ):
    '''
    version: 2021-06-16

    input:
        df_mi: marker mean intensity dataframe.
        dfb_thresh: boolean dataframe with on/off values for each cell marker_partition.
        es_dapipartition_filter: list of all DAPIn_nuclei (n is the round number) that shoulde be used as ok filer.
        s_segdir: directory where segmentation basin, feature extraction, and xy cell position files can be found.
        #s_format_segdir_cellpose: segmentation directory cellpose segmentation subridrectory.
        s_qcdir: qc directory.

    output:
        df_mi: write filtered df_mi dataframe to file under s_segdir, one file per slide.

    description:
         filter by cell positive for DAPI autotresholding, in round specified in ls_filter
    '''
    # get all dapi_nuclei columns
    es_dapinuclei = set(dfb_thresh.columns[dfb_thresh.columns.str.contains(config.d_nconv['s_marker_dapi']) & dfb_thresh.columns.str.endswith('_nuclei')].unique())
    print(f'feat._filter_dapi_positive processing es_dapinuclei: {sorted(es_dapinuclei)}')

    # handle plot data
    dfb_dapinuclei = dfb_thresh.loc[:, list(es_dapinuclei) + ['slide_scene']]
    df_scenes = dfb_dapinuclei.groupby('slide_scene').sum().T / dfb_dapinuclei.groupby('slide_scene').sum().max(axis=1)

    # order x axis
    df_scenes['order'] = [float(re.sub(r'[^\d.]','', s_index.replace(config.d_nconv['s_quenching'],'.5'))) for s_index in df_scenes.index]
    df_scenes.sort_values('order', inplace=True)
    df_scenes.drop('order', axis=1, inplace=True)
    df_scenes.index = [s_index.split('_')[0] for s_index in df_scenes.index]

    # plot
    fig,ax = plt.subplots(figsize=(10,5))
    df_scenes.plot(ax=ax, colormap='tab20', grid=True, title=f'tissue lost')
    ax.set_xticks(np.arange(0, (len(df_scenes.index)), 1))
    ax.set_xticklabels(list(df_scenes.index))
    ax.set_ylim(0.0, 1.1)
    ax.set_ylabel(f'{config.d_nconv["s_marker_dapi"]} positive cell fraction []')
    ax.set_xlabel('cyclic staining round []')
    ax.legend(loc = 3)
    plt.tight_layout()
    s_opath = s_qcdir + s_segdir.split('/')[-2] + '/'
    os.makedirs(s_opath, exist_ok = True)
    fig.savefig(s_opath + f'{".".join(sorted(dfb_thresh.slide.unique()))}_DAPI_rounds_lineplot.png', facecolor='white')

    # filter by first and last round dapi
    ls_dapipartition_filter = sorted(es_dapipartition_filter)
    es_index_dapifilter_ok = set(dfb_thresh.loc[dfb_thresh.loc[:, ls_dapipartition_filter].all(axis=1), :].index)
    # also filter by any dapi less than 1 in mean intensity if not proper thresholded before
    es_index_dapi_missing = set(df_mi.loc[(df_mi.loc[:, list(es_dapinuclei)] < 1).any(axis=1), :].index)
    # apply filter
    es_index_dapi = es_index_dapifilter_ok - es_index_dapi_missing
    df_mi_filter = df_mi.loc[df_mi.index.isin(es_index_dapi), :]
    print(f'number of cells before DAPI {ls_dapipartition_filter} filter: {df_mi.shape[0]}')
    print(f'filtering by {ls_dapipartition_filter}')
    print(f'number of cells after DAPI filter: {df_mi_filter.shape[0]}')

    # write  df_mi_filter to filer at s_segdir (not s_format_segdir)
    for s_slide in sorted(df_mi_filter.slide.unique()):
        s_filter_dapi = '_'.join([s_filter.split('_')[0] for s_filter in ls_dapipartition_filter])
        s_ofile = config.d_nconv['s_format_csv_shape_filteredmeanintenisty'].format(s_slide, s_filter_dapi)
        print(f'write file: {s_ofile}')
        df_mi_filter.loc[df_mi_filter.slide == s_slide].to_csv(s_segdir + s_ofile)


def _plot_thresh_result_dapiecad(
        es_slide,
        dfb_thresh,
        df_img_thresh,
        s_thresh_marker = 'Ecad',
        s_segdir = config.d_nconv['s_segdir'],  #'./Segmentation/',  # load centroidxy
        #s_format_segdir_cellpose = '{}{}_CellposeSegmentation/',  # s_segdir, s_slide
        s_qcdir = config.d_nconv['s_qcdir'],  #'./QC/',  # output
    ):
    '''
    version: 2021-06-16

    input:
        es_slide: set of slides.
        dfb_thresh: boolean dataframe with DAPI and s_thresh_marker_partition on/off values for each cell, e.g. gerated with auto_threshold.
        df_img_thresh: parsed filename and threshold data frame.
        s_thresh_marker: strong (tumor) cells cytoplasm marker used for positive negative tresholding..
        s_segdir: directory where segmentation basin, feature extraction, and xy cell position files can be found.
        #s_format_segdir_cellpose: segmentation directory cellpose segmentation subridrectory.
        s_qcdir: sting quality control directory where the result is stored.

    output:
        png plots in the s_qcdir directory.

    description:
        generate marker positive cell location in tissue plots for DAPI and Ecad,
        for tissue loss and tumor cell detection.
    '''
    # get all dapi_nuclei columns
    s_threshcyto = f'{s_thresh_marker}_cytoplasm'
    es_dapinuclei = set(dfb_thresh.columns[dfb_thresh.columns.str.contains(config.d_nconv['s_marker_dapi']) & dfb_thresh.columns.str.endswith('_nuclei')].unique())
    print(f'feat._plot_thresh_result_dapiecad processing: {sorted(es_dapinuclei)} {s_threshcyto}')

    # order dapi
    se_dapinuclei = pd.Series(list(es_dapinuclei), name='dapiround')
    print(se_dapinuclei)
    se_dapinuclei.index = [float(re.sub(r'[^\d.]','', s_dapiround.replace(config.d_nconv['s_quenching'],'.5'))) for s_dapiround in se_dapinuclei]
    se_dapinuclei.sort_index(inplace=True)
    ls_dapinuclei = list(se_dapinuclei.values)

    # plot
    thresh.markerpositive_scatterplots(
        df_img_thresh = df_img_thresh,
        dfb_thresh = dfb_thresh,
        #df_xy = df_xy,
        ls_marker_partition = ls_dapinuclei+[f'{s_thresh_marker}_cytoplasm'],
        es_slide_filter = es_slide,
        s_segdir = s_segdir,
        s_qcdir = s_qcdir,
    )


def filter_features(
        s_slide,
        es_dapipartition_filter, # {'DAPI1_nuclei','DAPI2_nuclei','DAPI16_nuclei'},
        es_marker_needed, #  {'DAPI16','Ecad'},
        i_thresh_manual, # 1000,
        s_thresh_marker = 'Ecad',
        es_cytoplasm_marker = set(), # {'Ecad'} all cancer marker
        es_custom_markerpartition = set(),  # optional
        es_shrunk_markerpartition = set(),  # optional against beedthroigh
        es_slidepxscene_cellline = set(),  # optional celllines will be treated like turmor cells
        b_filter_na = True,
        ds_centroid = {
            'DAPI2_nuclei_centroid-0': 'DAPI_Y',
            'DAPI2_nuclei_centroid-1': 'DAPI_X',
            'DAPI2_nuclei_area':'nuclei_area',
            'DAPI2_nuclei_eccentricity':'nuclei_eccentricity',
        },
        s_afsubdir = config.d_nconv['s_afsubdir'],  #'./SubtractedRegisteredImages/',
        s_segdir = config.d_nconv['s_segdir'],  #'./Segmentation/',
        s_format_segdir_cellpose = config.d_nconv['s_format_segdir_cellpose'],  #'{}{}_CellposeSegmentation/',  # s_segdir, s_slide
        s_qcdir = config.d_nconv['s_qcdir'],  #'./QC/',
    ):
    '''
    version: 2021-06-16

    input:
        s_slide:  slide id from which segmented feature mean intensity values and such should be extracted.
        es_dapipartition_filter: list of all DAPIn_nuclei (n is the round number) that shoulde be used as ok filer.
            user qc images to defined this! usually dapi2 - because dapi1 might be hazzy - and last good dapi,
            and additional bad rounds inbetween.
        es_marker_needed: marker that have to be in the final dataset. thus this round can not be dropped.
        i_thresh_manual: integer to specify s_thresh_marker threshold value.
        s_thresh_marker: string which specifies the marker to be used cytoplasm detetction.
            default is ecad, since segmentation is usualy run on ecad. adjust if necessary.
        es_cytoplasm_marker: set of strings to specify cytoplasm marker.
            pannel dependent. use sorted(basic.parse_tiff_reg('./'.marker.unique()))!
            usually choose all cancer cell marker.
            the marker do not have to define the exact partition.
        es_custom_markerpartition: set of strings to specify marker with specific patritions
            that should be kept, other then _Nuclei, _Ring or the specified cytoplasm markers.
            the marker have to define the exact original partition.
        es_shrunk_markerpatrition: set of shrunken marker partition that should
            for tumor cells (s_thresh_marker) replace corresponding perinuc5.
        es_slidepxscene_cellline: celllines will be enforced as tumorcells {s_thresh_marker}
            and as such any marker defined in es_shrunk_markerpatrition will be shrunken.
        b_filter_na: boolean to specify if any rows with a NA should be droped.
            default is True.
        ds_centroid: dictinonaty which defiend original nucleus segmentation centroid,
            area and eccentricity columns (value) and how they should be stanard named (key).
            the default dictionary is cellpose compatible.
        s_afsubdir: auto fluorescent subtracted registered image directory.
        s_segdir: directory where segmentation basin, feature extraction, and xy cell position files can be found.
        s_format_segdir_cellpose: segmentation directory cellpose segmentation subridrectory.
        s_qcdir: directory wher qc plots can be found.

    output:
        several csv files, tiff files, and plots.

    description:
        runs feature extraction with all patches and filters.
    '''
    # generate features_{s_slide}_CentroidXY.csv files
    filter_cellpose_xy(
        es_slide = {s_slide},
        ds_centroid = ds_centroid,
        s_segdir = s_segdir,
        s_format_segdir_cellpose = s_format_segdir_cellpose,
    )
    # load threshold and round parameter file
    df_img_thresh = thresh.load_thresh_df(
        es_slide = {s_slide},
        i_thresh_manual = i_thresh_manual,
        s_thresh_marker = 'Ecad',
        s_afsubdir = config.d_nconv['s_afsubdir'],  #'./SubtractedRegisteredImages/',
    )
    # load mean intensity segmentation feature datatframe
    df_mi = load_cellpose_features_df(
        es_slide = {s_slide},
        s_segdir = s_segdir,
        s_format_segdir_cellpose = s_format_segdir_cellpose,
    )
    # patch cells without cytoplasm
    #_fill_cellpose_nas(
    _patch_nucleus_without_cytoplasm(
        df_mi = df_mi,
        i_thresh_manual = i_thresh_manual,
        s_thresh_marker = s_thresh_marker,
    )
    # patch cellmembran marker with weak signal
    #_fill_bright_nas(
    _patch_weak_membrane_marker(
        df_mi = df_mi,
        s_thresh_marker = s_thresh_marker,
    )
    # patch bleed through by shrunk cancer cell marker like CD44 and Vim.
    #_shrunk_seg_regions(
    _patch_cytoplasm_bleedthrough(
        df_mi = df_mi,
        es_shrunk_markerpartition = es_shrunk_markerpartition,  # list of shrunken marker that should replace perinuc5
        s_thresh_marker = s_thresh_marker,  # this specifies tumor cells, the cells to be shrunken.
        es_slidepxscene_cellline = es_slidepxscene_cellline,  # celllines will be enforced as tumorcells and as such be shrunken.
    )
    # filter for nuclei and perinuc5 accoring to config.es_markerpartition_standard
    # and marker specified by es_cyto_marker and es_custom_markerpartition
    #filter_loc_cellpose(
    df_mi = _filter_cellpartition(
        df_mi = df_mi,
        es_cytoplasm_marker = es_cytoplasm_marker,  # have not to specify cell partition
        es_custom_markerpartition = es_custom_markerpartition, # have to specify cell partition
        b_filter_na = b_filter_na,
    )
    # drop last round
    r_last_round, es_marker_todrop = basic.find_last_round(
        df_img = df_img_thresh,  # this is actually the tresholdli file!
        es_marker_needed = es_marker_needed, # e.g. ('DAPI2_nuc','DAPI11_nuc','Ecad')  #
    )
    drop_marker(
        df_mi, # mean intensity values
        es_marker_todrop = es_marker_todrop,
    )
    # apply threshold
    #auto_threshold(
    dfb_thresh = thresh.apply_thresh(
        df_mi = df_mi,  # from load_cellpose_df
        df_img_thresh = df_img_thresh,  # from load_thresh_df
    )
    # filter dapi
    # generate qc line plot for tissue loss (defiend by dapi)
    # filter by cell positive for DAPI autotresholding, in round specified in es_dapipartition_filter
    #filter_dapi_cellpose(
    _filter_dapi_positive(
        df_mi = df_mi,
        dfb_thresh = dfb_thresh,
        es_dapipartition_filter = es_dapipartition_filter,
        s_qcdir = s_qcdir,
        s_segdir = s_segdir,
        #s_format_segdir_cellpose = s_format_segdir_cellpose,
    )
    # generate qc plot for tissue loss (dapi) and cancer cells (ecad)
    _plot_thresh_result_dapiecad(
        es_slide = {s_slide},
        dfb_thresh = dfb_thresh,
        df_img_thresh = df_img_thresh,
        s_thresh_marker = s_thresh_marker,
        s_segdir = config.d_nconv['s_segdir'],  #'./Segmentation/',  # load centroidxy
        #s_format_segdir_cellpose = '{}{}_CellposeSegmentation/',  # s_segdir, s_slide
        s_qcdir = s_qcdir,
    )


####################
# spawner function #
####################

def extract_features_spawn(
        es_slide,
        # processing
        b_parallel = True,
        s_type_processing = 'slurm',
        s_slurm_partition = 'exacloud',
        s_slurm_mem = '256G',
        s_slurm_time = '36:00:0',
        s_slurm_account = 'gray_lab',
        # specify input and output directory
        s_segdir = config.d_nconv['s_segdir'],
        s_format_segdir_cellpose = config.d_nconv['s_format_segdir_cellpose'],  # s_segdir, s_slide
        s_afsubdir = config.d_nconv['s_afsubdir'],
        s_format_afsubdir = config.d_nconv['s_format_afsubdir'],  # s_afsubdir, s_slide_pxscene
    ):
    '''
    verision: 2021-07-00

    input:
        es_slide: set of slide ids to process.

        # processing
        b_parallel: boolean to specify if slides shoudl be parallel processed.
            set to False if your hardware can't take it.
        s_type_processing: string to specify if pipeline is run on a slum cluster on not.
            knowen vocabulary is slurm and any other string.
        s_slurm_partition: slurm cluster partition to use.
            OHSU ACC options are 'exacloud', 'light', (and 'gpu').
            the default is tweaked to OHSU ACC settings.
        s_slurm_mem: slurm cluster memory allocation. format '64G'.
        s_slurm_time: slurm cluster time allocation in hour or day format.
            OHSU ACC max is '36:00:00' [hour] or '30-0' [day].
            the related qos code is tewaked to OHSU ACC settings.
        s_slurm_account: slurm cluster account to credit time from.
            OHSU ACC options are e.g. 'gray_lab', 'chin_lab'.

        # file system
        s_segdir:  segmentaion result directory.
        s_format_segdir_cellpose: cellpose segmentation result subdirectory.
        s_afsubdir: autofluorescence subtracted registered images directory.
        s_format_afsubdir: subfolder pattern in s_afsubdir. one subfolder per slide_pxscene.

    output:
        csv file for each slide with all extracted feature.

    description:
        spawn function to run the feat.extract_features function.
    '''
    for s_slide in sorted(es_slide):
        # this have to be a python template!
        print(f'extract_features_spawn: {s_slide}')

        # set run commands
        s_pathfile_template = 'template_extractfeatures_slide.py'
        s_pathfile = f'extractfeature_slide_{s_slide}.py'
        s_srun_cmd = f'python3 {s_pathfile}'
        ls_run_cmd = ['python3', s_pathfile]

        ## any ##
        # load template extract feature script code
        with open(f'{s_path_module}src/{s_pathfile_template}') as f:
            s_stream = f.read()

        # edit code generic. order matters!
        s_stream = s_stream.replace('peek_s_slide', s_slide)
        s_stream = s_stream.replace('peek_s_segdir', s_segdir)
        s_stream = s_stream.replace('peek_s_format_segdir_cellpose', s_format_segdir_cellpose)
        s_stream = s_stream.replace('peek_s_afsubdir', s_afsubdir)
        s_stream = s_stream.replace('peek_s_format_afsubdir', s_format_afsubdir)

        # write executable extract feature script code to file
        with open(s_pathfile, 'w') as f:
            f.write(s_stream)

        # execute extract feature script
        if b_parallel and (s_type_processing == 'slurm'):
            # generate sbatch file
            s_pathfile_sbatch = f'extractfeature_slide_{s_slide}.sbatch'
            config.slurmbatch(
                s_pathfile_sbatch = s_pathfile_sbatch,
                s_srun_cmd = s_srun_cmd,
                s_jobname = f'e{s_slide}',
                s_partition = s_slurm_partition,
                s_gpu = None,
                s_mem = s_slurm_mem,
                s_time = s_slurm_time,
                s_account = s_slurm_account,
            )
            # Jenny this is cool! Popen rocks.
            time.sleep(4)
            subprocess.run(
                ['sbatch', s_pathfile_sbatch],
                stdout = subprocess.PIPE,
                stderr = subprocess.STDOUT,
            )
        else:  # non-slurm
            # Jenny this is cool! Popen rocks.
            s_file_stdouterr = 'slurp-extractfeature_slide_{s_slide}.out'.replace('-','')
            time.sleep(4)
            o_process = subprocess.run(
                ls_run_cmd,
                stdout = open(s_file_stdouterr, 'w'),
                stderr = subprocess.STDOUT,
            )
            if not b_parallel:
                o_process.wait()


def filter_features_spawn(
        es_slide,
        es_dapipartition_filter,  # {'DAPI1_nuclei','DAPI2_nuclei','DAPI16_nuclei'},
        es_marker_needed,  #  {'DAPI16','Ecad'},
        i_thresh_manual,  # 1000,
        s_thresh_marker = 'Ecad',
        es_cytoplasm_marker = set(),  # {'Ecad'} cancer marker
        es_custom_markerpartition = set(),  # optional
        es_shrunk_markerpartition = set(),  # optional against beedthroigh
        es_slidepxscene_cellline = set(),  # optional celllines will be treated like turmor cells
        b_filter_na = True,
        ds_centroid = {
            'DAPI2_nuclei_centroid-0': 'DAPI_Y',
            'DAPI2_nuclei_centroid-1': 'DAPI_X',
            'DAPI2_nuclei_area':'nuclei_area',
            'DAPI2_nuclei_eccentricity':'nuclei_eccentricity',
        },
        # processing
        b_parallel = True,
        s_type_processing = 'slurm',
        s_slurm_partition = 'exacloud',
        s_slurm_mem = '128G',
        s_slurm_time = '36:00:0',
        s_slurm_account = 'gray_lab',
        # filter
        s_qcdir = config.d_nconv['s_qcdir'],
        s_segdir = config.d_nconv['s_segdir'],
        s_format_segdir_cellpose = config.d_nconv['s_format_segdir_cellpose'],  # s_segdir, s_slide
    ):
    '''
    verision: 2021-07-00

    input:
        es_slide: set of slide ids to process.
        es_dapipartition_filter: list of all DAPIn_nuclei (n is the round number) that shoulde be used as ok filer.
            user qc images to defined this! usually dapi2 - because dapi1 might be hazzy - and last good dapi,
            and additional bad rounds inbetween.
        es_marker_needed: marker that have to be in the final dataset. thus this round can not be dropped.
        i_thresh_manual: integer to specify s_thresh_marker threshold value.
        s_thresh_marker: string which specifies the marker to be used cytoplasm detetction.
            default is ecad, since segmentation is usualy run on ecad. adjust if necessary.
        es_cytoplasm_marker: set of strings to specify cytoplasm marker.
            pannel dependent. use sorted(basic.parse_tiff_reg('./'.marker.unique()))!
            usually choose all cancer cell marker.
            the marker do not have to define the exact partition.
        es_custom_markerpartition: set of strings to specify marker with specific patritions
            that should be kept, other then _Nuclei, _Ring or the specified cytoplasm markers.
            the marker have to define the exact original partition.
        es_shrunk_markerpatrition: set of shrunken marker partition that should
            for tumor cells (s_thresh_marker) replace corresponding perinuc5.
        es_slidepxscene_cellline: celllines will be enforced as tumorcells {s_thresh_marker}
            and as such any marker defined in es_shrunk_markerpatrition will be shrunken.
        b_filter_na: boolean to specify if any rows with a NA should be droped.
            default is True.
        ds_centroid: dictinonaty which defiend original nucleus segmentation centroid,
            area and eccentricity columns (value) and how they should be stanard named (key).
            the default dictionary is cellpose compatible.

        # processing
        b_parallel: boolean to specify if slides shoudl be parallel processed.
            set to False if your hardware can't take it.
        s_type_processing: string to specify if pipeline is run on a slum cluster on not.
            knowen vocabulary is slurm and any other string.
        s_slurm_partition: slurm cluster partition to use.
            OHSU ACC options are 'exacloud', 'light', (and 'gpu').
            the default is tweaked to OHSU ACC settings.
        s_slurm_mem: slurm cluster memory allocation. format '64G'.
        s_slurm_time: slurm cluster time allocation in hour or day format.
            OHSU ACC max is '36:00:00' [hour] or '30-0' [day].
            the related qos code is tewaked to OHSU ACC settings.
        s_slurm_account: slurm cluster account to credit time from.
            OHSU ACC options are e.g. 'gray_lab', 'chin_lab'.

        # file system
        s_qcdir: quality control result directory where segmentation basin,
             feature extraction, and xy cell position files can be found.
        s_segdir:  segmentaion result directory.
        s_format_segdir_cellpose: cellpose segmentation result subdirectory.

    output:
        csv file for each slide with all extracted feature.

    description:
        spawn function to run the feat.extract_features function.
    '''
    for s_slide in sorted(es_slide):
        # this have to be a python template!
        print(f'filter_features_spawn: {s_slide}')

        # set run commands
        s_pathfile_template = 'template_filterfeatures_slide.py'
        s_pathfile = f'filterfeature_slide_{s_slide}.py'
        s_srun_cmd = f'python3 {s_pathfile}'
        ls_run_cmd = ['python3', s_pathfile]

        ## any ##
        # load template fiter feature script code
        with open(f'{s_path_module}src/{s_pathfile_template}') as f:
            s_stream = f.read()

        # edit code generic
        s_stream = s_stream.replace('peek_s_slide', s_slide)
        s_stream = s_stream.replace('peek_es_dapipartition_filter', str(es_dapipartition_filter))
        s_stream = s_stream.replace('peek_es_marker_needed', str(es_marker_needed))
        s_stream = s_stream.replace('peek_i_thresh_manual', str(i_thresh_manual))
        s_stream = s_stream.replace('peek_s_thresh_marker', s_thresh_marker)
        s_stream = s_stream.replace('peek_es_cytoplasm_marker', str(es_cytoplasm_marker))
        s_stream = s_stream.replace('peek_es_custom_markerpartition', str(es_custom_markerpartition))
        s_stream = s_stream.replace('peek_es_shrunk_markerpartition', str(es_shrunk_markerpartition))
        s_stream = s_stream.replace('peek_es_slidepxscene_cellline', str(es_slidepxscene_cellline))
        s_stream = s_stream.replace('peek_b_filter_na', str(b_filter_na))
        s_stream = s_stream.replace('peek_ds_centroid', str(ds_centroid))
        s_stream = s_stream.replace('peek_s_qcdir', s_qcdir)
        s_stream = s_stream.replace('peek_s_segdir', s_segdir)
        s_stream = s_stream.replace('peek_s_format_segdir_cellpose', s_format_segdir_cellpose)

        # write executable filter feature script code to file
        with open(s_pathfile, 'w') as f:
            f.write(s_stream)

        # execute filter feature script
        if b_parallel and (s_type_processing == 'slurm'):
            # generate sbatch file
            s_pathfile_sbatch = f'filterfeature_slide_{s_slide}.sbatch'
            config.slurmbatch(
                s_pathfile_sbatch = s_pathfile_sbatch,
                s_srun_cmd = s_srun_cmd,
                s_jobname = f'f{s_slide}',
                s_partition = s_slurm_partition,
                s_gpu = None,
                s_mem = s_slurm_mem,
                s_time = s_slurm_time,
                s_account = s_slurm_account,
            )
            # Jenny this is cool! Popen rocks.
            time.sleep(4)
            subprocess.run(
                ['sbatch', s_pathfile_sbatch],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        else:  # non-slurm
            # Jenny this is cool! Popen rocks.
            s_file_stdouterr = 'slurp-filterfeature_slide_{s_slide}.out'.replace('-','')
            time.sleep(4)
            o_process = subprocess.run(
                ls_run_cmd,
                stdout=open(s_file_stdouterr, 'w'),
                stderr=subprocess.STDOUT,
            )
            if not b_parallel:
                 o_process.wait()


def feature_correct_labels_spawn(
        es_slide,
        i_thresh_manual,  # 1000,
        s_thresh_marker = 'Ecad',
        # processing
        b_parallel = True,
        s_type_processing = 'slurm',
        s_slurm_partition = 'exacloud',
        s_slurm_mem = '128G',
        s_slurm_time = '36:00:0',
        s_slurm_account = 'gray_lab',
        # file system
        s_segdir = config.d_nconv['s_segdir'],
        s_format_segdir_cellpose = config.d_nconv['s_format_segdir_cellpose'],  # s_segdir, s_slide
        s_afsubdir = config.d_nconv['s_afsubdir'],
        s_format_afsubdir = config.d_nconv['s_format_afsubdir'],  # s_afsubdir, s_slide_pxscene
    ):
    '''
    verision: 2021-07-00

    input:
        es_slide: set of slide ids to process.
        i_thresh_manual: integer to specify s_thresh_marker threshold value.
        s_thresh_marker: string which specifies the marker to be used cytoplasm detetction.

        # processing
        b_parallel: boolean to specify if slides shoudl be parallel processed.
            set to False if your hardware can't take it.
        s_type_processing: string to specify if pipeline is run on a slum cluster on not.
            knowen vocabulary is slurm and any other string.
        s_slurm_partition: slurm cluster partition to use.
            OHSU ACC options are 'exacloud', 'light', (and 'gpu').
            the default is tweaked to OHSU ACC settings.
        s_slurm_mem: slurm cluster memory allocation. format '64G'.
        s_slurm_time: slurm cluster time allocation in hour or day format.
            OHSU ACC max is '36:00:00' [hour] or '30-0' [day].
            the related qos code is tewaked to OHSU ACC settings.
        s_slurm_account: slurm cluster account to credit time from.
            OHSU ACC options are e.g. 'gray_lab', 'chin_lab'.

        # file system
        s_segdir:  segmentaion result directory.
        s_format_segdir_cellpose: cellpose segmentation result subdirectory.
        s_afsubdir: autofluorescence subtracted registered images directory.
        s_format_afsubdir: subfolder pattern in s_afsubdir. one subfolder per slide_pxscene.

    output:
        csv file for each slide with all extracted feature.

    description:
        spawn function to run the feat.extract_features function.
    '''
    for s_slide in sorted(es_slide):
        # this have to be a python template!
        print(f'feature_correct_labels_spawn: {s_slide}')

        # set run commands
        s_pathfile_template = 'template_featurecorrectlabels_slide.py'
        s_pathfile = f'featurecorrectlabels_slide_{s_slide}.py'
        s_srun_cmd = f'python3 {s_pathfile}'
        ls_run_cmd = ['python3', s_pathfile]

        ## any ##
        # load template fiter feature script code
        with open(f'{s_path_module}src/{s_pathfile_template}') as f:
            s_stream = f.read()

        # edit code generic. order matters!
        s_stream = s_stream.replace('peek_s_slide', s_slide)
        s_stream = s_stream.replace('peek_i_thresh_manual', str(i_thresh_manual))
        s_stream = s_stream.replace('peek_s_thresh_marker', s_thresh_marker)
        # filesystem
        s_stream = s_stream.replace('peek_s_segdir', s_segdir)
        s_stream = s_stream.replace('peek_s_format_segdir_cellpose', s_format_segdir_cellpose)
        s_stream = s_stream.replace('peek_s_afsubdir', s_afsubdir)
        s_stream = s_stream.replace('peek_s_format_afsubdir', s_format_afsubdir)

        # write executable feature correct labels script code to file
        with open(s_pathfile, 'w') as f:
            f.write(s_stream)

        # execute feature correct labels script
        if b_parallel and (s_type_processing == 'slurm'):
            # generate sbatch file
            s_pathfile_sbatch = f'featurecorrectlabels_slide_{s_slide}.sbatch'
            config.slurmbatch(
                s_pathfile_sbatch = s_pathfile_sbatch,
                s_srun_cmd = s_srun_cmd,
                s_jobname = f'l{s_slide}',
                s_partition = s_slurm_partition,
                s_gpu = None,
                s_mem = s_slurm_mem,
                s_time = s_slurm_time,
                s_account = s_slurm_account,
            )
            # Jenny this is cool! Popen rocks.
            time.sleep(4)
            subprocess.run(
                ['sbatch', s_pathfile_sbatch],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        else:  # non-slurm
            # Jenny this is cool! Popen rocks.
            s_file_stdouterr = 'slurp-featurecorrectlabels_slide_{s_slide}.out'.replace('-','')
            time.sleep(4)
            o_process = subprocess.run(
                ls_run_cmd,
                stdout=open(s_file_stdouterr, 'w'),
                stderr=subprocess.STDOUT,
            )
            if not b_parallel:
                o_process.wait()
