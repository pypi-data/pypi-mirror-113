import numpy as np
import scipy.stats as sp
import pandas as pd
from matplotlib import pyplot as plt


#Concept & Shannon Diversity sections @author: pbelange
#adapted by @author: jcaleta
############################################################################################################
#DEFINE FUNCTIONS & VARIABLES
#############################################################################################################

def expect_shandiv(distr):
    nonz_distr=np.asarray(distr)
    nonz_distr=np.where(nonz_distr == 0, 1, nonz_distr)
    return (sum(np.log(nonz_distr)*(nonz_distr))*-1)/1.3862943611198906

# def exper_shandiv(A, C, G, T):
#     N = A + T + C + G
#     return ((A/N*np.log(A/N) + T/N*np.log(T/N) + C/N*np.log(C/N) + G/N*np.log(G/N))*-1)/1.3862943611198906

def exper_shandiv(A, C, G, T):
    N = A + T + C + G
    array=np.asarray((A, C, G, T))
    array=np.where(array == 0, 1, array)
    A=array[0]
    C=array[1]
    G=array[2]
    T=array[3]
    return ((A/N*np.log(A/N) + T/N*np.log(T/N) + C/N*np.log(C/N) + G/N*np.log(G/N))*-1)/1.3862943611198906

def expect_pi(distr):
    A=distr[0]
    C=distr[1]
    G=distr[2]
    T=distr[3]
    return 1 - (A**2 + C**2 + G**2 + T**2)
    #return ((A*T + A*C + A*G + T*C + T*G + C*G)*10000)/4950.0
    
def exper_pi(A, C, G, T):
    N = A + T + C + G
    return (A*T + A*C + A*G + T*C + T*G + C*G)/((N**2-N)/2)

def expect_alt(distr):
    return (1 - np.amax(distr))*100
    
def exper_alt(random_nt_count):
    alt_mat = np.matrix(random_nt_count)
    N = np.sum(alt_mat, axis=0)
    max_alt = alt_mat.max(axis=0)
    return (N-max_alt)/N*100 
        
nt_distr=pd.read_csv('ACGT_distr.txt', sep='\t', header=None)
nt_distr=np.asarray(nt_distr.iloc[:,1:5])  
distr=sp.mode(nt_distr, axis=0).mode
distr=distr[0]/100
distr=np.around(distr, decimals=2, out=None)
distr=distr/np.sum(distr)

N = np.logspace(1,6,60).astype(int)
organism = 100


#########################SHANNON DIVERSITY SIM###########################################################################   

sim_shandiv_data = []     

for reads in N:
    random_nt = np.random.choice(np.array([1,2,3,4]), size=(reads,organism), p=distr)
    random_nt_count = [np.sum(random_nt==i,axis=0) for i in [1,2,3,4]] #sum the boolean instances for i==1, i==2, i==3, & i==4
    #across all columns (vertically) at once and store in 4 arrays of random_nt_count (i.e. 20 values for number of As, 20 values for
    #number of Ts....).NOTE: has to be array [] for this for loop format to work.
    sim_shandiv_data.append(exper_shandiv(random_nt_count[0],random_nt_count[1],random_nt_count[2],random_nt_count[3]))
    #superimposing entire arrays of A, T, C, G at every position to get shannon diversity ....so you end up with 20 shnnon diversities
    #per read depth (in this case 50) and you append those into a list so you will end up with a row per read depth, and 20 columns
    #(one per salmon)..

#plt.figure()
#for i in range(len(sim_shandiv_data)):
#    for j in range(organism):
#        plt.plot(N[i], sim_shandiv_data[i][j],'o',color='C0',alpha=0.3)

#The function 'zip' in python, basically compresses nested for loops into one line. So in this case,
#instead of going through every depth/ row then cycling through and plotting each column within that row,
#you 'zip' them:
#in the following, reads represents i, and shannonDiv represents j

#INDIVIDUAL SHANNON DIV PLOT
# plt.figure()
# for reads,shannonDiv in zip(N,sim_shandiv_data):
#     plt.plot(reads*np.ones(organism),shannonDiv,'o',color='C0',alpha=0.3)

