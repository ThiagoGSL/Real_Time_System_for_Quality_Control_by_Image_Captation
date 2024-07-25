import numpy as np
import time
from threading import Thread, Lock
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient() #REquesting conection with API Client
sim = client.require('sim')

#CUBES VARIABLES:
CUBE_SIDE = 0.15
CUBE_RADIUS = CUBE_SIDE/np.sqrt(2)

#CONVEYOR_VARIABLES:
CONVEYOR_LENGTH = 2
CONVEYOR_WIDTH = 0.5
CONVEYOR_TARGET_VEL = 0.1
CONVEYOR_HANDLE = sim.getObjectHandle("/conveyor")
CONVEYOR_POSITION = sim.getObjectPosition(CONVEYOR_HANDLE)
print(CONVEYOR_POSITION)

#FEEDER_VARIABLES:
FEEDER_HANDLE = sim.getObjectHandle("/Feeder")
REF_POINT = list(np.array(CONVEYOR_POSITION)+[-0.8,-0.25,0.2])
print(REF_POINT)
min_y_location = REF_POINT[1]+CUBE_RADIUS
max_y_location = REF_POINT[1]+CONVEYOR_WIDTH-CUBE_RADIUS
GEN_DEADLINE = 2*CUBE_RADIUS/CONVEYOR_TARGET_VEL


#Color list
colors = [[0.0,0.0,1.0], #blue
         [1.0,1.0,0.0]]  #yellow


cubes_ext_y_locations = []

cube_locations = Lock()

def generate_cube(y_location, orientation, color, CUBE_SIDE, REF_POINT):
    cube = sim.createPrimitiveShape(sim.primitiveshape_cuboid, list(np.array([1,1,1])*CUBE_SIDE))
    sim.setObjectParent(cube, FEEDER_HANDLE, True)
    
    #Setting properties
    sim.setShapeMass(cube,1)
    
    sim.setObjectInt32Param(cube, sim.shapeintparam_static, 0)
    sim.setObjectInt32Param(cube, sim.shapeintparam_respondable, 1)
    
    special_properties = sim.objectspecialproperty_collidable|sim.objectspecialproperty_measurable|sim.objectspecialproperty_detectable
    sim.setObjectSpecialProperty(cube, special_properties)
    
    sim.setObjectColor(cube, 0, sim.colorcomponent_ambient_diffuse, color)
    
    new_location = REF_POINT.copy()
    new_location[1] = y_location


    sim.setObjectPosition(cube, new_location, sim.handle_world)
    sim.setObjectOrientation(cube, [0,0,orientation], sim.handle_world)
    
    
#Thread functions
def cube_feeder_thread_function(cube_locations):
    client = RemoteAPIClient()
    sim = client.require('sim')
    global cubes_ext_y_locations
    while sim.getSimulationState() != sim.simulation_stopped:
        if sim.getSimulationState() == sim.simulation_advancing_running:
            # Defining random location, orientation and color
            rand_orientation = np.random.uniform(0,90)
            rand_y_location = np.random.uniform(min_y_location, max_y_location)
            rand_color = colors[np.random.randint(0,2)]

            # Defining low and high location point in y axis
            a, b = rand_y_location-CUBE_RADIUS, rand_y_location+CUBE_RADIUS
            
            if cubes_ext_y_locations:
                #print("Acquiring cube_locations lock")
                with cube_locations:
                    #Verifing if there are cubes in a higher y_location point compared to the new cube
                    try:
                        min_high_loc = np.min([a1 for (a1, b1) in cubes_ext_y_locations if b1 > rand_y_location])
                    except:
                        min_high_loc = REF_POINT[1]+CONVEYOR_WIDTH
                    
                    
                    #Verifing if there are cubes in a lower y_location point compared to the new cube
                    try:
                        max_low_loc =  np.max([b1 for (a1, b1) in cubes_ext_y_locations if a1 < rand_y_location])
                    except:
                        max_low_loc = REF_POINT[1]
                        
                    #Verifing if the espace available for the new cube is enough
                    if max_low_loc < a and b < min_high_loc:
                        print("gerando cubo")
                        generate_cube(rand_y_location, rand_orientation, rand_color, CUBE_SIDE, REF_POINT)
                        
                        cubes_ext_y_locations.append((a,b))
                        #print("Releasing cube_locations lock")
                    
            else:
                print("gerando cubo")
                generate_cube(rand_y_location, rand_orientation, rand_color, CUBE_SIDE, REF_POINT)
                
                with cube_locations:
                    cubes_ext_y_locations.append((a,b))
                
            time.sleep(GEN_DEADLINE)
    

def feeder_reset_thread_function(cube_locations):
    client = RemoteAPIClient()
    sim = client.require('sim')
    global cubes_ext_y_locations
    while sim.getSimulationState() != sim.simulation_stopped:
        if sim.getSimulationState() == sim.simulation_advancing_running:
            time.sleep(3)
            
            with cube_locations:
                cubes_ext_y_locations = []
                print(f"Cubos resetados")



#Program start
sim.startSimulation()

cube_generator_thread = Thread(target=cube_feeder_thread_function, args=(cube_locations,))
feeder_reset_thread = Thread(target=feeder_reset_thread_function, args=(cube_locations,))

# Start threads
cube_generator_thread.start()
feeder_reset_thread.start()

cube_generator_thread.join()
feeder_reset_thread.join()

print("Simulation stopped")