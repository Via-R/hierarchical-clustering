
# Hierarchical clustering  
![Clustering example](example.png)  
  
## Description  
  
This labwork implements hierarchical clustering algorithm, targeted at grouping a set of points (in this case, 2D points, but the code supports any amount of dimensions) into specified amount of clusters. You can read more [here](https://en.wikipedia.org/wiki/Hierarchical_clustering).
This code generates a set of 888 linearly distributed points in the 1x1 square (or reads from file), and then groups them into the desired amount of clusters. Colors and types of points' markers are picked randomly from the manually specified list of [matplotlib](https://matplotlib.org/stable/index.html) supported types.
  
## How to run  
If needed, create virtualenv:  
  
    $ python3 -m venv venv $ source venv/bin/activate  
Run the labwork:  
  
    $ python3 main.py [desired amount of clusters]
Once you run the code, you will be prompted to choose the source for starting points - you can have the points randomly generated or loaded from `input.txt` file, where points are specified alongside with their affiliation levels. If you selected loading from file, you will also be asked to enter the affiliation level, which defines which points from file will be included into clustering process (all points that have affiliation level lower than the one you specify will be omitted during clustering). Once you're done with filling in the prompt info, clustering process will commence.
