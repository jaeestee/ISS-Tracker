from flask import Flask, request
from geopy.geocoders import Nominatim
import requests, xmltodict, math, time

app = Flask(__name__)

@app.route('/delete-data', methods=['DELETE'])
def delete_data() -> str:
    """
    This function deletes the data and replaces the data with a blank dictionary.

    Returns:
        message (str): Message saying that the data was deleted.
    """

    #making DATA a global variable
    global DATA

    #simply setting DATA equal to nothing so that it "deletes" the data
    DATA = {}

    message = 'Successfully deleted all the data from the dictionary!\n'
    return message

@app.route('/post-data', methods=['POST'])
def post_data() -> str:
    """
    This function reloads the DATA dictionary object with the data from the website so that it can always
    use the most updated data set.

    Returns:
        message (str): Message saying that the data was successfully reloaded.
    """

    #making DATA a global variable
    global DATA
    
    #stores the data from the get request into the data variable and converts it into a dictionary
    DATA = requests.get(url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
    DATA = xmltodict.parse(DATA.text)

    message = 'Successfully reloaded the dictionary with the data from the web!\n'
    return message
    
@app.route('/', methods=['GET'])
def data() -> dict:
    """
    This function returns the data in the form of a dictionary. If it hasn't been posted at all yet, it will
    return a message saying that it doesn't exist. If it has been posted, it will print the data and if the
    delete method was called, it will return a blank dictionary.

    Returns:
        data (dict): The entire iss data.
    """

    #try-except block that returns if the data doesn't exist and an error occurs because of it
    try:
        DATA
    except NameError:
        return 'The data set does not exist yet!\n'

    return DATA

@app.route('/comment', methods=['GET'])
def get_comment() -> list:
    """

    """
    #try-except block that makes sure it returns a message if the data is empty or doesn't exist
    try:
        #stores the entire epoch data by navigating through the entire data dictionary
        comment = data()['ndm']['oem']['body']['segment']['data']['COMMENT']
    except TypeError:
        return 'The data set does not exist yet!\n'
    except KeyError:
        return 'The data is empty!\n'

    return comment

@app.route('/header', methods=['GET'])
def get_header() -> dict:
    """

    """
    #try-except block that makes sure it returns a message if the data is empty or doesn't exist
    try:
        #stores the entire epoch data by navigating through the entire data dictionary
        header = data()['ndm']['oem']['header']
    except TypeError:
        return 'The data set does not exist yet!\n'
    except KeyError:
        return 'The data is empty!\n'

    return header

@app.route('/metadata', methods=['GET'])
def get_metadata() -> dict:
    """

    """
    #try-except block that makes sure it returns a message if the data is empty or doesn't exist
    try:
        #stores the entire epoch data by navigating through the entire data dictionary
        metadata = data()['ndm']['oem']['body']['segment']['metadata']
    except TypeError:
        return 'The data set does not exist yet!\n'
    except KeyError:
        return 'The data is empty!\n'

    return metadata

@app.route('/now', methods=['GET'])
def current_location() -> dict:
    """

    """

    listOfEpochs = epoch_data()

    timeNow = time.time()
    timeEpoch = time.mktime(time.strptime(listOfEpochs[0][:-5], '%Y-%jT%H:%M:%S'))
    closestEpoch = listOfEpochs[0]
    previousDifference = abs(timeNow - timeEpoch)
    
    for epoch in listOfEpochs:
        timeEpoch = time.mktime(time.strptime(epoch[:-5], '%Y-%jT%H:%M:%S'))
        difference = abs(timeNow - timeEpoch)
        if difference < previousDifference:
            closestEpoch = epoch
            previousDifference = difference

    return location(closestEpoch)

@app.route('/epochs', methods=['GET'])
def epoch_data() -> list:
    """
    This function calls the get_data() function to retrieve the entire data set and returns the listOfEpochs
    variable. It can take in query parameters of offset and limit which will cause the data to start at a
    different point and limit the amount of data returned.

    Returns:
        results (list): The results from the entire list of Epochs from the iss data considering the offset and
        limit parameters.
    """

    #try-except block that makes sure it returns a message if the data is empty or doesn't exist
    try:
        #stores the entire epoch data by navigating through the entire data dictionary
        listOfEpochs = data()['ndm']['oem']['body']['segment']['data']['stateVector']
    except TypeError:
        return 'The data set does not exist yet!\n'
    except KeyError:
        return 'The data is empty!\n'

    #try and except blocks for the limit and offset variables so that it can only be an integer
    try:
        limit = int(request.args.get('limit', len(listOfEpochs)))
    except ValueError:
        return 'ERROR: Please send an integer for the limit!\n', 400
    try:
        offset = int(request.args.get('offset', 0))
    except ValueError:
        return 'ERROR: Please send an integer for the offset!\n', 400

    #initializing a new blank list to store the "new" data
    results = []

    #for loop that stores the requested Epoch data
    for i in range(limit):
        results.append(listOfEpochs[i+offset]['EPOCH'])
    
    return results

@app.route('/epochs/<string:epoch>', methods=['GET'])
def specific_epoch_data(epoch: str) -> dict:
    """
    This function returns the specific epoch data that was requested by the user.

    Args:
        epoch (str): The specific epoch key to find the requested epoch data.

    Returns:
        epochData (dict): The epoch data for the given epoch key.
    """

    #try-except block to make sure the data has information
    try:
        #stores the list of epochs
        listOfEpochs = data()['ndm']['oem']['body']['segment']['data']['stateVector']
    except TypeError:
        return 'The data seems to be empty or does not exist...\n'

    #shorts through the list to match the epoch key and returns the data for it
    for i in range(len(listOfEpochs)):
        if listOfEpochs[i]['EPOCH'] == epoch:
            return listOfEpochs[i]

    #if it doesn't find it, returns this prompt
    return 'Could not find the epoch for the given key.\n'

@app.route('/epochs/<string:epoch>/location', methods=['GET'])
def location(epoch: str) -> dict:
    """

    """

    specificEpoch = specific_epoch_data(epoch)

    MEAN_EARTH_RADIUS = 6371
    
    try:
        x = float(specificEpoch['X']['#text'])
        y = float(specificEpoch['Y']['#text'])
        z = float(specificEpoch['Z']['#text'])
        units = specificEpoch['X']['@units']
        epoch = specificEpoch['EPOCH']
    except TypeError:
        return 'The data seems to be empty or does not exist...\n'

    hrs = int(epoch[9:11])
    mins = int(epoch[12:14])
    lat = math.degrees(math.atan2(z, math.sqrt(x**2 + y**2)))
    lon = math.degrees(math.atan2(y, x)) - ((hrs-12)+(mins/60))*(360/24) + 32
    alt = math.sqrt(x**2 + y**2 + z**2) - MEAN_EARTH_RADIUS 

    if lat > 180:
        lat = lat - 360
    if lon > 180:
        lon = lon - 360

    geocoder = Nominatim(user_agent='iss_tracker')
    try:
        geoloc = geocoder.reverse((lat, lon), zoom = 10, language = 'en')
    except Error as e:
        return f'Geopy returned an error - {e}\n'

    try:
        geoloc = geoloc.raw
    except AttributeError:
        geoloc = 'The ISS must be over an ocean...'


    speed = calculate_epoch_speed(epoch)['speed']
    
    epochLocation = {'Epoch': epoch, 'Location': {'latitude': lat, 'longitude': lon, 'altitude': {'value': alt, 'units': units}}, 'geo': geoloc, 'speed': speed}
    
    return epochLocation

@app.route('/epochs/<string:epoch>/speed', methods=['GET'])
def calculate_epoch_speed(epoch: str) -> dict:
    """
    This function calculates the speed for the specific epoch and returns it.

    Args:
        epoch (str): The specific epoch key to find the requested epoch data.

    Returns:
        speed (float): The speed for the specific epoch requested.
    """

    #stores the specific epoch using the pre-existing function
    specificEpoch = specific_epoch_data(epoch)

    #try-except block to make sure the data has information
    try:
        specificEpoch['X_DOT']['#text']
    except TypeError:
        return 'Could not calculate the speed of the epoch for the given key.\n'
        
    #stores the X_DOT, Y_DOT, and Z_DOT for the specific epoch into corresponding variables and converts them to float
    xDot = float(specificEpoch['X_DOT']['#text'])
    yDot = float(specificEpoch['Y_DOT']['#text'])
    zDot = float(specificEpoch['Z_DOT']['#text'])

    #the units for the vector
    units = specificEpoch['X_DOT']['@units']
    
    #calculates the speed using the magnitude of a vector formula
    speed = math.sqrt(xDot**2 + yDot**2 + zDot**2)

    output = {'speed': {'value': speed, 'units': units}}
    return output

@app.route('/help', methods=['GET'])
def help() -> str:
    """
    This function returns a human readable string that explains all the available
    routes in this API.

    Returns:
       helpOutput (str): The string that explains the routes.
    """

    helpOutput = '''usage: curl localhost:5000[<route>][?<query parameter>]\n
The different possible routes:
    /                                   Returns the entire data set
    /epochs                             Returns the list of all Epochs in the data set
    /epochs/<epoch>                     Returns the state vectors for a specific Epoch from the data set
    /epochs/<epoch>/speed               Returns the instantaneous speed for a specific Epoch in the data set
    /help                               Returns the help text taht describes each route
    /delete-data                        Deletes all the data from the dictionary
    /post-data                          Reloads the dictionary with data from the website

The different query parameters (only works for the "/epochs" route):
    limit=<int>                         Returns a specific integer amount of Epochs from the data set
    offset=<int>                        Returns the entire data set starting offset by a certain integer amount
    limit=<int>'&'offset=<int>          Combining the limit and offset query parameters

    example:
    /epochs?limit=15'&'offset=3         Returns the 15 Epochs from the data set offset by 3

'''
    
    return helpOutput

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
