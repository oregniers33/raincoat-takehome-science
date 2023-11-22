1. download ESACCI SSM dataset manually from https://climate.esa.int/en/projects/soil-moisture/data/
2. download_ERA_data.py to automatically download one full year of ERA5 SSM data
3. ERA_data_preprocessing.py to preprocess ERA5 data, more spefically, perform daily average and reset grid to match grid of ESACCO data
4. ERA_ESACCI_SM_merge.py to merge both datasets according to the approch proposed in https://www.nature.com/articles/s41597-023-01991-w
