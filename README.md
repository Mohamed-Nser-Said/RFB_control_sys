# Redox Flow Battery Control GUI


![](https://github.com/Mohamed-Nser-Said/RFB_control_sys/blob/master/main_simple_ui/icons/manimage.png)

  > ### This project aims to provide a full operation system, this project is a combination of hardware and software, a python code will be used as a controlling software.

---
<img src="https://github.com/Mohamed-Nser-Said/RFB_control_sys/blob/master/main_simple_ui/icons/pumpgui3.jpg" alt="gui" width="450"/>

---

### Table of Contents
* Description
* Start
* required packages
* Hardware
* GUI


---
* ## Description 

   This is the source code for the [`redox flow battery`](https://en.wikipedia.org/wiki/Flow_battery) `GUI,,
  the `GUI` is built using python version of `Qt5`  [**`pyside2`**](https://doc.qt.io/qtforpython/index.html), the system consists
   of the `cell itself`, `Shenchen Peristaltic Pump`,
  [`Keithley Instruments Model 2450`](https://download.tek.com/manual/2450-900-01_D_May_2015_User_3.pdf) and
  [NI6001](http://deeea.urv.cat/deeea/images/laboratoris/manuals/ni_usb_6001_users_guide.pdf). the `GUI` provide speed control, start/stop, and direction, the program handels all requied Modbus communication via usb port.   
---
* ## Start
    after downloading the repository, run the __main__ python file which contain the main GUI.
---
* ## Packages

Package        | Version
---------------|-------
numpy           |1.19.5|
pandas          |1.2.0|
PyQt5           |5.15.2|
pyqtgraph       |0.11.1|
pyserial        |3.5|
PySide2         |5.15.2|

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
     the National Instruments USB-6001/6002/6003 data acquisition '(DAQ) devices'. The NI-DAQmx Python where used, nidaqmx can be installed with pip:
    
    $ python -m pip install nidaqmx,
     
    [for more information](https://nidaqmx-python.readthedocs.io/en/latest/)

---

  * ### GUI
    the GUI was built using PySide2 module which is Qt for Python,
    
    get PySide2 via pip by running: pip install PySide2.
    
    [for more information](https://wiki.qt.io/Qt_for_Python)
    
       **Main Dashboard** 
 





  |<img src="https://github.com/Mohamed-Nser-Said/RFB_control_sys/blob/master/main_simple_ui/icons/pumpgui1.jpg" alt="gui" width="200"/>)|<img src="https://github.com/Mohamed-Nser-Said/RFB_control_sys/blob/master/main_simple_ui/icons/pumpgui3.jpg" alt="gui" width="200"/>|
  |<img src="https://github.com/Mohamed-Nser-Said/RFB_control_sys/blob/master/main_simple_ui/icons/pumpgui2.jpg" alt="gui" width="200"/>|<img src="https://github.com/Mohamed-Nser-Said/RFB_control_sys/blob/master/main_simple_ui/icons/pumpgui4.jpg" alt="gui" width="200"/>|
  |--------------|---------------|

  

    
    
    
    
 




---
   


