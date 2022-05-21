# <center> NAP
This is **NAP** (**N**uclear **A**rchitecture **P**redictor) , it was created as a final project in **Bioinformatics Institute**.The main idea of this project is to predict a model of 3D spatial genome
organization having only DNA sequence. 

Contributors: 
- Ivan Kozlov (https://github.com/IvanKozlov98)
- Kirill Kirilenko (https://github.com/keyreallkeyrealenko)

**Note** NAP is not finished yet, in future it will work as a command line tool with a simple user interface. 

## Description

There are a few approaches to analyze the spatial organization of chromatin in a cell,
these methods are called __Chromosome conformation capture__. The most used of them is Hi-C. The main disadvantages of a Hi-C experiment are cost and required time. 
Often researcher wants to know whether the regions of interest interact or do not without performing Hi-C. Our program creates a Hi-C matrix (as in a real Hi-C experiment) *in silico* based only on primary sequence of given DNA.

Our model shows good metrics for binary classification (regions interact or do not) and multiclass classification 
(how much regions interact). Now we are on the way to create a not overfitted regression model. 

## Biology behind NAP

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

## Workflow


First, clone this repository:
1) ```git clone https://github.com/keyreallkeyrealenko/NAP.git```

2) ```cd NAP/```

3) ```conda env create -f env.yml```

4) ```conda activate nap```

5) ```pip install -r requirements.txt```

4) ```python -m src.preprocessing -c <name_chromosome> -r <resolution> -rp <path_to_repeat_annotation> -chr <path_to_chromosome> -g <path_to_gene_annotation> -gm <path_to_gomology> -o <output dataset>```

5) ```python -m src.extract_target -c <name_chromosome> -r <resolution>  -hic <hic_data> -m <ML_task> -o <output target>```

6) ```python -m src.training -x <dataset file> -y <target file> -t <threads count> -m <ML_task> -o <output model>```

7) ```python -m src.predictor -d <test dataset> -model <model> -m <ML_task> -o <output prediction>```

## Example
Building binary classification model based on 2R chromosome:
1) ```python -m src.preprocessing -c 2R -r 50000 -rp data/Amer/Amer_repeat_annotation_total.bed -chr data/Amer/2R/2R_chr.fa -g data/Amer/2R/2r_annotation_order.txt -gm data/Amer/2R/ncounts_2R.tsv -o 2R_dataset.csv```

2) ```python -m src.extract_target -c 2R -r 50000 -hic https://genedev.bionet.nsc.ru/site/hic_out/by_Project/Anopheles/ActualData/hic/AmerR4_V4/AmerR4A_V4.1000.hic -m Binary -o 2R_target_50000.npy```

3) ```python -m src.training -x 2R_dataset.csv -y 2R_target_50000.npy -t 4 -m Binary -o 2R_model_50000_binary.bin```


Test this model on 3L chromosome:
1) ```python -m src.preprocessing -c 3L -r 50000 -rp data/Amer/Amer_repeat_annotation_total.bed -chr data/Amer/3L/3L_chr.fa -g data/Amer/3L/3l_annotation_order.txt -gm data/Amer/3L/ncounts_3L.tsv -o 3L_dataset.csv```

2) ```python -m src.extract_target -c 3L -r 50000 -hic https://genedev.bionet.nsc.ru/site/hic_out/by_Project/Anopheles/ActualData/hic/AmerR4_V4/AmerR4A_V4.1000.hic -m Binary -o 3L_target_50000.npy```

3) ```python -m src.predictor -d 3L_dataset.csv -model 3L_model_50000_binary.bin -m Binary -o 3L_prediction.npy```


## Problems 

To now, NAP can predict Hi-C matrix only for a single chromosome not for a whole chromatin. We know in a real nucleus all chromosomes are tangled.
In future versions NAP will predict 3D structure for the whole chromatin as well as for a single chromosome. 










