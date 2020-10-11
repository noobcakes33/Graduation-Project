from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
#####################################
import time
import csv
import winsound
import numpy as np
##import h5py
from model import *
#####################################
import ctypes
import _ctypes
import pygame
import sys

if sys.hexversion >= 0x03000000:
    import _thread as thread
else:
    import thread

# colors for drawing different bodies 
SKELETON_COLORS = [pygame.color.THECOLORS["red"], 
                  pygame.color.THECOLORS["blue"], 
                  pygame.color.THECOLORS["green"], 
                  pygame.color.THECOLORS["orange"], 
                  pygame.color.THECOLORS["purple"], 
                  pygame.color.THECOLORS["yellow"], 
                  pygame.color.THECOLORS["violet"]]

class BodyGameRuntime(object):
    x = 0
    coordinates = []
    data = []
    i = 1
    def __init__(self):
        pygame.init()

        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()

        # Set the width and height of the screen [width, height]
        self._infoObject = pygame.display.Info()
        self._screen = pygame.display.set_mode((self._infoObject.current_w >> 1, self._infoObject.current_h >> 1), 
                                               pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)

        pygame.display.set_caption("Kinect for Windows v2 Body Game")

        # Loop until the user clicks the close button.
        self._done = False

        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()

        # Kinect runtime object, we want only color and body frames 
        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)

        # back buffer surface for getting Kinect color frames, 32bit color, width and height equal to the Kinect color frame size
        self._frame_surface = pygame.Surface((self._kinect.color_frame_desc.Width, self._kinect.color_frame_desc.Height), 0, 32)

        # here we will store skeleton data 
        self._bodies = None


    def draw_body_bone(self, joints, jointPoints, color, joint0, joint1):
        joint0State = joints[joint0].TrackingState;
        joint1State = joints[joint1].TrackingState;

        # both joints are not tracked
        if (joint0State == PyKinectV2.TrackingState_NotTracked) or (joint1State == PyKinectV2.TrackingState_NotTracked): 
            return

        # both joints are not *really* tracked
        if (joint0State == PyKinectV2.TrackingState_Inferred) and (joint1State == PyKinectV2.TrackingState_Inferred):
            return

        # ok, at least one is good 
        start = (jointPoints[joint0].x, jointPoints[joint0].y)
        end = (jointPoints[joint1].x, jointPoints[joint1].y)
        #print start, end
        #time.sleep(1)
        #print (jointPoints[joint0].x, jointPoints[joint0].y), (jointPoints[joint1].x, jointPoints[joint1].y)
        
        try:
            pygame.draw.line(self._frame_surface, color, start, end, 8)
        except: # need to catch it due to possible invalid positions (with inf)
            pass

    def draw_body(self, joints, jointPoints, color):

        # Right Arm    
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderRight, PyKinectV2.JointType_ElbowRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowRight, PyKinectV2.JointType_WristRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_HandRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HandRight, PyKinectV2.JointType_HandTipRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_ThumbRight);

        
        # Left Arm
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderLeft, PyKinectV2.JointType_ElbowLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowLeft, PyKinectV2.JointType_WristLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_HandLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HandLeft, PyKinectV2.JointType_HandTipLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_ThumbLeft);
        

    def draw_color_frame(self, frame, target_surface):
        target_surface.lock()
        address = self._kinect.surface_as_array(target_surface.get_buffer())
        ctypes.memmove(address, frame.ctypes.data, frame.size)
        del address
        target_surface.unlock()

    def run(self):
        # -------- Main Program Loop -----------
        #t_end = time.time() + 2
        #while time.time() < t_end:
        while not self._done:
            # --- Main event loop
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self._done = True # Flag that we are done so we exit this loop

                elif event.type == pygame.VIDEORESIZE: # window resized
                    self._screen = pygame.display.set_mode(event.dict['size'], 
                                               pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)
                    
            # --- Game logic should go here

            # --- Getting frames and drawing  
            # --- Woohoo! We've got a color frame! Let's fill out back buffer surface with frame's data 
            if self._kinect.has_new_color_frame():
                frame = self._kinect.get_last_color_frame()
                self.draw_color_frame(frame, self._frame_surface)
                frame = None

            # --- Cool! We have a body frame, so can get skeletons
            if self._kinect.has_new_body_frame(): 
                self._bodies = self._kinect.get_last_body_frame()

            # --- draw skeletons to _frame_surface
            if self._bodies is not None: 
                for i in range(0, self._kinect.max_body_count):
                    body = self._bodies.bodies[i]
                    if not body.is_tracked: 
                        continue 
                    
                    joints = body.joints
                    # convert joint coordinates to color space 
                    joint_points = self._kinect.body_joints_to_color_space(joints)
                    self.draw_body(joints, joint_points, SKELETON_COLORS[i])
                    
                    # >>>>>>>>>>>>>>>>> OUR COORDINATION FUCNTION <<<<<<<<<<<<<<<<<<<<<<<
                    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                 
                    # Right Arm
                    HandTipRight = [joint_points[PyKinectV2.JointType_HandTipRight].x , joint_points[PyKinectV2.JointType_HandTipRight].y]
                    ThumbRight = [joint_points[PyKinectV2.JointType_ThumbRight].x , joint_points[PyKinectV2.JointType_ThumbRight].y]
                    HandRight = [joint_points[PyKinectV2.JointType_HandRight].x , joint_points[PyKinectV2.JointType_HandRight].y]
                    WristRight = [joint_points[PyKinectV2.JointType_WristRight].x , joint_points[PyKinectV2.JointType_WristRight].y]
                    ElbowRight = [joint_points[PyKinectV2.JointType_ElbowRight].x , joint_points[PyKinectV2.JointType_ElbowRight].y]
                    print("HandTipRight:", HandTipRight)
                    print("ThumbRight:", ThumbRight)
                    print("HandRight:", HandRight)
                    print("WristRight:", WristRight)
                    print("ElbowRight:", ElbowRight)
                                    
                    # Left Arm
                    HandTipLeft = [joint_points[PyKinectV2.JointType_HandTipLeft].x , joint_points[PyKinectV2.JointType_HandTipLeft].y]
                    ThumbLeft = [joint_points[PyKinectV2.JointType_ThumbLeft].x , joint_points[PyKinectV2.JointType_ThumbLeft].y]
                    HandLeft = [joint_points[PyKinectV2.JointType_HandLeft].x , joint_points[PyKinectV2.JointType_HandLeft].y]
                    WristLeft = [joint_points[PyKinectV2.JointType_WristLeft].x , joint_points[PyKinectV2.JointType_WristLeft].y]
                    ElbowLeft = [joint_points[PyKinectV2.JointType_ElbowLeft].x , joint_points[PyKinectV2.JointType_ElbowLeft].y]
                    print("HandTipLeft:", HandTipLeft)
                    print("ThumbLeft:", ThumbLeft)
                    print("HandLeft:", HandLeft)
                    print("WristLeft:", WristLeft)
                    print("ElbowLeft:", ElbowLeft)
                    
                    BodyGameRuntime.x +=1
                    while len(BodyGameRuntime.coordinates) < 800:
                        '''
                        if len(BodyGameRuntime.coordinates) == 0:
                            time.sleep(2)R
                            winsound.PlaySound('button-09.wav', winsound.SND_FILENAME)
                        '''
                        BodyGameRuntime.coordinates += HandTipRight+ThumbRight+HandRight+WristRight+ElbowRight+HandTipLeft+ThumbLeft+HandLeft+WristLeft+ElbowLeft

                    #print("Coordinates: ",BodyGameRuntime.coordinates)
                    #print(type(BodyGameRuntime.coordinates))
                    #print(len(BodyGameRuntime.coordinates))
                    #print(np.array(BodyGameRuntime.coordinates))
                    #print(type(np.array(BodyGameRuntiRRRRRme.coordinates)))
                    #print(len(np.array(BodyGameRuntime.coordinates)))
                    #print(np.array(BodyGameRuntime.coordinates).shape)

                    predictedSign = modelPredict(np.array([BodyGameRuntime.coordinates]))
                    if predictedSign != 'rubbish':
                        engine.say(str(predictedSign))
                        engine.runAndWait()
                    BodyGameRuntime.coordinates = []


                    #BodyGameRuntime.data.append(BodyGameRuntime.coordinates)
                    '''
                    if len(BodyGameRuntime.coordinates) == 800:
                        print(BodyGameRuntime.coordinates)
                        np.save('coordinates_output_'+str(BodyGameRuntime.i),[BodyGameRuntime.coordinates])
                        BodyGameRuntime.i +=1
                        BodyGameRuntime.coordinates = []
                        #d = np.load('coordinates_output.npy')
                        #h = h5py.File('hello_train.hdf5','w')
                        #dset = h.create_dataset('train', data=d)
                        
                    if len(BodyGameRuntime.data) == 40:
                        with open("output2.csv","w") as f:
                            writer = csv.writer(f)
                            writer.writerows(BodyGameRuntime.data)
                        winsound.PlaySound('button-3.wav', winsound.SND_FILENAME)
                            
                    if BodyGameRuntime.x == 40:
                        print("40 frames done !")
                        winsound.PlaySound('button-3.wav', winsound.SND_FILENAME)   
                    
                    '''

                    # >>>>>>>>>>>>>>>>> OUR COORDINATION FUCNTION <<<<<<<<<<<<<<<<<<<<<<<
                    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                    
            # --- copy back buffer surface pixels to the screen, resize it if needed and keep aspect ratio
            # --- (screen size may be different from Kinect's color frame size) 
            h_to_w = float(self._frame_surface.get_height()) / self._frame_surface.get_width()
            target_height = int(h_to_w * self._screen.get_width())
            surface_to_draw = pygame.transform.scale(self._frame_surface, (self._screen.get_width(), target_height));
            self._screen.blit(surface_to_draw, (0,0))
            surface_to_draw = None
            pygame.display.update()

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit to 60 frames per second
            self._clock.tick(20)
            

        # Close our Kinect sensor, close the window and quit.
        self._kinect.close()
        pygame.quit()


__main__ = "Kinect v2 Body Game"
game = BodyGameRuntime();
game.run();

