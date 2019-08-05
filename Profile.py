# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 14:48:30 2019

@author: Cristina Ponte Lira
"""
###############################################################################
# Tool to: 
# 1) plot beach profile for platform beaches;
# 2) 
#
###############################################################################
import numpy as np
import matplotlib.pyplot as plt
from shapely import geometry

class Profile:
    
# =============================================================================
#     General definitions
# =============================================================================
    x_coastline = 0
# =============================================================================
#     Sandy profile default parameters
# =============================================================================
    y_sandy_coastline = False
   
    beachface_slope = 0.12

# =============================================================================
#     Rocky profile default parameters
# =============================================================================
    y_rocky_coastline= False
    platform_slope = False
    
# =============================================================================
#     Domain parameters
# =============================================================================
    lower_bound = -5
    right_bound = 100
    upper_bound = False
    
# =============================================================================
#     Interpolation parameters
# =============================================================================    
    interpolate_angle = 0.9
# =============================================================================
      
    def __init__(self, filename, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        
        data = np.load(filename)
        x = data[:,0]
        y = data[:,1]
        
        #test if origin of profile in x axis, if false create zero position
        if x[0]>0:
            origin_profile = np.array([[0,y[0]]])
            self.data_new = np.insert(data,0,origin_profile,axis=0)
        else:
            self.data_new = data
            
        
#sandy profile must touch/end at platform profile
            
        #test if sandy profile touches platform
        sandy_line = geometry.LineString(self.data_new)
        y = (-self.platform_slope)*self.data_new[-1,0] + self.y_rocky_coastline
        platform_line = geometry.LineString([(0, self.y_rocky_coastline), (self.data_new[-1,0], y)])
        query = sandy_line.intersects(platform_line)    

        if query == True:
            intersect_point = sandy_line.intersection(platform_line)
            p = np.array(list(intersect_point.coords))
            xp = p[0,0]
    
            data_new_x = self.data_new[:,0]
    
            data_new2_x = []
            for i in data_new_x:
                if np.any(i <= xp):
                    data_new2_x.append(i)
                    data_new2_y = list(self.data_new[0:len(data_new2_x),1])
            
            self.data_new2 = np.transpose(np.array([data_new2_x,data_new2_y]))
            
            m1 = self.interpolate_angle #slope value to interpolate sandy profile until platform
            b1 = self.data_new2[-1,0] + m1 * self.data_new2[-1,1]
            #equation of the rocky platform
            m2 = self.platform_slope
            self.b2 = self.y_rocky_coastline
            #solve equation system
            eq_1 = np.array([[m1,1], [m2,1]])
            eq_2 = np.array([b1,self.b2])
            self.sandy_x = np.linalg.solve(eq_1, eq_2)
            self.data_new2 = np.insert(self.data_new2,len(self.data_new2),self.sandy_x,axis=0)
        
        else:
            #equation of the sandy line
            m1 = self.interpolate_angle #m1 - slope value to interpolate sandy profile until platform
            b1 = self.data_new[-1,0] + m1 * self.data_new[-1,1]
            #equation of the rocky platform
            m2 = self.platform_slope
            self.b2 = self.y_rocky_coastline
            #solve equation system
            eq_1 = np.array([[m1,1], [m2,1]])
            eq_2 = np.array([b1,self.b2])
            self.sandy_x = np.linalg.solve(eq_1, eq_2)
            self.data_new2 = np.insert(self.data_new,len(self.data_new),self.sandy_x,axis=0)
            
        self.x = self.data_new2[:,0]
        self.y = self.data_new2[:,1]
        
        self.x_coastline = self.data_new2[0,0]
        self.y_sandy_coastline = self.data_new2[0,1]
        
        rocky_par = [['y_rocky_coastline', self.y_rocky_coastline],['platform_slope',self.platform_slope]]
        print (rocky_par)
        
    def plot(self):
        plt.plot(self.x, self.y,'.r')
        
        # platform line
        plat = np.array([[0,self.y_rocky_coastline], self.data_new2[-1]])
        plt.plot(plat[:,0],plat[:,1],'g')
        
        plt.xlabel('distância horizontal (m)')
        plt.ylabel('cota (m - NMM)')
        
        
    def sandy_volArea(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
            
        self.upper_bound = self.y_sandy_coastline + 2
        self.left_bound = self.x_coastline
        
        p_lower_left_bound = geometry.Point(self.left_bound, self.lower_bound)
        p_lower_right_bound = geometry.Point(self.right_bound, self.lower_bound)
    
        #domain_bounds = (self.left_bound, self.right_bound, self.lower_bound, self.upper_bound)

        #build rocky profile
        x_platform_offshore_limit = self.right_bound
        y_platform_offshore_limit = self.y_rocky_coastline - self.platform_slope * (x_platform_offshore_limit - self.x_coastline)
        p_platform_offshore_limit = geometry.Point(x_platform_offshore_limit, y_platform_offshore_limit)
        p_rocky_coastline = geometry.Point(self.x_coastline, self.y_rocky_coastline)

        point_list = [p_rocky_coastline, p_platform_offshore_limit]
        #platform_profile = geometry.LineString([[p.x, p.y] for p in point_list])
        
        point_list.extend([p_lower_right_bound, p_lower_left_bound])
        self.platform_polygon = geometry.Polygon([[p.x, p.y] for p in point_list])

        #build sandy profile

        point_new = np.array([[self.left_bound, p_rocky_coastline.y]])
        sand = np.append(self.data_new2,point_new,axis=0)
        self.sandy_polygon = geometry.Polygon(sand)
        
        volume=geometry.Polygon(sand)
        volume.area
        print('Volume=')
        print(volume.area)
        
    def plot_volumeArea(self):
        
        #plot
        #rocky profile
        x, y = self.platform_polygon.exterior.xy
        plt.fill(x, y, color=(0.3, 0.3, 0.3)) 
        #sandy profile

        x, y = self.sandy_polygon.exterior.xy
        plt.fill(x, y) 

        #plt.plot(left_bound, p_rocky_coastline.y, 'o')
    
 
        