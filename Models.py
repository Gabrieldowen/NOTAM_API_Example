class Notam:
    def __init__(self, data):
        self.id = data.get('id', None)
        self.series = data.get('series', None)
        self.number = data.get('number', None)
        self.type = data.get('type', None)
        self.issued = data.get('issued', None)
        self.affectedFIR = data.get('affectedFIR', None)
        self.selectionCode = data.get('selectionCode', None)
        self.traffic = data.get('traffic', None)
        self.purpose = data.get('purpose', None)
        self.scope = data.get('scope', None)
        self.minimumFL = data.get('minimumFL', None)
        self.maximumFL = data.get('maximumFL', None)
        self.location = data.get('location', None)
        self.effectiveStart = data.get('effectiveStart', None)
        self.effectiveEnd = data.get('effectiveEnd', None)
        self.text = data.get('text', None)
        self.translatedText = None
        self.classification = data.get('classification', None)
        self.accountId = data.get('accountId', None)
        self.lastUpdated = data.get('lastUpdated', None)
        self.icaoLocation = data.get('icaoLocation', None)
        self.coordinates = data.get('coordinates', None)
        self.radius = data.get('radius', None)
    
    def to_dict(self):
        return {
            'id': self.id,
            'series': self.series,
            'number': self.number,
            'type': self.type,
            'issued': self.issued,
            'affectedFIR': self.affectedFIR,
            'selectionCode': self.selectionCode,
            'traffic': self.traffic,
            'purpose': self.purpose,
            'scope': self.scope,
            'minimumFL': self.minimumFL,
            'maximumFL': self.maximumFL,
            'location': self.location,
            'effectiveStart': self.effectiveStart,
            'effectiveEnd': self.effectiveEnd,
            'text': self.text,
            'classification': self.classification,
            'accountId': self.accountId,
            'lastUpdated': self.lastUpdated,
            'icaoLocation': self.icaoLocation,
            'coordinates': self.coordinates,
            'radius': self.radius
        }

class NotamRequest:
    def __init__(self, data):
        self.startAirport = data.get('startAirport', None)
        self.destAirport = data.get('destAirport', None)
        self.destinations = []
        index = 2
        while f'destinationLocation{index}' in data:
            self.destinations.append( data.get(f'destinationLocation{index}') )
            index += 1
        self.responseFormat = data.get('responseFormat', None)
        self.effectiveStartDate =  data.get('effectiveStartDate', None)
        self.effectiveEndDate =  data.get('effectiveEndDate', None)
        self.startLong =  data.get('startLong', None)
        self.startLat =  data.get('startLat', None)
        self.destLong =  data.get('destLong', None)
        self.destLat =  data.get('destLat', None)
        self.sortBy =  data.get('sortBy', None)
        self.sortOrder =  data.get('sortOrder', None)
        self.radius = int(data.get('radius', 100)) if data.get('radius', None) is not None and data.get('radius', '') != '' else 100
        self.pathWidth = int(data.get('pathWidth', 50)) if data.get('pathWidth', None) is not None and data.get('pathWidth', '') != '' else 50
