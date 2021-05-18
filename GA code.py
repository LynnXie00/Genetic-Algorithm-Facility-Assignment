import random
from xlrd import open_workbook


#define the total distance
def total_distance(A, d):
    Sum=0
    for j in range(len(A)):
        for i in range (len(A[0])):
            Sum=Sum+A[j][i]*d[j][i]
    return Sum  #minimization problem, thus use the inverse

#calculate Aij based on clients(Xj)
def get_A(X,d):
    A=[[0 for j in range(len(d[0]))] for i in range(len(d))] #generate an A with 0s
    
    for i in range(len(A)):
        #select a subgroup of distance that sites are open\
        Sub_dj={}
        for j in range(len(X)):
            if X[j]!=0:
                Sub_dj[str(d[i][j])]=j
        #find the closet client
        min_d_j=sorted(Sub_dj)[0]
        A[i][Sub_dj[min_d_j]]=1
    return A          
                
#load distance dij from the excel file
wb = open_workbook('data.xlsx')
distances=[]
for ws in wb.sheets():
    for row in range(ws.nrows):
        values = []
        for col in range(ws.ncols):
            values.append(ws.cell(row,col).value)
        distances.append(values)
        
#number of candidate sites
    
sites=len(distances[0])
print("There are ",sites,"candidate sites ", end="and ")
#number of clients
clients=len(distances)
print(clients,"clients.")
#define mutation rate
r=float(input("What's the mutation rate? (0~1) "))

#define the number of solutions in the population (has to be even)
s=int(input("What's the population size (even number): "))

#define the number of sites needed
facilities=int(input("How many facilities do you want to open? "))

#define the number of iternations you need
iteration_n=int(input("How many iterations do you need? "))
        
iteration=1
#generate random solutions, a multi-dimensional list of s*sites
solutions=[[] for j in range(s)] 

for j in range(s):
    for i in range (sites):
        solutions[j].append(random.randint(0,1))
print("Running...",end="")        
while(iteration<iteration_n): #set the stop condition to number of iteration
    print(".",end="")  
    #select a random position to cross-over
#     print("________iteration",iteration,"________")
    p_c=random.randint(1,sites-1)
#     print("cross-over position is after:",p_c,"th number") #1-based index
    #cross-over
    solutions_c=[[] for j in range(s)] 
    for j in range(s):
        if(j % 2)== 0:
            solutions_c[j]=solutions[j][0:p_c]+solutions[j+1][p_c:sites]
        else:
            solutions_c[j]=solutions[j][0:p_c]+solutions[j-1][p_c:sites]

#     print("cross over")
#     for j in range(s):
#         print(solutions_c[j])
            
    #mutate_change an integer of n solutions
    n=int(r*s)
    solutions_m=solutions_c
    seq = [i for i in range(s)]
    s_m=random.choices(seq,k=n)
    for i in s_m:
        p_m=random.randint(0,sites-1)
        solutions_m[i][p_m]= 1- solutions_c[i][p_m]
#         print("mutation's position is",p_m+1,"for solution",i+1) #1-based index
        
#     print("mutation")
#     for j in range(s):
#         print(solutions_m[j])
        
    #calculate fitness
    fit_value=[]
    fit_percent=[]
    Total_fit=0
    for x in range(s):
        fit=1/total_distance(get_A(solutions_m[x],distances),distances)
        fit_value.append(fit)
        Total_fit=Total_fit+fit
    for x in range(s):
        fit_percent.append(fit_value[x]/Total_fit)
    #select offspring from mutated solutions based on fitness percentage     
    offsprings=random.choices(solutions_m,weights=fit_percent,k=s)
    
    for x in range(s):
        for y in range(sites):
            site_num=sum(offsprings[x])
            list=[a for a in range(sites)]
            #if select more than k sites, randomly close some until it's good
            while site_num>facilities:
                offsprings[x][random.choice(list)]=0
                site_num=sum(offsprings[x])
            #if less than k, randomly open some
            while site_num<facilities:
                offsprings[x][random.choice(list)]=1
                site_num=sum(offsprings[x])
                
    solutions=offsprings
    iteration=iteration+1
    
print("")    
print("Finished",iteration," iterations")
#sort the solution by distance
sorting_solutions={}
for k in range(s):
    sorting_solutions[str(total_distance(get_A(solutions[k],distances),distances))]=solutions[k]
sorted_solutions=sorted(sorting_solutions.items(),reverse=True)
#print out solutions
print("Solutions are displayed in descending order by the total distance (no duplication):")
for dis, Xis in sorted_solutions:    
    print("Xi:",Xis ,"__total distance:",round(dis,2))