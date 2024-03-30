from Models import Notam, NotamRequest
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
