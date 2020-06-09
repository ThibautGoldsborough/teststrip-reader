
"""
Created on Sat Jun 22 11:35:36 2019

@author: Thibaut Goldsborough


A python script to read test-strips from photographs. 


Multiple test strips can be photographed next to the 
reference test strip label. 


Add additional tests and modify the "test" variable (line 63)


A pygame window will open requiring the manual selection
of each reference color on the test strip label (Proceed 
in the order specified in the test strip list). Once all 
the colors on the reference label have been selected, 
proceed to the test strips.

Once finished, press "a" to proceed to the next photograph 
in the folder.

"""


from tabulate import tabulate
import pygame
import matplotlib.pyplot as plt
import os

photos_list=[]
RESULTS={}


""" SPECIFY BASEPATH """
basepath ="/Users/Name/Documents/test-strip_photos/"

for entry in os.listdir(basepath):
    if os.path.isfile(os.path.join(basepath, entry)):
        photos_list.append(entry)
 
    
"""TEST STRIP LISTS """
pH=list((5,6,6.5,7,7.5,8,8.5))
protein=list((0,0.1,0.3,1,3,10)) #(g/l)
pH_fix=list((0,1,2,3,4,5,6,7))
Iron=list((0,0.3,0.5,1,3,5)) #ppm
Hardness=list((0,25,50,120,250,425)) #ppm of CaCO3
Peroxide=list((0,1,3,10,50,100)) #ppm
Copper=list((0,0.3,0.6,1,6))#ppm
Phosphate=list((0,100,200,300,500,1000,2500)) #ppb
NH4=list((0,0.1,0.2,0.4,0.6,1,1.5,3,5)) #mg/l (ppm)
NO3=list((0,1,5,10,20,40,80,160,240))#mg/l (ppm)
NO2=list((0,0.025,0.05,0.1,0.2,0.4,0.6,0.8,1.0)) #mg/l (ppm)
NO=list((20,110,435))#ppm 


""" SPECIFY DESIRED TEST """
test=protein





def findinterceptcol(col_list,test,obstest):
    intercepty=0
    for j in range(len(col_list)):      
        if j!=0: 
            if (test[j-1]>=obstest and test[j]<=obstest)or ((test[j-1]<=obstest and test[j]>=obstest)):                        
                coef=(col_list[j-1]-col_list[j])/(test[j-1]-test[j])
                b=col_list[j]-coef*test[j]
                intercepty=(coef*obstest+b)

    return(intercepty)
    
    
def findvert(colred,colgreen,colblue,red,green,blue,test,precision):
    differ=[]
    x_axis_values=[]
    for i in range(len(test)-1):
        x_axis_range=test[i]
        while x_axis_range<=test[i+1]:
            x_axis_values.append(x_axis_range)
            x_axis_range+=(test[i+1]-test[i])*precision
    for x_axis_value in x_axis_values:
        for j in range(len(colred)):
            differ.append((abs(red-findinterceptcol(colred,test,x_axis_value))+abs(green-findinterceptcol(colgreen,test,x_axis_value))+abs(blue-findinterceptcol(colblue,test,x_axis_value)),x_axis_value))
    return(min(differ))
        
pygame.display.init() 
sampling=False
displayresults=False

for j in range(len(photos_list)):
    if photos_list[j]!='.DS_Store':

        results=[]
        fits=[]
        tab=[]
        running=True
        count=0
        sampling=False
        displayresults=False
        colred,colgreen,colblue,lred,lgreen,lblue=[],[],[],[],[],[]
        

        a1=photos_list[j]
        a2=pygame.image.load(basepath+a1)
        print('Image',a1)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
                pygame.display.quit()
        
        while running==True:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running=False
                    pygame.display.quit()
            if (pygame.key.get_pressed()[pygame.K_p]!=0):
                test=pH_fix
                print("PH")
            if (pygame.key.get_pressed()[pygame.K_c]!=0):
                test=Hardness
                print("Hardness")
            if (pygame.key.get_pressed()[pygame.K_o]!=0):
                test=protein
                print("Protein")
                
            display_surface = pygame.display.set_mode((1400,300)) 
            a=pygame.transform.scale(a2, (1400, 300)) 
            white=(250,250,250)
            display_surface.fill(white)
            display_surface.blit(a, (0, 0))
            pygame.display.update()
            
            if sampling==False:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos=pygame.mouse.get_pos()
                        red,green,blue=0,0,0
                        sampling=True
                        pygame.time.wait(100)
                               
            if sampling==True: 
                
               pygame.draw.rect(display_surface,(0,0,0), [pos[0],pos[1],pygame.mouse.get_pos()[0]-pos[0],pygame.mouse.get_pos()[1]-pos[1]],2)
               pygame.display.update()
               
                
            if sampling==True:    
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        display_surface.fill(white)
                        display_surface.blit(a, (0, 0))
                        pygame.display.update()
                        sampling=False
                        pos2=pygame.mouse.get_pos()
                        red,green,blue=0,0,0
                        lengy=abs(pos[1]-pos2[1])
                        lengx=abs(pos[0]-pos2[0])
                        startposx=min(pos[0],pos2[0])
                        startposy=min(pos[1],pos2[1])
                        for i in range(lengx):
                            for j in range(lengy):
                                red+=display_surface.get_at((startposx+i,startposy+j))[0]
                                green+=display_surface.get_at((startposx+i,startposy+j))[1]
                                blue+=display_surface.get_at((startposx+i,startposy+j))[2]
                        if count<len(test):
                            colred.append(red/(lengx*lengy))
                            colgreen.append(green/(lengx*lengy))
                            colblue.append(blue/(lengx*lengy))
                            count+=1
                        else:
                            lred.append(red/(lengx*lengy))
                            lgreen.append(green/(lengx*lengy))
                            lblue.append(blue/(lengx*lengy))
                        
            if (pygame.key.get_pressed()[pygame.K_a]!=0):
                displayresults=True
            if displayresults==True:
                for colors in range(len(lred)):
                    red,green,blue=lred[colors],lgreen[colors],lblue[colors]
                    estimate=findvert(colred,colgreen,colblue,red,green,blue,test,0.001)[1]
                    fit=findvert(colred,colgreen,colblue,red,green,blue,test,0.001)[0]
                    plt.plot(test,colred,"r")
                    plt.plot(test,colgreen,"g")
                    plt.plot(test,colblue,"b")
                    plt.hlines(red,xmin=min(test),xmax=max(test),color="r",linestyles='dashed')
                    plt.hlines(green,xmin=min(test),xmax=max(test),color="g",linestyles='dashed')
                    plt.hlines(blue,xmin=min(test),xmax=max(test),color="b",linestyles='dashed')
                    plt.vlines(estimate,ymin=0,ymax=250)
                    plt.ylabel('Color Intensity')
                    plt.show()
                           
                    results.append(estimate)
                    fits.append(fit)
                    print("Prediction:",estimate,"   Fit:",fit)
                
                for z in range(len(fits)):
                    tab.append((results[z],fits[z]))
                running=False
                print("")
                print(a1)
                print(tabulate(tab,headers=("Estimate","Fit"),tablefmt="fancy_grid"))
                RESULTS[a1]=results
pygame.display.quit()

print(RESULTS)
