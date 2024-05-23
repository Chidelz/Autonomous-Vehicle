## NRC - Autonomous Vehicle Competition
We are participating in the National Robotics Competition (NRC) under the Autonomous Vehicle Challenge (AVC). The NRC is an annual event where students from all over the country come to compete in various robotic competitions. The challenges typically include events such as robot sumu, maze solving, line following, and more.  We are tasked to create a fully autonomous vehicle that will navigate a predetermined obstacle course that is located at the parking lot west of Marion Veteran Memorial Coliseum in Marion, Ohio. Our main goal is to have a successful run of the course where the vehicle navigates around the obstacles successfully and crosses the finish line in under 5 minutes. The course will consist of multiple multicolored buckets and a single ramp. The layout is illustrated below in Figure 1.  During the competition, each team is given 3 attempts to run through the course. The course will be closed to both spectators and participants, with participants running vehicles within the perimeter of the course. Only one vehicle may be allowed to run the course at a time. Figure 2 below illustrates the components that are on the obstacle course.


Figure 1: Obstacle Course Dimensions

## **udev: overview**

udev allows a Linux system to use consistent names for devices such as removable drives and printers, which in turn allows users to experience predictable behavior when devices are added or removed from the system. 
Muliple devices set(GPS and VESC)

How to setting up the udev rule for detect the multiple usb devices connected to Linux system ?
1. Firstly, to open the location the udev-rules located locations
   
   Terminal:
   
   **_$ cd /etc/udev/rules.d/_**
   
3. Next, in that directory we can now copy the **udev.rules** file in the github directory into the above location.
   
   **OR**

   You could make a udev.rules file in the directory and copy the script from the **udev.rules** file in the github directory
   

   Terminal:
   
   **_$ sudo nano udev.rules_**

   **Note:** The above command creates and opens a file called udev.rules inside /etc/udev/rules.d folder.
   
   
   When you type **ls** in your **/etc/udev/rules.d/** directory it should have the **udev.rules** file
   

5. We can then save the created udev rule file by running reload and restart commands.

    Terminal:
    
    **_$ sudo service udev reload_**
   
   **_$ sudo service udev restart_**

6. Finally, plug in the all external devices(GPS,VESC) to USB port of system.

   Terminal:
   
   _$ ls /dev/tty*_
   
   You should be able to see the **/dev/ttyGPS** and **/dev/ttyVESC** set.
