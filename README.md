# <center> NAP
This is **NAP** (**N**uclear **A**rchitecture **P**redictor) , it was created as a final project in **Bioinformatics Institute**.The main idea of this project is to predict a model of 3D spatial genome
organization having only DNA sequence. 

Contributors: 
- Ivan Kozlov (https://github.com/IvanKozlov98)
- Kirill Kirilenko (https://github.com/keyreallkeyrealenko)

**Note** NAP is not finished yet, in future it will work as a command line tool with a simple user interface. 

## Description

There are a few approaches to analyze the spatial organization of chromatin in a cell,
these methods are called __Chromosome conformation capture__. The most used of them is Hi-C. The main disadvantages of a Hi-C experiment is cost and required time. 
Often researcher wants to know whether the regions of interest interact or do not without performing Hi-C. Our program creates a Hi-C matrix (as in a real Hi-C experiment) *in silico* based only on primary sequence of given DNA.

Our model shows good metrics for binary classification (regions interact or do not) and multiclass classification 
(how much regions interact). Now we are on the way to create a not overfitted regression model. 

## Biology behind the ...

DNA sequence itself is full of information such as repeated DNA motifs, genes, GC-content, distance between regions, etc. It is known that euchromatin
is localized in the nuclear interior and heterochromatin at the nuclear periphery (https://doi.org/10.1038/s41586-019-1275-3), the
same time heterochromatin is made up of repeated DNA mainly. Formation of topologically associating domains (TADs) depends on 
distance and sequence in DNA, genes with similar function which activity depends on the same enhancer more often locate 
(doi: 10.1016/j.molcel.2016.05.018) in the same TAD.
The thoughts written above as well as other _ab inition_ assumptions allowed us to create NAP – 3D nuclear spatial predictor. 

## Requirements

The program was tested on MacOS, Ubuntu. The amount of RAM depends on resolution you want to simulate witn NAP. e.g. for 
Hi-C matrix at 50k resolution it perfectly works with 8 Gb RAM, but Hi-C matrix at 5k resolution requires much more RAM, with 5k 
resolution it was tested on a machine with 128 Gb RAM and 12 CPUs. But we recommend simulating your Hi-C matrix at 50k resolution. 
We showed NAP predicts better at 50k resolution (The resolution you choose in a python script we provide). 

The software requirements are provided with **env.yml** file. 

## Instruction

First, clone this repository:
1) ```git clone https://github.com/keyreallkeyrealenko/NAP.git```


## Problems 

To now, NAP can predict Hi-C matrix only for a single chromosome not for a whole chromatin. We know in a real nucleus all chromosomes are tangled.
In future versions NAP will predict 3D structure for the whole chromatin as well as for a single chromosome. 