# plt.axhline(expect_shandiv(distr),linestyle = '--',label='Expected Shannon Diversity')
# plt.axhline((expect_shandiv(distr)*0.05+expect_shandiv(distr)), linestyle = 'dotted', color='black', alpha=0.3, label='5% Error')
# plt.axhline(expect_shandiv(distr)-(expect_shandiv(distr)*0.05),linestyle = 'dotted', color='black', alpha=0.3)
# plt.title('Simulated Shannon Diversity at Different Sequencing Depths \nGiven a Nucleotide Distribution of %s' %str(distr))
# plt.xscale('log')
# plt.xlabel('Sequencing Depth (reads/site)')
# plt.ylabel('Shannon Diversity')
# plt.legend(frameon=False)
# plt.tight_layout()
# plt.show()

#len(sim_shandiv_data[0]) #columns..width
#len(sim_shandiv_data) #rows...height
        
########################PI DIVERSITY SIM#########################################################################
    
sim_pi = []

for reads in N:
    random_nt = np.random.choice(np.array([1,2,3,4]), size=(reads,organism), p=distr)
    random_nt_count = [np.sum(random_nt==i,axis=0) for i in [1,2,3,4]] 
    sim_pi.append(exper_pi(random_nt_count[0],random_nt_count[1],random_nt_count[2],random_nt_count[3]))

#exPi=round(expect_pi(distr), 2)-0.01
exPi=expect_pi(distr)

#INDIVIDUAL PI PLOT
# plt.figure()
# for reads,pi in zip(N,sim_pi):
#     plt.plot(reads*np.ones(organism),pi,'o',color='magenta',alpha=0.3)

# plt.axhline(exPi,linestyle = '--',color='magenta',label='Expected \u03C0 Diversity')
# plt.axhline((exPi*0.05+exPi), linestyle = 'dotted', color='black', alpha=0.3, label='5% Error')
# plt.axhline(exPi-(exPi*0.05),linestyle = 'dotted', color='black', alpha=0.3)
# plt.title('Simulated Nucleotide (pi) Diversity at Different Sequencing Depths \nGiven a Nucleotide Distribution of %s' %str(distr))
# plt.xscale('log')
# plt.xlabel('Sequencing Depth (reads/site)')
# plt.ylabel('\u03C0 Diversity')
# plt.legend(frameon=False)
# plt.tight_layout()
# plt.show()

#########################ALT ALLELE SIM###########################################################################

sim_alt = []

for reads in N:
    random_nt = np.random.choice(np.array([1,2,3,4]), size=(reads,organism), p=distr)
    random_nt_count = [np.sum(random_nt==i,axis=0) for i in [1,2,3,4]] 
    sim_alt.append(np.asarray(exper_alt(random_nt_count))) 

#INDIVIDUAL ALT ALLELE PLOT
# plt.figure()
# for i in range(len(N)):
#     for j in range(organism):
#         plt.plot(N[i], sim_alt[i][0][j],'o',color='gold',alpha=0.3)
        
# plt.axhline(expect_alt(distr),linestyle = '--',color='gold',label='Expected Alternative Allele Frequency')
# plt.axhline((expect_alt(distr)*0.05+expect_alt(distr)), linestyle = 'dotted', color='black', alpha=0.3, label='5% Error')
# plt.axhline((expect_alt(distr)-expect_alt(distr)*0.05),linestyle = 'dotted', color='black', alpha=0.3)
# plt.title('Simulated Alternate Allele Frequency at Different Sequencing Depths \nGiven a Nucleotide Distribution of %s' %str(distr))
# plt.xscale('log')
# plt.xlabel('Sequencing Depth (reads/site)')
# plt.ylabel('Non-Reference Bases (%)')
# plt.legend(frameon=False)
# plt.tight_layout()
# plt.show()
##########################THRESHOLD ################################################################################################################
#arrays
simShan_array=np.asarray(sim_shandiv_data)
simPi_array=np.asarray(sim_pi)
simFreq_array = [item for sublist in sim_alt for item in sublist]
simFreq_array=np.asarray(simFreq_array)

#error limits
shanLo=expect_shandiv(distr)-expect_shandiv(distr)*0.05
shanUp=expect_shandiv(distr)+expect_shandiv(distr)*0.05
piLo=exPi-(exPi*0.05)
piUp=(exPi*0.05+exPi)
freqLo=expect_alt(distr)-expect_alt(distr)*0.05
freqUp=expect_alt(distr)*0.05+expect_alt(distr)

