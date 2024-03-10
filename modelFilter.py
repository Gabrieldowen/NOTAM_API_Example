from MinimalCirclesPath import getPath, getDistance

def is_notam_relevant(notam, path, pathWidth):
    """
    Check if a NOTAM is relevant based on its location relative to the flight path.
    
    Parameters:
    - notam: A Notam object.
    - path: A list of tuples, each representing a latitude and longitude on the flight path.
    - pathWidth: The width of the flight path corridor.
    
    Returns:
    - True if the NOTAM is within any of the path's circles, False otherwise.
    """
    for point in path:
        if getDistance(notam.coordinates[0], notam.coordinates[1], point[0], point[1]) <= pathWidth / 2:
            return True
    return False

def filter_notams_by_path(notams, startLat, startLong, destLat, destLong, radius, pathWidth):
    """
    Filter NOTAMs to include only those that fall within the flight path.
    
    Parameters:
    - notams: A list of Notam objects.
    - startLat, startLong: The latitude and longitude of the start airport.
    - destLat, destLong: The latitude and longitude of the destination airport.
    - radius: The radius for NOTAM relevance along the path.
    - pathWidth: The width of the flight path corridor.
    
    Returns:
    - A list of Notam objects that are relevant to the flight path.
    """
    path = getPath(startLat, startLong, destLat, destLong, radius, pathWidth)
    relevant_notams = [notam for notam in notams if is_notam_relevant(notam, path, pathWidth)]
    return relevant_notams
