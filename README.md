# <center> Project
This is ... , it was created as a final project in **Bioinformatics Institute**.The main idea of this project is to predict a model of 3D spatial genome
organization having only DNA sequence. 

Contributors: 
- Ivan Kozlov (https://github.com/IvanKozlov98)
- Kirill Kirilenko (https://github.com/keyreallkeyrealenko)

## Description

There are a few approaches to analyze the spatial organization of chromatin in a cell,
these methods are called __Chromosome conformation capture__. The most used of them is Hi-C. The main disadvantages of a Hi-C experiment is cost and required time. 
Often researcher wants to know whether the regions of interest are connected or not without performing Hi-C. Our program creates a Hi-C matrix (as in a real Hi-C experiment) *in silico* based only on primary sequence of given DNA.

Our model shows good metrics for binary classification (regions interact or do not) and multiclass classification 
(how much regions interact). Now we are on the way to create a not overfitted regression model.

## Biology behind the ...

DNA sequence itself is full of information such as repeated DNA, genes, GC-content, distance between regions, etc. It is known that euchromatin
is localized in the nuclear interior and heterochromatin at the nuclear periphery (https://doi.org/10.1038/s41586-019-1275-3), the
same time heterochromatin is made up of repeated DNA mainly. Formation of topologically associating domains (TADs) depends on 
distance and sequence in DNA, genes with similar function which activity depends on the same enhancer more often locate 
(doi: 10.1016/j.molcel.2016.05.018) in the same TAD.
The thoughts written above as well as other _ab inition_ assumptions allowed as to create .. – 3D nuclear spatial predictor. 

