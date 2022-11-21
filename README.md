# NAP
This is **NAP** (**N**uclear **A**rchitecture **P**redictor) , it was created as a final project in **Bioinformatics Institute**. 
The main idea of this project is to create a model that predict 3D spatial genome organization having only
DNA sequence. 

Don't worry, take a __NAP__...

Contributors: 
- Ivan Kozlov (https://github.com/IvanKozlov98)
- Kirill Kirilenko (https://github.com/keyreallkeyrealenko)

Superviser:
- Gennadiy Zakharov (https://github.com/GennadiyZakharov)

**Note** NAP is not finished yet, in future it will work as a command line tool with a simple user interface. 

## Goal and Objectives

The __Goal__ of this project is to determine whether DNA sequence itself can be a good predictor of the 3D nuclear organization.

The __Objectives__:
1) Come up with an approach to analyzing the 3D genome structure
2) Create a ML model to predict Hi-C matrix as reflection of 3D genome 

## Description

There are a few approaches to analyze the spatial organization of chromatin in a cell,
these methods are called __Chromosome conformation capture__. The most used of them is Hi-C. The main disadvantages of
a Hi-C experiment are cost and required time. Often researcher wants to know whether the regions of interest interact
or do not without performing Hi-C. Our program creates a Hi-C matrix (as in a real Hi-C experiment) *in silico* based
only on primary sequence of given DNA.

Our model shows good metrics for binary classification (regions interact or do not) and multiclass classification 
(how much regions interact). Now we are on the way to create a not overfitted regression model. 

The starting point of our project was [this](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8395981/) article and 
a corresponding program __Homology Segment Analysis__ (HSA). HSA allows to create a similarity matrix of different
segments (bins) of a genome. 

## Biology behind NAP

DNA sequence itself is full of information such as repetitive DNA (different type of TEs), genes, GC-content, distance
between regions, etc. It is known that euchromatin  is localized in the nuclear interior and heterochromatin at the nuclear
periphery (https://doi.org/10.1038/s41586-019-1275-3), the same time heterochromatin is made up of repetitive DNA mainly.
Formation of topologically associating domains (TADs) depends on distance and sequence in DNA, genes with similar function which activity depends on the same enhancer more often locate 
(doi: 10.1016/j.molcel.2016.05.018) in the same TAD. The thoughts written above as well as other _ab inition_ assumptions allowed us to create NAP – 3D nuclear spatial predictor. 

## Requirements

The program was tested on MacOS, Ubuntu. The amount of RAM depends on resolution and chromosome/genome fragment length 
you want to simulate with NAP. e.g. for Hi-C matrix at 50k resolution and chromosome 2R of _An. merus_ 
(approximately 65 Mb in length) it perfectly works with 8 Gb RAM, but Hi-C matrix at 5k resolution requires much more
RAM, with 5k resolution it was tested on a machine with 128 Gb RAM and 12 CPUs. But we recommend simulating 
your Hi-C matrix at 50k resolution. We showed NAP predicts better at 50k resolution 
(The resolution you choose in a python script we provide).

If you do not have annotated repeats in .bed format (such as ```data/Amer/Amer_repeat_annotation_total.bed```) and organism on
which you chose to run NAP is not well studied you have to run __RepeatModeler__ -> __RepeatMasker__. It requires powerful hardware 
(128 Gb RAM and 12 cores is enough). Read more about RepeatMasker and Augustus (https://www.repeatmasker.org/ and https://bioinf.uni-greifswald.de/augustus/)

The software requirements are provided with ```env.yml``` file. 

Also, you have to be familiar with HSA and has similarity matrix for a chromosome on which you chose to run NAP. 
The thorough description of HSA you may find [here](https://github.com/Beneor/homology-segment-analysis). 

## Workflow

The workflow depends on files you have. If you have only chromosome files without gene annotation and repetitive DNA
annotation first you must run RepeatModeler, RepeatMasker and Augustus separately. And the workflow will look like: 
(__Read before run: RepeatModeler will work for a week on a machine with medium hardware!__)

1) ```git clone https://github.com/keyreallkeyrealenko/NAP.git```

2) ```cd NAP/```

3) ```conda env create -f env.yml```

4) ```conda activate nap```

5-9 steps are to annotate TEs in a file.

5) ```BuildDatabase -name <db name> <file fasta>```

6) ```RepeatModeler -database <db name> -pa <number of cores> -LTRStruct >& run.out```

