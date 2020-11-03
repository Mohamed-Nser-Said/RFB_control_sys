# Redox Flow Battery Control System


![](https://github.com/Mohamed-Nser-Said/RFB_control_sys/blob/master/QtIcons/battery-charge.png?raw=true)

  > ### This project aims to provide a full operation system, this project is a combination of hardware and software, a python code will be used as a controlling software.

---

### Table of Contents
* Description
* Quick Start
* Hardware
* GUI


---
* ## Description 

   This project aims to provide a full operation system for a [redox flow battery](https://en.wikipedia.org/wiki/Flow_battery),
    the system will be controlled through a GUI,
  the GUI is built using python version of **Qt5**  [**pyside2**](https://doc.qt.io/qtforpython/index.html), the system consists
   of the cell itself, Shenchen Peristaltic Pump,
  [Keithley Instruments Model 2450](https://download.tek.com/manual/2450-900-01_D_May_2015_User_3.pdf) and
  [NI6001](http://deeea.urv.cat/deeea/images/laboratoris/manuals/ni_usb_6001_users_guide.pdf). the documentation will go through
   the basic connection of the hardware and the python code associated with it and the method that has been used,
    however it will not explain the technical part of the Redox Flow battery.   
---
* ## Quick Start
    after downloading the repository, run the ViewDashboard python file which contain the main GUI.
---        

* ## Hardware
  * ### Shenchen Peristaltic Pump
  ![Shenchen Peristaltic Pump](https://www.good-pump.com/uploadfile/load/images/2020/202004/20200407/15/20200407103434z1kzlgic.jpg)
  
  MODBUS-RTU standard communication is used to control the pump, message frame as below：
  
  |Slave address | Function code | Data area         | CRC Check (Cyclic Redundancy Check)   |
  |--------------|---------------|-------------------|---------------------------------------|
  |1 Byte        | 1 Byte        | or up to 252 bytes|     2 Bytes                           |
  |              |               |                   |  CRC low       CRC high               |
  
  **CRC check**: CRC code is 2 bytes, 16 check codes. Use CRC-16(which used in American binary
synchronous system).

    Polynomial: G(X)=X16+X15+X2+1.
---
  * ### Keithley Instruments Model 2450
        
  
---
  * ### NI6001
     the National Instruments USB-6001/6002/6003 data acquisition (DAQ) devices. The NI-DAQmx Python where used, nidaqmx can be installed with pip:
    
    $ python -m pip install nidaqmx,
     
    [for more information](https://nidaqmx-python.readthedocs.io/en/latest/)

---

  * ### GUI
    the GUI was built using PySide2 module which is Qt for Python,
    
    get PySide2 via pip by running: pip install PySide2.
    
    [for more information](https://wiki.qt.io/Qt_for_Python)
    
       **Main Dashboard** 
    ![Main Dashboard](https://github.com/Mohamed-Nser-Said/RFB_control_sys/blob/master/QtIcons/dashboard.png?raw=true)
    
    ![Pump](https://github.com/Mohamed-Nser-Said/RFB_control_sys/blob/master/QtIcons/pumpwidget2.png?raw=true)
    
    ![pump](https://github.com/Mohamed-Nser-Said/RFB_control_sys/blob/master/QtIcons/pumpwidget.png?raw=true)
 




---
   


