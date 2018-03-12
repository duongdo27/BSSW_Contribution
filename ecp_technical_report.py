# required install package
# pip install oauth2client==1.5.2
# pip install gspread==0.6.2

import gspread
from oauth2client.client import SignedJwtAssertionCredentials
import json

# Below are the indexes of necessary information in the Google Sheet. Need to change if needed

TECH_AREA = 4  # Column E
PROJECT = range(5, 10)  # will be one of the columns F through J in the spreadsheet
HAVE_SPOTLIGHT = 10  # column K
SPOTLIGHT_REPORT = 11  # column L
PROGRESS_REPORT = 12  # column M


# get the google client - no need to change
def get_google_client():
    with open('google_key.json') as f:
        config = json.load(f)

    creds = SignedJwtAssertionCredentials(
        config['client_email'],
        config['private_key'],
        ['https://spreadsheets.google.com/feeds']
    )
    return gspread.authorize(creds)


# group by technical area
def process_value(values, topics):
    topic = values[TECH_AREA]
    if topic in topics:
        topics[topic].append(values)
    else:
        topics[topic] = [values]


# get the project from Google sheet
def get_project(values):
    for i in PROJECT:
        if values[i]:
            return values[i]
    return ""


# write content to file
def write_to_file(topics):
    for topic in sorted(topics.keys()):
        filename = "{}.md".format(topic)
        with open(filename, "w") as f:
            # Write header for file
            f.write("### {}\n\n".format(topic))

            ls = []
            # add projects, spotlight, and progress report to list
            for values in topics[topic]:
                ls.append([get_project(values), values[SPOTLIGHT_REPORT], values[PROGRESS_REPORT], values[HAVE_SPOTLIGHT]])

            # sort the list by project orders
            ls = sorted(ls, key=lambda x: x[0])

            # write the list to file
            for project, spotlight, progress_report, have_spotlight in ls:
                # write the spot light if any
                if spotlight:
                    f.write("Spotlight: {}\n".format(have_spotlight))
                    f.write("{}\n\n".format(spotlight))

                # write project
                f.write("#### {}\n".format(project))

                # write progress report
                if progress_report:
                    f.write("{}\n\n".format(progress_report))
                else:
                    f.write("No report")


def run():
    gc = get_google_client()

    # Open file: key in the URL
    doc = gc.open_by_key('1wRWjy5UvA62hNvdhU-JVsWK0_8r6exdnDyn4vufand0')

    # Open tab
    sheet = doc.worksheet("Sheet1")

    row_count = sheet.row_count
    topics = {}
    for row in range(2, row_count + 1):
        values = sheet.row_values(row)

        # Blank row
        if not values[0]:
            break
        # process the values collected
        process_value(values, topics)
        #print values

    # write values into file
    write_to_file(topics)


if __name__ == '__main__':
    run()
