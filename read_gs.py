# pip install oauth2client==1.5.2
# pip install gspread==0.6.2
# pip install cryptography==1.4

import gspread
from oauth2client.client import SignedJwtAssertionCredentials
import json


def get_google_client():
    with open('google_key.json') as f:
        config = json.load(f)

    creds = SignedJwtAssertionCredentials(
        config['client_email'],
        config['private_key'],
        ['https://spreadsheets.google.com/feeds']
    )
    return gspread.authorize(creds)


def process_value(values, name):
    folders = {"Original Experience": "Articles", "Curated Links": "CuratedContent",
               "Event": "Events", "Blog Article": "Site"}
    topic = ""
    for i in range(15, 21):
        if values[i]:
            topic = values[i]
            break
    folder = folders[values[21]]
    fo = open("{}/{}".format(folder, name), "w")
    for i in range(22, 27):
        fo.write(values[i])
    fo.write("\n\n<!---")
    fo.write("\nCategories: {}".format(values[14]))
    fo.write("\nTopic: {}".format(topic))
    fo.write("\nPrerequisites: default")
    fo.write("\n--->")


def run():
    gc = get_google_client()

    # Open file: key in the URL
    doc = gc.open_by_key('1xFi0frEQdLb7a3LPtn8-2zFt2myO5dk15_8soseMkDk')

    # Open tab
    sheet = doc.worksheet("Form Responses 1")

    row_count = sheet.row_count
    for row in range(2, row_count + 1):
        values = sheet.row_values(row)

        # Blank row
        if not values[0]:
            break

        process_value(values, "foo{}.md".format(row))


if __name__ == '__main__':
    run()
