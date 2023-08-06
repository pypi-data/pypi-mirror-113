# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 10:48:31 2021

@author: jon-f
"""

import os
from datetime import date
import folium
import ee
import gammamap
import reducer
from downloadfunctions import *
from visualizefunctions import *

def auth():
    """
    Authenticates the user to Google Earth Engine and initializes the library.

    Args:
        None.

    Returns:
        None.

    """
    while True:
        try:
            response = int(input('Would you like to authenticate through browser (input "1") \
                                 or service account and private key (input "2")? '))
            if response == 1:
                ee.Authenticate()
                ee.Initialize()
            elif response == 2:
                try:
                    service_account = input("Enter your service account email: ")
                    json_file = ''
                    for file in os.listdir():
                        if file.endswith('.json'):
                            json_file = file
                            break
                    credentials = ee.ServiceAccountCredentials(service_account, json_file)
                    ee.Initialize(credentials=credentials)
                except:
                    print("The JSON private key file could not be found or was inconsistent \
                          with the service account. Please only one key in the current \
                              file directory.")
            break
        except:
            print("I didn't understand your response. Please input either 1 or 2.")

auth()

class Area():
    """
    This is the main class. Defined by the geoJSON inputed by the user, \
        it contains methods for displaying, operating on, and downloading
        ee.Images and ee.ImageCollections.

    Args:
        geoJSON (dict):  The geoJSON defining a singular geographical area. \
            See https://geojson.io/.

    """
    def __init__(self, geoJSON):
        self.geoJSON = geoJSON
        self.coords = self.geoJSON['features'][0]['geometry']['coordinates']
        self.aoi = ee.Geometry.Polygon(self.get_coords())

    def get_coords(self):
        """
        Gets the coordinates defined by the geoJSON.

        Args:
            None.

        Returns:
            self.coords (list): The coordinates defined by the geoJSON.

        """
        return self.coords

    def get_aoi(self):
        """
        Gets the AOI defined by the coordinates.

        Args:
            None.

        Returns:
            self.aoi (list): The AOI defined by the coordinates.

        """
        return self.aoi

    def apply_filters(self, collection='COPERNICUS/S1_GRD_FLOAT',
                      start_date=ee.Date(0),
                      end_date=ee.Date(date.today().isoformat()),
                      tRP1=None, tRP2=None, res=None, ins=None, earliest_first=False):
        """
        Applies filters to grab an image collecton.

        Args:
            collection (str): Which collection to grab images from
            start_date (ee.Date): Start date of filtering
            end_date (ee.Date): End date of filtering
            tRP1 (str): Band to filter for. Defaults to None for None for any bands
            tRP2 (str): Secondary band to filter for. Defaults for None for any bands
            res (str): L, M, or H. Resolution to filter for. Defaults to None (any resolution)
            ins (str): The instrumental mode to filter for. Defaults to None (any mode)
            earliest_first (bool): If set to True, the ee.ImageCollection returned \
                will be sorted s.t. the first ee.Image will be the captured the \
                    earliest. Defaults to False for latest image first.

        Returns:
            sort (ee.ImageCollection): An image collection with the area of geoJSON
            and the specified filters in the args applied.
        """
        if isinstance(start_date, (str, int)):
            start_date = ee.Date(start_date)
        if isinstance(end_date, (str, int)):
            end_date = ee.Date(end_date)

        aoi = self.get_aoi()

        img_set = ee.ImageCollection(collection).filterBounds(aoi).filterDate(start_date, end_date)

        if tRP1 is not None:
            img_set = img_set.filter(ee.Filter.listContains(
                'transmitterReceiverPolarisation', tRP1))
        if tRP2 is not None:
            img_set = img_set.filter(ee.Filter.listContains(
                'transmitterReceiverPolarisation', tRP2))

        if ins is not None:
            img_set = img_set.filter(ee.Filter.eq('instrumentMode', ins))
        if res is not None:
            img_set = img_set.filter(ee.Filter.eq('resolution', res))

        sort = img_set.sort('system:time_start', opt_ascending=earliest_first)
        return sort

    def one_per(self, time_range, collection='COPERNICUS/S1_GRD_FLOAT',
                      start_date=ee.Date(0),
                      end_date=ee.Date('2021-06-24'),
                      tRP1=None, tRP2=None, res=None, ins=None):
        """
        Applies filters to create a LIST with one ee.Image per time_range.

        Args:
            time_range (str): day, month, or year. Specifies the approximate \
                time range between photos.
            collection (str): Which collection to grab images from
            start_date (ee.Date): Start date of filtering
            end_date (ee.Date): End date of filtering
            tRP1 (str): Band to filter for. Defaults to None for None for any bands
            tRP2 (str): Secondary band to filter for. Defaults for None for any bands
            res (str): L, M, or H. Resolution to filter for. Defaults to None \
                for any resolution
            ins (str): The instrumental mode to filter for. Defaults to None \
                for any instrument mode

        Returns:
            img_set (ee.ImageCollection): An image collection with the area
            of geoJSON and the proper filters applied
        """
        def percent_missing(image):
            """
            Helper function that returns the % of the image data missing in the first band.

            Args:
                image (ee.Image): The image to calculate the % missing of

            Returns:
                percentMissing (float): The % missing of the image data compared \
                    to the self.get_aoi()
            """
            missing = ee.Number(image.mask().expression('1-b(0)').reduceRegion(
                ee.Reducer.sum(), self.get_aoi(), scale=100, maxPixels=10e8).get('constant'))
            totalArea = ee.Number(ee.Image(1).mask().reduceRegion(
                ee.Reducer.sum(), self.get_aoi(), scale=100, maxPixels=10e8).get('constant'))

            percent_missing = missing.divide(totalArea).getInfo()
            return percent_missing

        if isinstance(start_date, (str, int)):
            start_date = ee.Date(start_date)
        if isinstance(end_date, (str, int)):
            end_date = ee.Date(end_date)

        end_date_time = end_date

        current_start_time = start_date

        collected_imgs = []
        while ee.Algorithms.If(
                ee.Number.expression("x > 0", {
                    'x': end_date_time.difference(current_start_time, 'day')
                    }), 1, 0).getInfo():
            (current_start_time, current_end_time) = (ee.Date(current_start_time)
                                                      .getRange(time_range).getInfo()['dates'])
            img_col = self.apply_filters(collection=collection,
                              start_date=current_start_time,
                              end_date=current_end_time, tRP1=tRP1, tRP2=tRP2,
                              res=res, ins=ins, earliest_first=True)
            try:
                as_list = img_col.toList(img_col.size())
                best = ee.Image(as_list.get(0)).clip(self.get_aoi())
                pm_best = percent_missing(best)
                for i in range(as_list.length().getInfo()):
                    latest = ee.Image(as_list.get(i)).clip(self.get_aoi())
                    pm_latest = percentMissing(latest)
                    if pm_latest < 0.01:
                        best = latest
                        pm_best = pm_latest
                        break
                    elif pm_latest < pm_best:
                        best = latest
                        pm_best = pm_latest
                collected_imgs.append(best.clip(self.get_aoi()))
                print('Selected an image for {}'
                      .format(ee.Date(current_start_time).format('YYYY-MM-dd').getInfo()))

            except:
                print('There are no images in the',
                      time_range, "starting on",
                      ee.Date(current_start_time).format('YYYY-MM-dd').getInfo())
                print('The best image had {:.2f}% pixels of data missing. \
                      Try selecting a smaller area.'.format(pm_best*100))

            current_start_time = current_end_time

        return collected_imgs

    def latest_img(self, collection='COPERNICUS/S1_GRD_FLOAT'):
        """
        Grabs the latest image in the given collection.

        Args:
            collection (str): A collection name from GEE's public collections data. \
                Defaults to S1_GRD_FLOAT

        Returns:
            latest (ee.Image): The latest image for this area
        """

        img_col = self.apply_filters(collection=collection,
                                     end_date=ee.Date(date.today().strftime("%Y-%m-%d")))
        latest = img_col.first().clip(self.get_aoi())

        return latest

    def append_elevation_info(self, image):
        """
        Adds the elevation information to each image passed into it. \
            The image argument must be an ee.Image.

        Args:
            images (ee.Image): Image to add the elevation information.
            Since this is a class function, these are covering the same geographical area.

        Returns:
            multi (ee.Image): Image with added elevation as a new band
        """
        elv_collection = 'UMN/PGC/REMA/V1_1/8m'
        aoi = self.get_aoi()

        elevation = ee.Image(elv_collection).clip(aoi)
        multi = ee.Image([image, elevation])
        return multi

    def normalize_all_bands(self, image):
        """
        Noramlizes each of the bands in an image to range in values \
            between 0 and 1.

        Args:
            image (ee.Image): Image to normalize

        Returns:
            image_norm (ee.Image): A new image, with normalized float values
            dicts (list): A list of ee.Dictionary containing the min and max \
                of each band.
        """
        aoi = self.get_aoi()
        bands = image.bandNames().getInfo()
        img_bands = []
        dicts = []
        for band in bands:
            min_max_dict = image.select(band).reduceRegion(ee.Reducer.minMax(), aoi,
                                                crs='EPSG:3031', scale=1000)

            mini = ee.Number(min_max_dict.get('{}_min'.format(band)))
            maxi = ee.Number(min_max_dict.get('{}_max'.format(band)))

            img_bands.append(image.select(band).unitScale(mini.subtract(1), maxi.add(1)))
            dicts.append(min_max_dict)
        image_norm = ee.Image(img_bands)

        return image_norm, dicts

    def gammafilter(self, image):
        """
        Applies a gamma maximum filter to an image/images. As implemented as in
        Sentinel-1 SAR Backscatter Analysis Ready Data Preparation in Google Earth Engine

        Args:
            image (ee.Image or ee.ImageCollection): The image/images to be filtered for speckle

        Returns:
            filtered (ee.Image): The filtered image/images

        """
        if isinstance(image, ee.Image):
            filtered = gammamap.gammamap(image)
        elif isinstance(image, ee.ImageCollection):
            filtered = image.map(gammamap.gammamap)
        elif isinstance(image, list):
            filtered = list(map(self.gammafilter, image))
        return filtered

    def disp(self, image, rgb=False, band=0):
        """
        Displays an image in rgb/grayscale folium map fashion

        Args:
            image (ee.Image): The image to display
            rgb (bool): Whether or not to display in rgb corresponding to
            band (int): Selects which band to display if rgb is set to False. Defaults to 0

        Returns:
            None.
        """
        location = self.get_aoi().centroid().coordinates().getInfo()[::-1]
        # folium doesn't support crs other than crs 4326
        fmap = folium.Map(location=location, zoom_start=12)
        bands = image.bandNames().getInfo()
        if rgb:
            try:
                blue = image.select('elevation')
                blue.bandNames().getInfo()
            except:
                blue = image.select(bands[0]).divide(image.select(bands[1]))

            rgb = ee.Image.rgb(image.select(bands[0]),
                               image.select(bands[1]), blue)
            fmap.add_ee_layer(rgb, {'min': [0, 0, 0], 'max': [1, 1, 200]}, name='Image')
            fmap.add_child(folium.LayerControl())
            display(fmap)

        else:
            fmap.add_ee_layer(image.select(bands[band]), {'min': 0, 'max': 1}, name='Image')
            fmap.add_child(folium.LayerControl())
            display(fmap)

    def download(self, image, directory, scale=50, add_elevation=True):
        """
        Downloads either an image or an image collection to a directory.
        (note: I couldn't get geemap to download singular images, but
        I also couldn't get Google EE to download multiple images. In the end,
        I decided to download singular images to the local directory, but
        python lists of images or ee.ImageCollection will be saved to
        the glaciers_ee bucket in Google Cloud Platform)

        Args:
            images (ee.Image or ee.ImageCollection or list): image/images to download
            directory (str): name of relative directory to save images to,
            leave as a blank string you'd like to save in current directory
            scale (float): The scale to download at in meters/pixel. By default
            set to 50 meters per pixel

        Returns:
            None.
        """
        if isinstance(image, ee.Image):
            try:
                image_segmented = reducer.reduce(reducer.primer(self.get_coords()))
                bands = image.bandNames().getInfo()

                for geometry in image_segmented:
                    geo_obj = Area(reducer.geoJSONer(geometry))
                    geo_img = ee.Image(image.get('system:id').getInfo())
                    if add_elevation:
                        geo_img_elv = geo_obj.append_elevation_info(geo_img)
                        download = ee.Image([geo_img_elv.select(bands[0]),
                                             geo_img_elv.select(bands[1]),
                                             geo_img_elv.select('elevation')]
                                            ).clip(geo_obj.get_aoi())
                    else:
                        download = ee.Image([geo_img.select(bands[0]),
                                           geo_img.select(bands[1])]).clip(geo_obj.get_aoi())

                    DLimg(download, directory=directory, scale=scale, aoi=geo_obj.get_aoi())
                merger(directory)
            except:
                print('When the images are finished uploading, they will be avaiable at:')
                print('https://console.cloud.google.com/storage/browser/glaciers_ee')
                batchExport([image], directory=directory, scale=scale)

        elif isinstance(image, list):
            print('When the images are finished uploading, they will be avaiable at:')
            print('https://console.cloud.google.com/storage/browser/glaciers_ee')
            batchExport(image, directory=directory, scale=scale)

        elif isinstance(image, ee.ImageCollection):
            print('When the images are finished uploading, they will be avaiable at:')
            print('https://console.cloud.google.com/storage/browser/glaciers_ee')
            aslist = eeICtolist(image)
            batchExport(aslist, directory=directory, scale=scale)

    def hist(self, image, band=0):
        """
        Creates the values for an intensity histogram of an image.

        Args:
            image (ee.Image): The image to calculate the histogram for
            band (int): The band to calculate the pixel intensities for

        Returns:
            hist (list): The histogram created
        """
        aoi = self.get_aoi()
        bands = image.bandNames()

        band_max = image.select(band).reduceRegion(ee.Reducer.max(),
                                                   aoi, crs='EPSG:3031', scale=100)
        maxi = ee.Number(band_max.get(bands.get(band))).getInfo()
        if maxi >= 2:
            print("Warning: the image may not haven been properly normalized.",
                  "The image should be renormalized before creating a histogram")

        hist = image.select(band).reduceRegion(ee.Reducer.fixedHistogram(0, 1, 500),
                                               aoi).get(bands.get(band)).getInfo()

        return hist

    def get_stats(self, image, band=0):
        """
        Grabs common statistics about and image's specified band including mean, variance, and skew.

        Args:
            image (ee.Image): The image to grab stats about
            band (int): The band to make calculations about of the image

        Return:
            stats (dict): A dictionary containing statistics about the image band.
        """
        bands = image.bandNames().getInfo()

        stats = {}
        stats['mean'] = image.select(bands[band]).reduceRegion(ee.Reducer.mean(),
                          self.get_aoi()).get(bands[band]).getInfo()
        stats['variance'] = image.select(bands[band]).reduceRegion(ee.Reducer.variance(),
                          self.get_aoi()).get(bands[band]).getInfo()
        stats['skew'] = image.select(bands[band]).reduceRegion(ee.Reducer.skew(),
                          self.get_aoi()).get(bands[band]).getInfo()
        return stats