#mask data points falling outside 5% error
simShan_within=np.ma.masked_outside(simShan_array, shanLo, shanUp)
simShan_within=np.ma.masked_invalid(simShan_within)
simPi_within=np.ma.masked_outside(simPi_array, piLo, piUp)
simPi_within=np.ma.masked_invalid(simPi_within)
simFreq_within=np.ma.masked_outside(simFreq_array, freqLo, freqUp) 
simFreq_within=np.ma.masked_invalid(simFreq_within)

#col=depths, values=how many points out of the 'organism' variable fall within the error range
#sum number of points at each depth that fall within 5% accuracy
shanWithinCount=np.ma.MaskedArray.count(simShan_within, axis=1)   
piWithinCount=np.ma.MaskedArray.count(simPi_within, axis=1)             
freqWithinCount=np.ma.MaskedArray.count(simFreq_within, axis=1) 

#percentage of data that is within error range 
shanWithinPerc=shanWithinCount/organism*100
shanAccuracy=N[np.where(shanWithinPerc>=80)][0]
piWithinPerc=piWithinCount/organism*100
piAccuracy=N[np.where(piWithinPerc>=80)][0]
freqWithinPerc=freqWithinCount/organism*100
freqAccuracy=N[np.where(freqWithinPerc>=80)][0]
#########################COMPOSITE PLOT#############################################################################################################
plt.figure(9)
fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)
fig.suptitle('Simulated Intrahost Genetic Diversity Metrics at Different Sequencing Depths Given a Nucleotide Distribution of %s' %str(distr), 
             fontsize=14, y=0.98)
for reads,shannonDiv in zip(N,sim_shandiv_data):
    ax1.plot(reads*np.ones(organism),shannonDiv,'o',color='xkcd:royal blue',alpha=0.3)
ax1.axhline(expect_shandiv(distr),linestyle = '--', color='xkcd:royal blue', label='Expected Shannon Diversity')
ax1.axhline(shanUp, linestyle = 'dotted', color='black', alpha=0.3, label='5% Error')
ax1.axhline(shanLo, linestyle = 'dotted', color='black', alpha=0.3)
ax1.axvline(x=100, color='gold')
ax1.axvline(x=500, color='teal')
ax1.axvline(x=shanAccuracy, color='black', alpha=0.4, linestyle='dashdot')
ax1.set_ylabel('Shannon Diversity (H)', fontsize=11)
ax1.legend(frameon=False)
for reads,pi in zip(N,sim_pi):
    ax2.plot(reads*np.ones(organism),pi,'h',color='deeppink',alpha=0.3)
ax2.axhline(exPi,linestyle = '--',color='deeppink',label='Expected Nucleotide Diversity')
ax2.axhline(piUp, linestyle = 'dotted', color='black', alpha=0.3, label='5% Error')
ax2.axhline(piLo,linestyle = 'dotted', color='black', alpha=0.3)
ax2.axvline(x=100, color='gold')
ax2.axvline(x=500, color='teal')
ax2.axvline(x=piAccuracy, color='black',alpha=0.4, linestyle='dashdot')
ax2.set_ylabel('Nucleotide Diversity (\u03C0)', fontsize=11)
ax2.legend(frameon=False)
for i in range(len(N)):
    for j in range(organism):
        plt.plot(N[i], sim_alt[i][0][j],'p',color='xkcd:orange yellow',alpha=0.3)
ax3.axhline(expect_alt(distr),linestyle = '--',color='xkcd:orange yellow',label='Expected Alternative \nAllele Frequency')
ax3.axhline(freqUp, linestyle = 'dotted', color='black', alpha=0.3, label='5% Error')
ax3.axhline(freqLo, linestyle = 'dotted', color='black', alpha=0.3)
ax3.axvline(x=100, color='gold')
ax3.axvline(x=500, color='teal')
ax3.axvline(x=freqAccuracy, color='black', alpha=0.4, linestyle='dashdot')
ax3.set_ylabel('Alt Allele Frequency (%)', fontsize=11)
ax3.legend(frameon=False)
plt.xscale('log')       
plt.xlabel('Sequencing Depth (reads/ site)', fontsize=13)     
plt.tight_layout()
fig.subplots_adjust(hspace=0.1)







    











