'''
Problem Statement: Given a area of land (in sq.units), the algorithm
should pave the following buildings with different set of Rules
initially and then scale up at later version to embed RL into it to
get maximum returns from the population.

Each sq.unit of land will be occupied by each unit (MC, R, H, HSCH etc...)
Depending on the area given repetitions are allowed (Based on Rules)

Initial version(0.0.1): Pave the building layout depending on the rules given.

Rules Log:
1. Initial version(0.0.1) will pave a layout for the Layout1 design of city from excel sheet.

Buildings List: Refer to excel sheet:
1. Mountain Cottage (MC) - These are buildings that generally align towards the Mountain areas.
2. Road (R) - Every house/ Mountain Cottage should have access to the Road. Indeed every
building(House, MC or PS,P,C etc..) should have access.
3. House (H) - Surely far from Power Plants (Power Plants)
4. High School (HSCH) - Should be away from the Power Plants and should be beside houses.
Atleast 1 for 20 houses(MCs included)
5. Police Station (PS) - Should be in vicinity of houses. Should be atleast 1 for 8 houses.
6. Clinic (C) - Should be around houses. Should be atleast 1 for 8 houses.
7. Coal Power Plant (CPP) - Shouldn't be around Houses and HighSchool. Should be atleast 1 for 20 houses.
'''

# required libraries
import numpy as np

# Classes for each element of the city
class MC():
    '''
    Location: Mountain Cottages (MCs) generally lie in the vicinity of Mountains.
    Population: Can accommodate around 20 people.
    '''
    location = dict({'N':None, 'E':None, 'W':None, 'S':None})
    population = 20
    def __init__(self):
        self.location = location
        self.population = population

class R():
    '''
    Location: Roads generally connect every element in the map.
    Atleast one direction of an element in the map should have a Road (Traversible road indeed).
    Population: NA
    '''
    location = dict({'N':None, 'E':None, 'W':None, 'S':None})
    def __init__(self):
        self.location = location

class H():
    '''
    Location: Mountain Cottages (MCs) generally lie in the vicinity of Mountains.
    Population: Can accommodate around 20 people.
    '''
    location = dict({'N':None, 'E':None, 'W':None, 'S':None})
    def __init__(self):
        self.location = location
        self.population = 50

class HSCH():
    '''
    Location: Schools should be in the vicinity of houses and away from CPP (Coal Power Plant)
    '''
    location = dict({'N':None, 'E':None, 'W':None, 'S':None})
    def __init__(self):
        self.location = location

class PS():
    '''
    Location: PS should be in the vicinity of houses.
    serviceability: Atleast 1 for 8 houses.
    '''
    location = dict({'N':None, 'E':None, 'W':None, 'S':None})
    def __init__(self):
        self.location = location
        self.serviciabiity = 8

class C():
    '''
    Location: C should be in the vicinity of houses.
    serviceability: Atleast 1 for 8 houses.
    '''
    location = dict({'N':None, 'E':None, 'W':None, 'S':None})
    def __init__(self):
        self.location = location
        self.serviciabiity = 8

class CPP():
    '''
    Location: CPP should be away from houses.
    serviceability: Atleast 1 for 8 houses.
    '''
    location = dict({'N':None, 'E':None, 'W':None, 'S':None})
    def __init__(self):
        self.location = location
        self.serviciabiity = 20

class city():
    '''
    rows: rows into which each unit of the city could be placed
    cols: cols into which each unit of the city could be placed
    '''
    
    def __init__(self, rows, cols):
        '''
        Parameters
        ----------
        rows : TYPE
            DESCRIPTION.
        cols : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        self.rows = rows
        self.cols = cols
        
    def check_plot(self, layout, row, col):
        '''
        Parameters
        ----------
        layout : TYPE
            DESCRIPTION.
        row : TYPE
            DESCRIPTION.
        col : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        if layout[row][col] != 0.0:
            return((False,layout[row][col]))
        else:
            return(True)
        
    def layout_rules(self, row, col):
        '''

        Parameters
        ----------
        row : TYPE
            DESCRIPTION.
        col : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        # layout_rules gets the row and col to understand the plot location and allocates node item accordingly
        if row == 0:
            # Generally only MCs will be constructed here
            print('At the Mountains')
            return('MC')
            
        else:
            print('In the city')
            
    def startDesign(self):
        '''

        Returns
        -------
        None.

        '''
        # creating a matrix of city layout
        prime_layout = np.zeros((self.rows, self.cols))
        #return(prime_layout)
    
        # randomly accessing the plots of the layout
        for i in range(100):
            rand_row = np.random.randint(0, self.rows)
            rand_col = np.random.randint(0, self.cols)
            print(rand_row, rand_col)
            
            # Check if the plot is already occupied
            occupy_flag = self.check_plot(prime_layout, rand_row, rand_col)
            print(occupy_flag)
            
            # If plot is free, select an item acc to rules
            if occupy_flag:
                # Assign a new node as per the layout_rules
                self.layout_rules(rand_row, rand_col)
            
        
# Implementation
if __name__ == '__main__':
    city1 = city(5,4)
    
    # printing initial design
    #print('Printing Initial City Layout')
    #layout = city1.startDesign()
    #print(layout)
    city1.startDesign()



