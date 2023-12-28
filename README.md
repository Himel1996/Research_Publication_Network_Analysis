# ADM HW5 The eternal significance of publications and citations!

This repository contains code and analysis for ADM Homework 5.

## Repository Structure

The repository contains the following key files and folders:

- `main.ipynb`: Jupyter notebook containing the code and analysis for the homework, including data collection, preprocessing, command line solutions and algorithmic question.
  
- `main.html`: HTML file for the main solution
  
- `GeneratedFiles`: Folder containing generated output from `main.ipynb`, including:
  - `df.csv`: Preprocessed top 10,000 papers' dataframe 
  - `citation_graph.graphml`: The citation graph
  - `collaboration_graph.graphml`: the collaboration graph
  
- `functions.py`: Python module containing the functions used in Q1 of main solution
  
- `functionality.py`: Python module containing the Backend Implementation functionalities of Q2 of main solution
  
- `controller.py`: Python module containing the Controller menu for Q2 of main solution
  
- `visualizer.py`: Python module containing the visualization functions for Q2 of main solution

- `CommandLine.sh`: Bash script containing solution for command line question
  
- `clq-output.png`: Output image for the CommandLine question




## Analysis Summary

The analysis focussed on the [dataset](https://www.kaggle.com/datasets/mathurinache/citation-network-dataset) from Kaggle. The following were done:
- Preprocessing the data and working on top 10,000 papers based on number of citations
- Creating Citation Graph with each paper being the node
- Creating Collaboration Graph with each author being the node
- Implementing Backend functionalities relating to both the graphs
- Implementing the Front-end and visualizations to understand the networks better

The repository contains all code and output to replicate the analysis described in the homework.

## Authors:

- Himel Ghosh
- Francesco Sbordone
- Riccardo Violano
- Selin Topaloglu
