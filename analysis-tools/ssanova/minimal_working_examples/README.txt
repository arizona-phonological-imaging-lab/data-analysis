Before you try to run a minimal working example of the SSANOVA.R script, you should know some things. 

An SSANOVA (smoothing spline ANOVA) compares two curves to tell you if they are different or not. For our purposes, we are using the SSANOVA to tell if two tongue contours are different. That means that we are only ever comparing two tongue contours (each corresponding to a point in an articulation of a sound). These could be two vowels, two fricatives, to stop closures, whatever you want. For more info, check out Davidson (2006) "Comparing tongue shapes from ultrasound imaging using smoothing spline analysis of variance."

With that in mind, let's run an example. You should find three example data files in this same folder.

    ssanova_ready_achlais.txt
    ssanova_ready_balach.txt
    ssanova_ready_airgead.txt

Each file contains x's and y's corresponding to tongue contours of two sounds. Each sound has three sets of x's and y's. This means that the participant who said these words said the same word three times, and then each word (ie sound of interest) was traced. Open one up and take a look.

The files listed above have a word at the end of the file name. This word contains one of our two sounds of interest. To run the SSANOVA.R, you must know both sounds, because they are arguments to run the script.

For example, to use the ssanova_ready_achlais.txt data:

(1) open the SSANOVA.R script

(2) at the bottom of the script, change the datalocation variable to your local data file path, such as:

    datalocation <- '/home/josh/Desktop/ssanova_ready_achlais.txt'

(3) at the very bottom of the script, change the first two arguments to the compare function to the two sounds in the datafile, such as:
    compare("achlais_sf", "tulg_Vu2", mydata)

(4) save and run the script

