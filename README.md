# HarborSeal-ID
This repository houses the scripts used to create the harbor seal GTseq assay which eventually uses the GTscore pipeline created by Garrett McKinney.
(found at https://github.com/gjmckinney/GTscore)

This repository includes:

  1. scripts to select SNPs from local scat sample RADseq data (Guillford 2020) and a global/pacific RADseq dataset (pulled from Liu et al. 2022)
  
  2. scripts to pull seqs for primer design with batchprimer3
  
  3. scripts to further select primers to order

  4. the optimization rounds and subsequent scripts to remove primers that interacted or didn't work

  5. scripts to run the GTseq and GTscore pipelines locally and to analyze the output of the GTscore pipeline for analyzing harbor seal genotypes with the GTseq assay

*this repo does not have scripts updated to work in the updated directory structure*