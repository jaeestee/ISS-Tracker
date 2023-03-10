# Navigation:
- [ISS Complete Tracking](https://github.com/jaeestee/ISS-Tracker/blob/main/README.md#iss-complete-tracking)
- [Image Handling](https://github.com/jaeestee/ISS-Tracker/blob/main/README.md#image-handling)
  - [Pulling the Image](https://github.com/jaeestee/ISS-Tracker/blob/main/README.md#pulling-the-image-jaeesteeiss_tracker-from-docker-hub)
  - [Running the Image](https://github.com/jaeestee/ISS-Tracker/blob/main/README.md#running-the-image)
  - [Building a New Image](https://github.com/jaeestee/ISS-Tracker/blob/main/README.md#building-a-new-image)
- [Queries to Use](https://github.com/jaeestee/ISS-Tracker/blob/main/README.md#queries-to-use-while-the-app-is-running)
  - [Load/Reload Data](https://github.com/jaeestee/ISS-Tracker/blob/main/README.md#to-loadreload-the-data-run-this-command)
  - [Delete Data](https://github.com/jaeestee/ISS-Tracker/blob/main/README.md#to-delete-the-data-run-this-command)
  - [Print Entire Data](https://github.com/jaeestee/ISS-Tracker/blob/main/README.md#to-print-the-entire-data-set-whether-it-exists-or-is-empty-run-this-command)
  - [Print Comments](https://github.com/jaeestee/ISS-Tracker/blob/main/README.md#to-print-the-comments-in-the-data-run-this-command)
  - [Print Header](https://github.com/jaeestee/ISS-Tracker/blob/main/README.md#to-print-the-header-in-the-data-run-this-command)
  - [Print Metadata](https://github.com/jaeestee/ISS-Tracker/blob/main/README.md#to-print-the-metadata-in-the-data-run-this-command)
  - [Print Current ISS Location](https://github.com/jaeestee/ISS-Tracker/blob/main/README.md#to-print-the-current-location-of-the-iss-run-this-command)
  - [Print List of Epochs](https://github.com/jaeestee/ISS-Tracker/blob/main/README.md#to-print-out-a-list-of-all-epochs-in-the-data-set-run-this-command)
  - [Print Specific Epoch](https://github.com/jaeestee/ISS-Tracker/blob/main/README.md#to-print-a-specific-epoch-run-this-command)
  - [Print Location of Specific Epoch](https://github.com/jaeestee/ISS-Tracker/blob/main/README.md#to-print-the-location-of-a-specific-epoch-run-this-command)
  - [Print Speed of Specific Epoch](https://github.com/jaeestee/ISS-Tracker/blob/main/README.md#to-print-the-speed-of-a-specific-epoch-run-this-command)
- [Desribing the ISS Data](https://github.com/jaeestee/ISS-Tracker/blob/main/README.md#describing-the-iss-data)
  
# ISS Complete Tracking
This homework contains the script ``iss_tracker.py``. This script is a flask application that is used to return data from the iss trajectory data. The data returned is explained in the sections below.

***iss_tracker.py***
- This flask app contains functions that are called when queries are sent to the running app, therefore returning values that were requested. The functions are:
  - ``delete_data()``, ``post_data()``, ``data()``, ``get_comment()``, ``get_header()``, ``get_metadata()``, ``current_location()``, ``epoch_data()``, ``specific_epoch_data()``, ``location()``, ``calculate_epoch_speed()``, and ``help()``.
> The functions correspond to the queries in the "Queries To Use" section, respectively.

> Back up to [Navigation](https://github.com/jaeestee/ISS-Tracker/blob/main/README.md#navigation)
# Image Handling
## Pulling the image ```jaeestee/iss_tracker``` from Docker Hub:
To pull the existing image, run this command:
```bash
$ docker pull jaeestee/iss_tracker
```
If done properly, ``jaeestee/iss_tracker`` should show up with the tag ``latest`` when running this command:
```bash
$ docker images
```
> The output should look similar to this:
> ```
> REPOSITORY             TAG       IMAGE ID       CREATED         SIZE
> jaeestee/iss_tracker   latest    d8276d24fa21   2 hours ago     897MB
> ```

> Back up to [Navigation](https://github.com/jaeestee/ISS-Tracker/blob/main/README.md#navigation)
## Running the image:
To start running the containerized Flask app, run this command:
```bash
docker-compose up
```
> Remember that the docker-compose.yml file must exist in the same folder for this to work!
If done properly, the output should look similar to this:
```
Starting iss-tracker_flask-app_1 ... done
Attaching to iss-tracker_flask-app_1
flask-app_1  |  * Serving Flask app 'iss_tracker'
flask-app_1  |  * Debug mode: on
flask-app_1  | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
flask-app_1  |  * Running on all addresses (0.0.0.0)
flask-app_1  |  * Running on http://127.0.0.1:5000
flask-app_1  |  * Running on http://172.19.0.2:5000
flask-app_1  | Press CTRL+C to quit
flask-app_1  |  * Restarting with stat
flask-app_1  |  * Debugger is active!
flask-app_1  |  * Debugger PIN: 125-216-670
```
Now the app is running!
> **IMPORTANT: Have this running on a separate window and keep it running while sending queries!!!**

> Back up to [Navigation](https://github.com/jaeestee/ISS-Tracker/blob/main/README.md#navigation)
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

> Back up to [Navigation](https://github.com/jaeestee/ISS-Tracker/blob/main/README.md#navigation)
# Queries To Use While The App is Running:
## To load/reload the data, run this command:
```bash
$ curl localhost:5000/post-data -X POST
```
If done properly, the output should look like this:
```
Successfully reloaded the dictionary with the data from the web!
```

> Back up to [Navigation](https://github.com/jaeestee/ISS-Tracker/blob/main/README.md#navigation)
## To delete the data, run this command:
```bash
$ curl localhost:5000/delete-data -X DELETE
```
If done properly, the output should look like this:
```
Successfully deleted all the data from the dictionary!
```

> Back up to [Navigation](https://github.com/jaeestee/ISS-Tracker/blob/main/README.md#navigation)
## To print the entire data set (whether it exists or is empty), run this command:
```bash
$ curl localhost:5000/
```
> This will send a get request using curl to the app that should be running.

If done properly (**WITH THE APP RUNNING ON A SEPARATE TAB**), the end of the output should look similar to one of these 3 outputs:
- Output possibility 1:
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
- Output possibility 2:

```
The data set does not exist yet!
```
> This means that the POST method has not been called.

- Output possibility 3:
```
{}
```
> This means that the DELETE method was called, emptying the data.

> Back up to [Navigation](https://github.com/jaeestee/ISS-Tracker/blob/main/README.md#navigation)
## To print the comments in the data, run this command:
```bash
$ curl localhost:5000/comment
```
If done properly, the output should look similar to this:
```
[
  "Units are in kg and m^2",
  "MASS=473291.00",
  "DRAG_AREA=1421.50",
  "DRAG_COEFF=2.80",
  "SOLAR_RAD_AREA=0.00",
  "SOLAR_RAD_COEFF=0.00",
  "Orbits start at the ascending node epoch",
  "ISS first asc. node: EPOCH = 2023-03-08T12:50:10.295 $ ORBIT = 2617 $ LAN(DEG) = 108.61247",
  "ISS last asc. node : EPOCH = 2023-03-23T11:58:44.947 $ ORBIT = 2849 $ LAN(DEG) = 32.65474",
  "Begin sequence of events",
  "TRAJECTORY EVENT SUMMARY:",
  null,
  "|       EVENT        |       TIG        | ORB |   DV    |   HA    |   HP    |",
  "|                    |       GMT        |     |   M/S   |   KM    |   KM    |",
  "|                    |                  |     |  (F/S)  |  (NM)   |  (NM)   |",
  "=============================================================================",
  "GMT067 Reboost        067:19:47:00.000             0.6     428.1     408.4",
  "(2.0)   (231.1)   (220.5)",
  null,
  "Crew05 Undock         068:22:00:00.000             0.0     428.7     409.6",
  "(0.0)   (231.5)   (221.2)",
  null,
  "SpX27 Launch          074:00:30:00.000             0.0     428.3     408.7",
  "(0.0)   (231.2)   (220.7)",
  null,
  "SpX27 Docking         075:12:00:00.000             0.0     428.2     408.6",
  "(0.0)   (231.2)   (220.6)",
  null,
  "=============================================================================",
  "End sequence of events"
]
```
> A message will appear if the data is empty or doesn't exist yet.

> Back up to [Navigation](https://github.com/jaeestee/ISS-Tracker/blob/main/README.md#navigation)
## To print the header in the data, run this command:
```bash
$ curl localhost:5000/header
```
If done properly, the output should look similar to this:
```
{
  "CREATION_DATE": "2023-067T21:02:49.080Z",
  "ORIGINATOR": "JSC"
}
```
> A message will appear if the data is empty or doesn't exist yet.

> Back up to [Navigation](https://github.com/jaeestee/ISS-Tracker/blob/main/README.md#navigation)
## To print the metadata in the data, run this command:
```bash
$ curl localhost:5000/metadata
```
If done properly, the output should look similar to this:
```
{
  "CENTER_NAME": "EARTH",
  "OBJECT_ID": "1998-067-A",
  "OBJECT_NAME": "ISS",
  "REF_FRAME": "EME2000",
  "START_TIME": "2023-067T12:00:00.000Z",
  "STOP_TIME": "2023-082T12:00:00.000Z",
  "TIME_SYSTEM": "UTC"
}
```
> A message will appear if the data is empty or doesn't exist yet.

> Back up to [Navigation](https://github.com/jaeestee/ISS-Tracker/blob/main/README.md#navigation)
## To print the current location of the ISS, run this command:
```bash
$ curl localhost:5000/now
```
If done properly, the output should look similar to this:
```
{
  "Epoch": "2023-069T06:48:00.000Z",
  "Location": {
    "altitude": {
      "units": "km",
      "value": 419.7851549137822
    },
    "latitude": 28.659367107265545,
    "longitude": -126.3121600929075
  },
  "geo": "The ISS must be over an ocean...",
  "speed": {
    "units": "km/s",
    "value": 7.666292075028554
  }
}
```
> A message will appear if the data is empty or doesn't exist yet.

> You can use this website, [ISS Real Time Tracker](https://www.n2yo.com/?s=90027), to check that the latitude and longitude given in the output is similar to the latitude and longitude of the website's tracker.

> Back up to [Navigation](https://github.com/jaeestee/ISS-Tracker/blob/main/README.md#navigation)
## To print out a list of all Epochs in the data set, run this command:
```bash
$ curl localhost:5000/epochs
```
If done properly, the end of the output should look similar to this:
```
  "2023-082T11:20:00.000Z",
  "2023-082T11:24:00.000Z",
  "2023-082T11:28:00.000Z",
  "2023-082T11:32:00.000Z",
  "2023-082T11:36:00.000Z",
  "2023-082T11:40:00.000Z",
  "2023-082T11:44:00.000Z",
  "2023-082T11:48:00.000Z",
  "2023-082T11:52:00.000Z",
  "2023-082T11:56:00.000Z",
  "2023-082T12:00:00.000Z"
]
```
> A message will appear if the data is empty or doesn't exist yet. Additionally, there should be a lot more data points, this is a shortened version.

> It is also possible to use the query parameters ``limit`` and ``offset``:
> ```
> $ curl localhost:5000/epochs?limit=<int>'&'offset=<int>
> ```
> where limit prints out a specific number of Epochs and offset changes the starting point.

> Back up to [Navigation](https://github.com/jaeestee/ISS-Tracker/blob/main/README.md#navigation)
## To print a specific Epoch, run this command:
```bash
$ curl localhost:5000/epochs/<epochKey>
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
> A message will appear if the data is empty or doesn't exist yet.

> Back up to [Navigation](https://github.com/jaeestee/ISS-Tracker/blob/main/README.md#navigation)
## To print the location of a specific Epoch, run this command:
```bash
$ curl localhost:5000/epochs/2023-063T12:00:00.000Z/location
```
If done properly, the output should look similar to this:
```
{
  "Epoch": "2023-082T12:00:00.000Z",
  "Location": {
    "altitude": {
      "units": "km",
      "value": 426.493361256541
    },
    "latitude": 3.693612400678767,
    "longitude": 67.77071661260686
  },
  "geo": "The ISS must be over an ocean...",
  "speed": {
    "units": "km/s",
    "value": 7.6603442162552815
  }
}
```
> A message will appear if the data is empty or doesn't exist yet.

> Back up to [Navigation](https://github.com/jaeestee/ISS-Tracker/blob/main/README.md#navigation)
## To print the speed of a specific Epoch, run this command:
```bash
$ curl localhost:5000/epochs/2023-063T12:00:00.000Z/speed
```
If done properly, the output should look similar to this:
```
{
  "speed": {
    "units": "km/s",
    "value": 7.6603442162552815
  }
}
```
> A message will appear if the data is empty or doesn't exist yet.

# Describing the ISS Data:
An Epoch is simply a point in time that the ISS is at. It is represented in 3D cartesian coordinates (X, Y, and Z components), as well the corresponding vector components (X_DOT, Y_DOT, and Z_DOT). The units of the coordinates are kilometers, while the vector components are in kilometers per second. Lastly, the Epoch Key (example: 2023-063T12:00:00.000Z) represents the year, date, and time, in that exact order.
> From the [NASA ISS Trajectory Data Website](https://spotthestation.nasa.gov/trajectory_data.cfm)
  
> Back up to [Navigation](https://github.com/jaeestee/ISS-Tracker/blob/main/README.md#navigation)
