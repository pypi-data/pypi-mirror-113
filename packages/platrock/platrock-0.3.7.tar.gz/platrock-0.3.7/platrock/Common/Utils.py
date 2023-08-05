"""
Copyright (c) 2019 François Kneib
Copyright (c) 2019 Franck Bourrier
Copyright (c) 2019 David Toe
Copyright (c) 2019 Frédéric Berger
Copyright (c) 2019 Stéphane Lambert

This file is part of PlatRock.

PlatRock is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3 of the License.

PlatRock is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar. If not, see <http://www.gnu.org/licenses/>.
"""
from osgeo import gdal
import functools,operator



def get_geojson_all_properties(filename,unique=True):
	result=[]
	shp_file=gdal.OpenEx(filename)
	for feat in shp_file.GetLayer(0):
		feat_dict=feat.ExportToJson(as_object=True) #loop on rocks start polygons
		result.append(list(feat_dict['properties'].keys()))
	if unique:
		result=functools.reduce(operator.iconcat, result, []) #flatten
		unique_result = list(set(result))
		return unique_result
	return result

def get_geojson_all_shapes(filename,unique=True):
	result=[]
	shp_file=gdal.OpenEx(filename)
	for feat in shp_file.GetLayer(0):
		feat_dict=feat.ExportToJson(as_object=True) #loop on rocks start polygons
		result.append(feat_dict['geometry']["type"])
	if unique:
		#result=functools.reduce(operator.iconcat, result, []) #flatten
		unique_result = list(set(result))
		return unique_result
	return result
