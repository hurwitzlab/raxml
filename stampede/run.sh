#!/bin/bash

#SBATCH -J raxml
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -p normal
#SBATCH -t 24:00:00
#SBATCH -A iPlant-Collabs

module load tacc-singularity

IMG=/work/05066/imicrobe/singularity/raxml-8.2.12.img

set -u

singularity exec $IMG run_raxml.py "$@" # -o raxml-out

echo "Done."
echo "Comments to Ken Youens-Clark <kyclark@email.arizona.edu>"
