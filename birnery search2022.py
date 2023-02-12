n= int(input("Enter the list"))
a=[]
for i in range(n):
    a.append(int(input("Enter the no ")))
    a.sort()

x= int(input("Enter the element"))

flag= False
f=0
l=n-1

while(f<=l):
    m=(f+l)//2
    
    if (a[m]<x):
        f=m+1
    elif(a[m]>x):
        f=m-1
    else:
        flag= True 
        break;
    
if(flag== True):
    print("Found")
else:
    print("Not Found")
    