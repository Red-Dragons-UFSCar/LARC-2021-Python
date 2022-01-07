# FIRASim

The simulator [repository](https://github.com/IEEEVSS/FIRASim) constains some install instructions, you can follow them here as well for the simplified version

 Install the dependencies:
 ```sh
 $ sudo apt-get install git build-essential cmake qt5-default libqt5opengl5-dev libgl1-mesa-dev libglu1-mesa-dev libprotobuf-dev protobuf-compiler libode-dev libboost-dev
 ```

 Clone into FIRASim:
 ```sh
 $ git clone https://github.com/IEEEVSS/FIRASim
 $ cd FIRASim
 ```

 Create a build directory:
 ```sh
 $ mkdir build
 $ cd build
 ```

 Compile:
 ```sh
 $ cmake ..
 $ make
 ```

Now you should be able to run the simulator:

 ```sh
 $ cd ..
 $ ./bin/FIRASim
 ```

# VSSSReferee

The referee repository can be found [here](https://github.com/VSSSLeague/VSSReferee)

 Clone into VSSReferee repository:
 ```sh
 $ git clone https://github.com/VSSSLeague/VSSReferee.git
 cd VSSReferee
 ```

 Make a build directory
 ```sh
 $ mkdir build
 $ cd build
 ```

 Compile:
 ```sh
 $ qmake ..
 $ make
 ```

 Now you can run the referee program for 3v3 category:
 ```
 $ cd ..
 $ ./bin/VSSReferee --3v3
 ```

 However, if the desired category is 5v5, you should run:
 ```
 $ ./bin/VSSReferee --5v5
 ```
