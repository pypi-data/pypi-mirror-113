# coding: utf-8

# In general Geoformat is licensed under an MIT/X style license with the
# following terms:
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

# Authors :
#   Guilhain Averlant
#   Eliette Catelin
#   Quentin Lecuire
#   Charlotte Montesinos Chevalley
#   Coralie Rabiniaux

import sys

# GEOFORMAT conf variables
from geoformat_lib.conf.driver_variable import (
    OGR_FORMAT_CSV,
    OGR_FORMAT_KML,
    OGR_FORMAT_POSTGRESQL,
    OGR_FORMAT_GEOJSON,
    OGR_FORMAT_XLSX,
    OGR_FORMAT_ESRI_SHAPEFILE,
    OGR_DRIVER_NAMES)

from geoformat_lib.conf.geometry_variable import GEOMETRY_TYPE, GEOMETRY_CODE_TO_GEOMETRY_TYPE, GEOFORMAT_GEOMETRY_TYPE

# predicates
from geoformat_lib.geoprocessing.connectors.predicates import (
    point_intersects_point,
    point_intersects_segment,
    point_intersects_bbox,
    segment_intersects_bbox,
    segment_intersects_segment,
    bbox_intersects_bbox,
    point_position_segment,
    ccw_or_cw_segments
)

# operations
from geoformat_lib.geoprocessing.connectors.operations import (
    coordinates_to_point,
    coordinates_to_segment,
    coordinates_to_bbox,
    segment_to_bbox
)

# Geoprocessing

# measure
# distance
from geoformat_lib.geoprocessing.measure.distance import (
    euclidean_distance,
    manhattan_distance,
    point_vs_segment_distance,
    euclidean_distance_point_vs_segment
)
# length
from geoformat_lib.geoprocessing.measure.length import segment_length
from geoformat_lib.geoprocessing.length import geometry_length

# area
from geoformat_lib.geoprocessing.measure.area import shoelace_formula
from geoformat_lib.geoprocessing.area import geometry_area

# matrix
from geoformat_lib.geoprocessing.matrix.adjacency import (
    create_adjacency_matrix,
    get_neighbor_i_feat,
    get_area_intersecting_neighbors_i_feat
)

# line merge
from geoformat_lib.geoprocessing.line_merge import line_merge

# merge geometries
from geoformat_lib.geoprocessing.merge_geometries import merge_geometries

# point_on_linestring
from geoformat_lib.geoprocessing.point_on_linestring import (
    point_at_a_distance_on_segment,
    points_on_linestring_distance
)

# split
from geoformat_lib.geoprocessing.split import (
    segment_split_by_point,
    linestring_split_by_point
)

# union
from geoformat_lib.geoprocessing.union import (
    union_by_split
)

# geoparameters -> lines
from geoformat_lib.geoprocessing.geoparameters.lines import (
    line_parameters,
    perpendicular_line_parameters_at_point,
    point_at_distance_with_line_parameters,
    crossing_point_from_lines_parameters
)

# boundaries
from geoformat_lib.geoprocessing.geoparameters import boundaries

# geoparameters -> bbox
from geoformat_lib.geoprocessing.geoparameters.bbox import (
    bbox_union,
    extent_bbox,
    point_bbox_position
)

# bbox conversion
from geoformat_lib.conversion.bbox_conversion import (
    envelope_to_bbox,
    bbox_to_envelope,
    bbox_extent_to_2d_bbox_extent,
    bbox_to_polygon_coordinates
)

# bytes conversion
from geoformat_lib.conversion.bytes_conversion import (
    int_to_4_bytes_integer,
    float_to_double_8_bytes_array,
    coordinates_list_to_bytes,
    double_8_bytes_to_float,
    integer_4_bytes_to_int
)

# coordinates conversion
from geoformat_lib.conversion.coordinates_conversion import (
    format_coordinates,
    coordinates_to_2d_coordinates
)

# features conversion
from geoformat_lib.conversion.feature_conversion import (
    feature_serialize,
    feature_deserialize,
    features_geometry_ref_scan,
    features_fields_type_scan,
    feature_list_to_geolayer,
    feature_filter_geometry,
    feature_filter_attributes,
    feature_filter,
    features_filter
)

# fields conversion
from geoformat_lib.conversion.fields_conversion import (
    update_field_index,
    recast_field,
    drop_field
)

# geolayer conversion
from geoformat_lib.conversion.geolayer_conversion import (
    multi_geometry_to_single_geometry_geolayer,
    geolayer_to_2d_geolayer,
    create_geolayer_from_i_feat_list,
    reproject_geolayer
)

# geometry conversion
from geoformat_lib.conversion.geometry_conversion import (
    geometry_type_to_2d_geometry_type,
    geometry_to_2d_geometry,
    geometry_to_geometry_collection,
    multi_geometry_to_single_geometry,
    ogr_geometry_to_geometry,
    geometry_to_ogr_geometry,
    geometry_to_wkb,
    wkb_to_geometry,
    wkt_to_geometry,
    geometry_to_wkt,
    force_rhr,
    geometry_to_bbox,
    reproject_geometry
)

# metadata conversion
from geoformat_lib.conversion.metadata_conversion import (
    geometries_scan_to_geometries_metadata,
    fields_scan_to_fields_metadata,
    reorder_metadata_field_index_after_field_drop
)

# precision tolerance conversion
from geoformat_lib.conversion.precision_tolerance_conversion import (
    deduce_rounding_value_from_float,
    deduce_precision_from_round
)

# segment conversion
from geoformat_lib.conversion.segment_conversion import (
    segment_list_to_linestring
)

# database operation
from geoformat_lib.db.db_request import (
    sql,
    sql_select_to_geolayer
)

# geometry conversion
from geoformat_lib.conversion.geometry_conversion import (
    bbox_extent_to_2d_bbox_extent,
    geometry_type_to_2d_geometry_type,
    geometry_to_2d_geometry,
    geometry_to_geometry_collection
)

# data printing
from geoformat_lib.explore_data.print_data import (
    get_features_data_table_line,
    print_features_data_table,
    get_fields_metadata_table_line,
    print_metadata_field_table
)
# random geometries
from geoformat_lib.explore_data.random_geometry import (
    random_point,
    random_segment,
    random_bbox
)
# attributes index
from geoformat_lib.index.attributes.hash import (
    create_attribute_index
)

# grid index
from geoformat_lib.index.geometry.grid import (
    bbox_to_g_id,
    point_to_g_id,
    g_id_to_bbox,
    g_id_to_point,
    g_id_neighbor_in_grid_index,
    create_grid_index,
    grid_index_to_geolayer
)

# driver
from geoformat_lib.driver.ogr.ogr_driver import (
    ogr_layer_to_geolayer,
    ogr_layers_to_geocontainer,
    geolayer_to_ogr_layer,
    geocontainer_to_ogr_data_source
)

# clauses
from geoformat_lib.processing.data.clauses import (
    clause_group_by,
    clause_where,
    clause_where_combination,
    clause_order_by,
)

# processing data
from geoformat_lib.processing.data.field_statistics import field_statistics

# geoformat driver
from geoformat_lib.driver.geojson_driver import (
    geojson_to_geolayer,
    geolayer_to_geojson
)
from geoformat_lib.driver.postgresql_driver import geolayer_to_postgres

__version__ = 20210720


def version(version_value=__version__, verbose=True):
    version_dev = 'Alpha'
    if verbose:
        return '{version_dev} version {version_number}'.format(version_dev=version_dev, version_number=version_value)
    else:
        return version_value

