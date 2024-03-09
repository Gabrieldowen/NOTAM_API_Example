import Models
import json

#This function takes an array of NOTAMs and the desired classification type (INTL, DOM, MIL, etc.)
#currently this function just prints the NOTAMs with the desired classification type to a file (ClassificationTesting) but will change later
#can call from app.py with ex: printClassificationToFile(Notams, "INTL") if you include: from NOTAMType import printClassificationToFile
def printClassificationToFile(notams, classificationType):
    arrayOfNotamsWithClassificationType = []

    for notam in notams:
       if notam.classification == classificationType:
           arrayOfNotamsWithClassificationType.append(notam)


    with open('ClassificationTesting', 'w') as file:
        for notam in arrayOfNotamsWithClassificationType:
            file.write(str(notam.classification))
            file.write("    Notam ID: ")
            file.write(str(notam.id))
            file.write("\n")

    return arrayOfNotamsWithClassificationType