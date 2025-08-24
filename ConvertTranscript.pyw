import operator
import tkinter
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os
import time

# keep root in background
Tk().withdraw()

# open the raw transcript file that contains the JS array of the transcript
filename = askopenfilename(title="Open your file for Encryption/Decryption")
raw_transcript = open(filename, 'r')

# intermediary file for cleaning up before mapping participant ID's
# better to use a file than store in memory as transcript could be too long to store in memory
cleaned_transcript = open("semi-converted.txt", 'x')

participant_id_list = []

# strip everything except participant ID and text
for line in raw_transcript.readlines():
    if line[0:19] == '            "text":':
        cleaned_transcript.write(line[20:])
        cleaned_transcript.write('\n')

    if line[0:32] == '                "participantId":':
        cleaned_transcript.write(line[16:])

# finished with cleaned_transcript file
cleaned_transcript.close()

# reopen cleaned transcript as read-only
cleaned_transcript = open("semi-converted.txt", 'r')

participant_mapping = {}

# ask the user to map the participants
# using a TK subwindow to make it more user-friendly
lines = cleaned_transcript.readlines()
for i, line in enumerate(lines):
    if line[0:17] == '"participantId": ':
        current_participant = line[17:].strip('\n').strip('"')
        if current_participant not in participant_mapping:
            subwindow = tkinter.Toplevel()
            subwindow.title("RingCentral Transcript Mapper")

            participant_text = str(lines[i + 1])
            prompt_text = "Who said the following: "
            prompt_label = tkinter.Label(subwindow, textvariable=tkinter.StringVar(value=prompt_text))
            participant_label = tkinter.Label(subwindow, textvariable=tkinter.StringVar(value=participant_text))

            name_entry = tkinter.Entry(subwindow)

            confirm_button = tkinter.Button(subwindow, text="Confirm", command=lambda: (operator.setitem(participant_mapping, current_participant, name_entry.get()), subwindow.destroy()))
            skip_button = tkinter.Button(subwindow, text="skip", command=lambda: subwindow.destroy())

            prompt_label.pack()
            participant_label.pack()
            name_entry.pack()
            confirm_button.pack()
            skip_button.pack()
            subwindow.wait_window()

timestamp = int(time.time())
converted_transcript = open(f"converted_transcript{timestamp}.txt", 'x')

# write final transcript
for line in lines:
    if line[0:17] == '"participantId": ':
        current_participant = line[17:].strip('\n').strip('"')
        if current_participant in participant_mapping:
            converted_transcript.write(participant_mapping[current_participant])
            converted_transcript.write('\n')
        else:
            converted_transcript.write(line)
    else:
        converted_transcript.write(line)

converted_transcript.close()
cleaned_transcript.close()
os.remove("semi-converted.txt")







