import json
import Models

def ParseNOTAM(apiOutput=None):
    if apiOutput is None:
        print("*********************\n USING TEST DATA \n*********************")
        # File path where the test JSON data is saved
        file_path = "static/TestData/TestNOTAM.json"

        # Reading test JSON data from the file
        with open(file_path, 'r') as json_file:
            apiOutput = json.load(json_file)

    NOTAMs = []
    seen_notam_ids = set()  # Set to track the IDs of NOTAMs already processed

    try:
        for notam in apiOutput:
            if 'items' in notam:
                for item in notam['items']:
                    try:
                        core_notam_data = item.get('properties', {}).get('coreNOTAMData', {}).get('notam')
                        if core_notam_data:
                            # Check if the NOTAM ID is already seen
                            notam_id = core_notam_data.get('id')
                            if notam_id and notam_id not in seen_notam_ids:
                                NOTAMs.append(Models.Notam(core_notam_data))
                                seen_notam_ids.add(notam_id)  # Mark this NOTAM ID as seen
                            else:
                                print(f"Duplicate NOTAM skipped: {notam_id}")
                        else:
                            print("Warning: NOTAM missing coreNOTAMData")
                    except Exception as e:
                        print(f"Error processing item: {e}")
            else:
                print(f"Warning: 'items' key missing in notam: {notam}")
    except Exception as e:
        print(f"Error occurred: {e}")

    #assign_color_to_notam(NOTAMs)
    return NOTAMs


def assign_color_to_notam(notams):
    for notam in notams:
        # Go through every notam and look for key words to assign color value
        if 'LGT' in notam.text or 'MKR' in notam.text or 'MARKINGS' in notam.text or 'LIGHTING' in notam.text or 'OBST' in notam.text:
            notam.color = '#ffd966' # yellow
            print(notam.id + "is yellow")

        elif 'CLSD' in notam.text:
            notam.color = '#ff7f7f' # red
            print(notam.id + "is red")

        else:
            notam.color = '#bad4b7' # green

    

if __name__ == '__main__':
    NOTAMs = ParseNOTAM()
    print(NOTAMs)
