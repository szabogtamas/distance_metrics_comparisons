# distance_metrics_comparisons

A small comparison of different implementations to calculate Jaccard distances in
Python or R. Project is under development, not yet released.

## Usage

### Run it inside a Docker container (recommended)

To run Python script calculating Jaccard distances:
```
docker run -it -v $PWD:/home/rstudio/local_files \
  szabogtamas/distance_metrics_comparisons \
  python3 /usr/local/dev_scripts/similarity_r/calculate_jaccard.R \
  -i /home/rstudio/local_files/example_data/long_format_category_labels.csv \
  -o /home/rstudio/local_files/jaccard_matrix_of_example_run.csv
```

To run the analysis based on R:
```
docker run -it -v $PWD:/home/rstudio/local_files \
  szabogtamas/distance_metrics_comparisons \
  Rscript /usr/local/dev_scripts/similarity_r/calculate_jaccard.R \
  -i /home/rstudio/local_files/example_data/long_format_category_labels.csv \
  -o /home/rstudio/local_files/jaccard_matrix_of_example_run.csv
```

### Run it locally

Be sure to have all dependencies included in the Dockerfile installed locally.  
  
To run Python script calculating Jaccard distances:
```
python scripts/similarity_utils/calculate_jaccard.py \
  -i example_data/long_format_category_labels.csv \
  -o jaccard_matrix_of_example_run.csv
```

To run the analysis based on R:
```
Rscript scripts/similarity_r/calculate_jaccard.R \
  -i example_data/long_format_category_labels.csv \
  -o jaccard_matrix_of_example_run.csv
```