# IoT-agriculture
IoT based agriculture automatic system

# RaspberryPi Setting

1. user: pi
2. password: Taif@123 default: raspberry
3. ip: raspberrypi

ssh: ``ssh pi@raspberrypi``

Steps to Follow-on setting up the RaspberryPi

1. Update and upgrade
   1. ```shell
       sudo apt-get update 
      ```
   2. ```shell
       sudo apt-get upgrade
      ```
      
2. Install git and setup profile
   1. ```shell
      sudo apt install git
      ```
   
   Set up the profile
   2. ```shell
      git config --global user.name "Your Name"
      
      git config --global user.email "youremail@domain.com"
      
      git config --global user.password "your password"
      ```
      
3. Pull the code
   1. ```shell
       cd ~
       
       git clone https://github.com/TaifQureshi/IoT-agriculture.git      
      ```

4. Install all the required packages.
   1. Run the command in the repository folder
   
   2. ```shell
         pip install -r requirements.txt 
      ```

5. Run the following command to install the ``iot_agriculture`` package
    ```shell
      python setup.py install
    ```

6. Change the configurations in config folder as per the requirement 

7. Install the cron
   1. ```shell
         sudo apt-get install cron
      ```
   2. ```shell
        crontab /home/pi/IoT-agriculture/host/respberry/cron
      ```
8. Start the script for the pi
   1. ```shell
         python run.py raspberrypi
      ```
      

# AWS server setting