7) ```RepeatMasker -s -xsmall -a -gff -pa <number of cores> -u -lib  <repeat database> <chromosome_file.fasta>```

8) ```rmsk2bed <repeatmasker .out file> > <repeats.bed>```

9) ```cut -f 1,2,3,4 <repeats.bed> > <final_repeats.bed>```

10-11 steps to annotate genes, CDS, etc.

10) ```augustus --strand=both --species=<organism_type provided by augustus> <chromosome.fa> > <genes.fa>```

11) ```cut -f 1,3,4,5 <genes.fa> | awk '{print $1,$3,$4,$2}' > <final_genes.fa>```

Make sure repeats annotation is in the same format as file we provided (```data/Amer/Amer_repeat_annotation_total.bed```)
and genes annotation is the same as ```data/Amer/2R/2r_annotation_order.txt```.

Here you should have a similarity matrix received with HSA. 

12) ```python -m src.preprocessing -c <name_chromosome> -r <resolution> -rp <path_to_repeat_annotation> -chr <path_to_chromosome> -g <path_to_gene_annotation> -gm <path_to_gomology> -o <output dataset>```

13) ```python -m src.extract_target -c <name_chromosome> -r <resolution>  -hic <hic_data> -m <ML_task> -o <output target>```

14) ```python -m src.training -x <dataset file> -y <target file> -t <threads count> -m <ML_task> -o <output model>```

15) ```python -m src.predictor -d <test dataset> -model <model> -m <ML_task> -o <output prediction>```

## Example
Building binary classification model based on 2R chromosome with annotation files we provided:
1) ```python -m src.preprocessing -c 2R -r 50000 -rp data/Amer/Amer_repeat_annotation_total.bed -chr data/Amer/2R/2R_chr.fa -g data/Amer/2R/2r_annotation_order.txt -gm data/Amer/2R/ncounts_2R.tsv -o 2R_dataset.csv```

2) ```python -m src.extract_target -c 2R -r 50000 -hic https://genedev.bionet.nsc.ru/site/hic_out/by_Project/Anopheles/ActualData/hic/AmerR4_V4/AmerR4A_V4.1000.hic -m Binary -o 2R_target_50000.npy```

3) ```python -m src.training -x 2R_dataset.csv -y 2R_target_50000.npy -t 4 -m Binary -o 2R_model_50000_binary.bin```


Test this model on 3L chromosome:
1) ```python -m src.preprocessing -c 3L -r 50000 -rp data/Amer/Amer_repeat_annotation_total.bed -chr data/Amer/3L/3L_chr.fa -g data/Amer/3L/3l_annotation_order.txt -gm data/Amer/3L/ncounts_3L.tsv -o 3L_dataset.csv```

2) ```python -m src.extract_target -c 3L -r 50000 -hic https://genedev.bionet.nsc.ru/site/hic_out/by_Project/Anopheles/ActualData/hic/AmerR4_V4/AmerR4A_V4.1000.hic -m Binary -o 3L_target_50000.npy```

3) ```python -m src.predictor -d 3L_dataset.csv -model 2R_model_50000_binary.bin -m Binary -o 3L_prediction.npy```

## Conclusion

Here we devised a program __NAP__ that creates a Hi-C matrix of 2 different genome segments based only on DNA sequence and it's properties. NAP works as a ML-model, can work in three modes: 1) binary classification;
2) multiclass classification; and 3)regression. NAP shows good metrics for modes 1-2 (classification).  


## Problems 

To now, NAP can predict Hi-C matrix only for a single chromosome not for a whole chromatin. We know in a real nucleus all chromosomes are tangled.
In future versions NAP will predict 3D structure for the whole chromatin as well as for a single chromosome. The pipeline is not easy to reproduce,
we will simplify it. 

## References 

1) Falk, Martin, et al. "Heterochromatin drives compartmentalization of inverted and conventional nuclei." 
   Nature 570.7761 (2019): 395-399.
   
2) Dixon, Jesse R., David U. Gorkin, and Bing Ren. "Chromatin domains: the unit of chromosome organization." 
   Molecular cell 62.5 (2016): 668-680.
   
3) Zhuravlev, Aleksandr V., et al. "Chromatin Structure and “DNA Sequence View”: The Role of Satellite DNA in Ectopic
   Pairing of the Drosophila X Polytene Chromosome." International Journal of Molecular Sciences 22.16 (2021): 8713.









