#!/usr/bin/env python

import os, sys
import argparse
import cdsapi

def is_leapyr(n):
    if n%4==0:
        if n%100==0:
            if n%400==0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


def download_ERA_Land_data(year, outFolder):

    day_list_full = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']

    # build request dictionary
    for i in range(12):

        monthStr = f'{i+1:02d}'

        # output file
        outFilename = os.path.join(outFolder, 'ERA5_VSWL1_{}{}_025.grib'.format(monthStr,year))

        if i in [0, 2, 4, 6, 7, 9, 11]: # month with 31 days
            day_list = day_list_full

        elif i in [3, 5, 8, 10]: # month with 30 days
            day_list = day_list_full[:-1]

        elif i == 1 and is_leapyr(year): # february leap years
            day_list = day_list_full[:-2]

        elif i == 1 and not is_leapyr(year): # february not leap years
            day_list = day_list_full[:-3]

        req_dict = {
            'variable': 'volumetric_soil_water_layer_1',
            'year': '%s' % str(year),
            'month': '%s' % monthStr,
            'day': day_list,
            'grid': [0.25, 0.25],
            'time': [
                '00:00', '01:00', '02:00',
                '03:00', '04:00', '05:00',
                '06:00', '07:00', '08:00',
                '09:00', '10:00', '11:00',
                '12:00', '13:00', '14:00',
                '15:00', '16:00', '17:00',
                '18:00', '19:00', '20:00',
                '21:00', '22:00', '23:00',
            ],
            'format': 'grib',
        }

        # request cdsapi
        c = cdsapi.Client()
        c.retrieve('reanalysis-era5-land', req_dict, outFilename)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    required_arguments = parser.add_argument_group("Required arguments")
    required_arguments.add_argument(
        "--year",
        "-y",
        type=int,
        help="full year to be downloaded",
        required=True,
    )
    required_arguments.add_argument(
        "--outFolder",
        "-o",
        help="output folder",
        required=True,
    )
    args = parser.parse_args()

    download_ERA_Land_data(args.year, args.outFolder)
