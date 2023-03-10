# Navigation:
- put stuff here
  
# ISS Complete Tracking
This homework contains the script ``iss_tracker.py``. This script is a flask application that is used to return data from the iss trajectory data. The data returned is explained in the sections below.

***iss_tracker.py***
- This flask app contains functions that are called when queries are sent to the running app, therefore returning values that were requested. The functions are ``data()``, ``epoch_data()``, ``specific_epoch_data()``, and ``calculate_epoch_speed()``.
> The functions correspond to the queries down below, respectively.

# Image Handling
## Pulling the image ```jaeestee/iss_tracker``` from Docker Hub:
To pull the existing image, run this command:
```bash
$ docker pull jaeestee/iss_tracker:hw05
```
If done properly, ``jaeestee/iss_tracker`` should show up with the tag ``hw05`` when running this command:
```bash
$ docker images
```
> The output should look similar to this:
> ```
> REPOSITORY             TAG       IMAGE ID       CREATED         SIZE
> jaeestee/iss_tracker   hw05      d8276d24fa21   2 hours ago     897MB
> ```

## Running the image:
To start running the containerized Flask app, run this command:
```bash
docker run -it --rm -p 5000:5000 jaeestee/iss_tracker:hw05
```
If done properly, the output should look similar to this:
```
 * Serving Flask app 'iss_tracker'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.17.0.2:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 953-963-822
```
Now the app is running!
> **IMPORTANT: Have this running on a separate window and keep it running while sending queries!!!**

## Building a New Image:
To build a new image from the **Dockerfile** present in this directory, run this command:
```
$ docker build -t <dockerhubusername>/iss_tracker:<version> .
```
> **IMPORTANT: Make sure to be in the same directory as the ``Dockerfile`` and DO NOT FORGET THE "." at the very end of this command!!!**

If done properly, the output should look similar to this:
```
Sending build context to Docker daemon  10.24kB
Step 1/6 : FROM python:3.8.10
 ---> a369814a9797
Step 2/6 : RUN pip install Flask==2.2.2
 ---> Using cache
 ---> bbf69ba6f74f
Step 3/6 : RUN pip install requests==2.22.0
 ---> Using cache
 ---> 9cccc52676f6
Step 4/6 : RUN pip install xmltodict==0.13.0
 ---> Using cache
 ---> 3813629386c4
Step 5/6 : COPY iss_tracker.py /iss_tracker.py
 ---> Using cache
 ---> 071d505247d6
Step 6/6 : CMD ["python", "iss_tracker.py"]
 ---> Using cache
 ---> d8276d24fa21
Successfully built d8276d24fa21
Successfully tagged jaeestee/iss_tracker:test
```
Now you have successfully created your own image!

# Queries To Use While The App is Running:
## To print the entire data set, run this command:
```bash
$ curl localhost:5000/
```
> This will send a get request using curl to the app that should be running.
If done properly (**WITH THE APP RUNNING**), the end of the output should look similar to this:
```
"metadata": {
            "CENTER_NAME": "EARTH",
            "OBJECT_ID": "1998-067-A",
            "OBJECT_NAME": "ISS",
            "REF_FRAME": "EME2000",
            "START_TIME": "2023-048T12:00:00.000Z",
            "STOP_TIME": "2023-063T12:00:00.000Z",
            "TIME_SYSTEM": "UTC"
          }
        }
      },
      "header": {
        "CREATION_DATE": "2023-049T01:38:49.191Z",
        "ORIGINATOR": "JSC"
      }
    }
  }
}
```
> This will print out the entire data set, but as long as you see the metadata section, it printed everything properly.

## To print out a list of all Epochs in the data set, run this command:
```bash
$ curl localhost:5000/epochs
```
If done properly, the end of the output should look similar to this:
```
"EPOCH": "2023-063T12:00:00.000Z",
    "X": {
      "#text": "2820.04422055639",
      "@units": "km"
    },
    "X_DOT": {
      "#text": "5.0375825820999403",
      "@units": "km/s"
    },
    "Y": {
      "#text": "-5957.89709645725",
      "@units": "km"
    },
    "Y_DOT": {
      "#text": "0.78494316057540003",
      "@units": "km/s"
    },
    "Z": {
      "#text": "1652.0698653803699",
      "@units": "km"
    },
    "Z_DOT": {
      "#text": "-5.7191913150960803",
      "@units": "km/s"
    }
  }
]
```
> It is also possible to use the query parameters ``limit`` and ``offset``:
> ```
> $ curl localhost:5000/epochs?limit=<int>'&'offset=<int>
> ```
> where limit prints out a specific number of Epochs and offset changes the starting point.

## To print a specific Epoch, run this command:
```bash
$ curl localhost:5000/epochs/epochKey
```
> Make sure to replace the epochKey with a specific Epoch as shown below:
> ```bash
> $ curl localhost:5000/epochs/2023-063T12:00:00.000Z
> ```
If done properly, the output should look similar to this:
```
{
  "EPOCH": "2023-063T12:00:00.000Z",
  "X": {
    "#text": "2820.04422055639",
    "@units": "km"
  },
  "X_DOT": {
    "#text": "5.0375825820999403",
    "@units": "km/s"
  },
  "Y": {
    "#text": "-5957.89709645725",
    "@units": "km"
  },
  "Y_DOT": {
    "#text": "0.78494316057540003",
    "@units": "km/s"
  },
  "Z": {
    "#text": "1652.0698653803699",
    "@units": "km"
  },
  "Z_DOT": {
    "#text": "-5.7191913150960803",
    "@units": "km/s"
  }
}
```

## To print the speed of a specific Epoch, run this command:
```bash
$ curl localhost:5000/epochs/2023-063T12:00:00.000Z/speed
```
If done properly, the output should look similar to this:
```
Speed: 7.661757196327827 km/s
```

# Describing the ISS Data:
An Epoch is simply a point in time that the ISS is at. It is represented in 3D cartesian coordinates (X, Y, and Z components), as well the corresponding vector components (X_DOT, Y_DOT, and Z_DOT). The units of the coordinates are kilometers, while the vector components are in kilometers per second. Lastly, the Epoch Key (example: 2023-063T12:00:00.000Z) represents the year, date, and time, in that exact order.
> From the [NASA ISS Trajectory Data Website](https://spotthestation.nasa.gov/trajectory_data.cfm)
