# IoT-agriculture
IoT based agriculture automatic system

# RaspberryPi Setting

1. user: pi
2. password: Taif@123 default: raspberry
3. ip: raspberrypi
4. ping raspberrypi.local

ssh: ``ssh pi@raspberrypi``

Steps to Follow-on setting up the RaspberryPi

1. Update and upgrade
   1. ```shell
       sudo apt-get update -y
      ```
   2. ```shell
       sudo apt-get upgrade -y
      ```
      
2. Install git and setup profile
   1. ```shell
        sudo apt install git -y
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

4. Install package
   1. ```shell
        sudo apt install python3-pip -y
      
        sudo apt-get install pigpio python-pigpio python3-pigpio
      
        sudo pigpiod
      ```
   2. Install package
      1. ```shell
           git clone https://github.com/adafruit/Adafruit_Python_DHT.git
         
           cd ~/Adafruit_Python_DHT
         
           sudo apt-get update
         
           sudo apt-get install build-essential python-dev
         
           sudo python setup.py install
         ```

5. Install all the required packages.
   1. Run the command in the repository folder
   
   2. ```shell
         pip install -r requirements.txt 
      ```

6. Run the following command to install the ``iot_agriculture`` package
    ```shell
      python setup.py install
    ```

7. Change the configurations in config folder as per the requirement 

8. Install the cron
   1. ```shell
         sudo apt-get install cron
      ```
   2. ```shell
        crontab /home/pi/IoT-agriculture/host/respberry/cron
      ```
9. Start the script for the pi
   1. ```shell
         python run.py raspberrypi
      ```
      

# AWS server setting

ip: 3.110.166.9

Open port 8080 on aws server


1. Update and upgrade
   1. ```shell
       sudo apt-get update -y
      ```
   2. ```shell
       sudo apt-get upgrade -y
      
      sudo apt install libpq-dev python3-dev
      ```
      
2. Install git and setup profile
   1. ```shell
      sudo apt install git -y
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
   
6. Install postgres
   1. ```shell
         sudo apt install postgresql postgresql-contrib -y
      ```
   
   2. Switch user
      ```shell
         sudo -i -u postgres
         
         psql
      ```
   
   3. Setpassword
      ```shell
         ALTER USER postgres PASSWORD '<new-password>';
      ```
      
7. Run the server code
   1. ```shell
         nohup python3 run.py server >> /tmp/server.nohup.out;
      ```



# Data base setting
1. host: localhost
2. port: 5432
3. user: postgres
4. password: Taif@123
5. database: iot_data

psql script

```sql

CREATE DATABASE iot_data;

\c iot_data

CREATE TABLE IF NOT EXISTS sensor_data (
	client_id character varying(15) COLLATE pg_catalog."default",
	light BOOLEAN,
	water BOOLEAN,
	time timestamp NOT NULL,
	last_water timestamp NOT NULL	
);

```