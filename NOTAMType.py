import Models
import json

#This function takes an array of NOTAMs and the desired classification type (INTL, DOM, MIL, etc.)
#currently this function just prints the NOTAMs with the desired classification type to a file (ClassificationTesting) but will change later
def printClassification(notams, classificationType):
    arrayOfNotamsWithClassificationType = []

    for notam in notams:
       if notam.classification == classificationType:
           arrayOfNotamsWithClassificationType.append(notam)


    with open('ClassificationTesting', 'w') as file:
        for notam in arrayOfNotamsWithClassificationType:
            file.write(str(notam.classification))
            file.write("\n")

    return arrayOfNotamsWithClassificationType