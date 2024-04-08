from Models import Notam, NotamRequest
import re
import ParseNOTAM
import GetNOTAM
import time

"""
Keep the NOTAM that announces the runway closure.
Remove any subsequent NOTAMs that are related to the closed runway, as they would be redundant.
These could include NOTAMs about lighting, navigational aids, and other services that are implicitly not available due to the runway being closed.

"""

def extract_closed_runways(notams):
    """Extract a set of identifiers for closed runways from a list of NOTAMs."""
    closed_runways = set()
    for notam in notams:
        if 'CLSD' in notam.text:
            # Extract the runway identifier
            parts = notam.text.split()
            for i, part in enumerate(parts):
                if part == 'RWY' and i+1 < len(parts):
                    # Assume the next part is the runway identifier
                    closed_runways.add(parts[i+1])
    return closed_runways

def filter_notams(notams, closed_runways):
    """Filter out NOTAMs that relate to any of the closed runways."""
    filtered_notams = []
    for notam in notams:
        if not any(closed_runway in notam.text for closed_runway in closed_runways):
            filtered_notams.append(notam)
    return filtered_notams


"""
    Remove all NOTAMs related to obstacles. Such NOTAMs typically describe temporary
    structures or equipment that may penetrate navigable airspace but are not always
    significant for aircraft operating at standard flight levels, especially for IFR pilots.
"""
def filter_out_obstacle_notams(notams):
    return [notam for notam in notams if "OBST" not in notam.text]

"""
    Retain NOTAMs for obstacles exceeding a specified height threshold. High obstacles
    could present a risk to aircraft during critical phases of flight like approach or departure
    and are therefore significant enough to be considered in flight planning.
"""

# This function will keep NOTAMs with obstacles higher than a certain height.
def filter_keep_high_obstacle_notams(notams, height_threshold=500):
    high_obstacle_notams = []
    for notam in notams:
        if "OBST" in notam.text:
            # Search for height information in the NOTAM text
            match = re.search(r'(\d+)\s?FT', notam.text)
            if match:
                # Convert the captured height to an integer
                height = int(match.group(1))
                if height > height_threshold:
                    high_obstacle_notams.append(notam)
    return high_obstacle_notams

"""
    Identify NOTAMs related to non-standard airport lighting or markings. Variations from
    standard lighting and markings are often not critical to the operations of larger aircraft
    or those under IFR, and such NOTAMs can typically be disregarded to focus on more
    pertinent flight information.
"""

def identify_lighting_marking_notams(notams):
    marked_notams = set()
    for notam in notams:
        if 'LGT' in notam.text or 'MKR' in notam.text or 'MARKINGS' in notam.text or 'LIGHTING' in notam.text:
            marked_notams.add(notam)
    return marked_notams

# This function will filter out NOTAMs that have been marked as lighting or marking NOTAMs.
def filter_out_lighting_marking_notams(notams, marked_notams):
    return [notam for notam in notams if notam not in marked_notams]

def filter_classification(notams, classification):
    marked_notams = set()
    for notam in notams:
        if classification in notam.classification:
            marked_notams.add(notam)
    return marked_notams

def filter_out_classification(notams, classification):
    marked_notams = filter_classification(notams, classification)
    return [notam for notam in notams if notam not in marked_notams]

def filter_keyword(notams, keyword):
    marked_notams = set()
    for notam in notams:
        if keyword in notam.text:
            marked_notams.add(notam)
    return marked_notams

def filter_out_keyword(notams, keyword):
    marked_notams = filter_classification(notams, keyword)
    return [notam for notam in notams if notam not in marked_notams]