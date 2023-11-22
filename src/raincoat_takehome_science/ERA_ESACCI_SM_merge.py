#!/usr/bin/env python

import os, sys
import argparse
import pandas as pd
import xarray as xr
import numpy as np



def ERA5_ESACCI_SM_merge(ERA5_inFolder, ESACCI_inFolder, outFolder):

    # open ERA5 SM daily files
    ERA5_ds = xr.open_mfdataset(f"{ERA5_inFolder}ERA5_SM_"+"*.nc", combine="nested", concat_dim=[pd.Index(np.arange(365), name="tmp_dim")])

    # open ESACCI SM daily files
    ESACCI_ds = xr.open_mfdataset(f"{ESACCI_inFolder}ESACCI-"+"*.nc", combine="nested", concat_dim="time")

    SM_ESACCI = ESACCI_ds.sm
    SM_ERA5 = ERA5_ds.swvl1

    # mask no data in ESACCI and mask ERA5 on same location
    SM_ESACCI_masked = SM_ESACCI.where(SM_ESACCI != -9999)
    SM_ERA5_masked = SM_ERA5.where(SM_ESACCI != -9999)

    # compute pixel-wise temporal mean and std
    SM_ESACCI_mean = SM_ESACCI_masked.mean(dim="time", skipna=True)
    SM_ESACCI_std = SM_ESACCI_masked.std(dim="time", skipna=True)
    SM_ERA5_mean = SM_ERA5_masked.mean(dim="tmp_dim", skipna=True)
    SM_ERA5_std = SM_ERA5_masked.std(dim="tmp_dim", skipna=True)

    # # adjust ERA5 SM data to fit ESACCI SM temporal distribution
    # # see https://www.nature.com/articles/s41597-023-01991-w
    # ERA5_adjusted = (SM_ESACCI_std.values / SM_ERA5_std.values) * SM_ERA5_masked.values + ((SM_ESACCI_mean.values - SM_ERA5_mean.values) * (SM_ESACCI_std.values / SM_ERA5_std.values))
    #
    # ERA5_adjusted.to_netcdf('/media/olivier/Data/tmp/test_ERA5_SM/RES/ERA5_adjusted.nc')
    #
    # # # replace missing values in ESA CCI SM with ERA5 adjusted values
    # ESACCI_SM_filled = ESACCI_ds['sm'].where(ESACCI_ds['sm'] == -9999, ERA5_adjusted)
    # # # ESACCI_SM_filled = np.where(ESACCI_SM_filled == np.nan, ERA5_ds['swvl1'].values, ESACCI_SM_filled) # fill desert and snow/ice with ERA5 data
    # # ESACCI_SM_filled_da = xr.DataArray(ESACCI_SM_filled, coords={'latitude': ESACCI_ds['lat'].values,'longitude': ESACCI_ds['lon'].values,'time': ESACCI_ds['time'].values}, dims=["time", "latitude", "longitude"])
    # ESACCI_SM_filled.to_netcdf('/media/olivier/Data/tmp/test_ERA5_SM/RES/ESACCI_SM_filled.nc')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    required_arguments = parser.add_argument_group("Required arguments")
    required_arguments.add_argument(
        "--ERA5_inFolder",
        "-ie",
        help="input folder where daily mean ERA data are stored (one file per day)",
        required=True,
    )
    required_arguments.add_argument(
        "--ESACCI_inFolder",
        "-ic",
        help="input folder where daily ESACCI data are stored (one file per day)",
        required=True,
    )
    required_arguments.add_argument(
        "--outFolder",
        "-o",
        help="output folder where merged data will be stored",
        required=True,
    )
    args = parser.parse_args()

    ERA5_ESACCI_SM_merge(args.ERA5_inFolder, args.ESACCI_inFolder, args.outFolder)
