#!/usr/bin/env python

import os, sys
import argparse
import glob as gb
import pandas as pd
import xarray as xr
import rasterio as rio
import cfgrib


def ERA5_SM_data_preprocessing(inFolder, outFolder):

    # preprocessings will consist in :
    # - daily average of SM values
    # - reshape grid to match ESACCI_SM dataset
    # - write outputs in similar format than ESACCI_SM dataset

    # get files list
    list_grib_files = gb.glob(os.path.join(inFolder, '*.grib'))

    # loop on files and apply preprocessings
    for f in list_grib_files:
        DS = xr.open_dataset(f, engine="cfgrib")
        # daily average
        DS_daily = DS.resample(time='D').mean()
        # reset lon to -180 : 180 rather than 0 : 360 and shift from centered coordinates to top left corner ATTENTION probably not accurate
        DS_daily.coords['longitude'] = (DS_daily.coords['longitude'] + 180) % 360 - 179.875
        DS_daily.coords['latitude'] = DS_daily.coords['latitude'] - 0.125
        DS_daily = DS_daily.sortby(DS_daily.longitude)
        # crop to remove -90.5 coordinates
        DS_daily = DS_daily.where(DS_daily.latitude >= -90, drop=True)
        # save daily data as netCDF
        dates, datasets = zip(*DS_daily.resample(time='1D').mean('time').groupby('time'))
        filenames = [os.path.join(outFolder, 'ERA5_SM_' + pd.to_datetime(date).strftime('%Y%m%d') + '.nc') for date in dates]
        xr.save_mfdataset(datasets, filenames)
        # print (DS_daily)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    required_arguments = parser.add_argument_group("Required arguments")
    required_arguments.add_argument(
        "--inFolder",
        "-i",
        help="input folder where ERA data are stored (one file per month)",
        required=True,
    )
    required_arguments.add_argument(
        "--outFolder",
        "-o",
        help="output folder where preprocessed data will be stored",
        required=True,
    )
    args = parser.parse_args()

    ERA5_SM_data_preprocessing(args.inFolder, args.outFolder)
