# Analysis instructions

1. Install the [Miniconda Python distribution](https://repo.continuum.io/miniconda/Miniconda2-latest-Windows-x86_64.exe)
2. Open up a cmd window
3. Navigate to the folder where you saved the attached files (type the following and hit Enter):

  `cd C:\path\to\saved\files`
  
4. Create the environment:

  `conda env create -f environment.yml`
  
5. Activate the environment:

  `activate elpcjd`
  
6. Run elpc-test.py script:

  `python elpc-test.py C:\path\to\sessions\folder`
  
Steps 1-4 only need to be completed once, and step 5 whenever you open a new cmd window. The script creates a folder for each sensor type (Humidity/Temperature/etc.), copies over all the relevant session data, then performs the max/min/mean/median analysis.