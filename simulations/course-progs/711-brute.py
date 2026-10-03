# Brute force search for solutions to 711 puzzle
# x+y+z+r = 711,
# x*y*z*(711-x-y-z) = 711*10**6  
# All prices are in cents.
# All combinations such that x <= y <= z  are generated
# but only if  x <= y <= z <= r the equation is checked.

n = 0
for x in range(1,709):
    for y in range(x,710-x):
        for z in range(y,711-x-y):
            r = 711-x-y-z
            if (z <= r): 
                n = n+1
                if (x*y*z*r==711000000): print('x,y,z,r',x,y,z,r,' cents') 
print(  ' checked',n,'  cases' )
