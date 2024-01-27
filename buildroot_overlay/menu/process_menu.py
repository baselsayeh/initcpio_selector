import yaml
import os
import sys
import struct
import select

choices=[]

output=[]

#Load events config
f = open('events.conf', 'r')
event_conf = yaml.safe_load(f)
f.close()

f = open(sys.argv[1], 'r')
menu = yaml.safe_load(f)
f.close()

for item in menu["menu"]:
    choices.append(item["Name"])

def clear_screen():
    os.system('clear')
def draw_choices(index):
    for choice in choices:
        if index == choices.index(choice):
            print("\033[41m", ">", choice, "\033[0m")
        else:
            print("  ", choice)
    print("")


FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(FORMAT)
def get_key():
    event_files=[]
    for event in event_conf["events"]:
        efile = open(event["path"], "rb")
        event_files.append(efile)
        event["fno"] = efile.fileno()

    po = select.poll()
    for efile in event_files:
        po.register(efile.fileno(), select.POLLIN)

    while True:
        events = po.poll(99999*1000)
        #event = in_file.read(EVENT_SIZE)
        if not events:
            return 0
        for fno,ev in events:
            for efile in event_files:
                if fno != efile.fileno():
                    continue
                event = efile.read(EVENT_SIZE)
                (tv_sec, tv_usec, type, code, value) = struct.unpack(FORMAT, event)

                #print("type:", type, ",code:", code, ",value:", value)

                #get the event from the event config
                curr_event_conf=None
                for event in event_conf["events"]:
                    if event["fno"] == efile.fileno():
                        curr_event_conf = event["actions"]
                        break

                #See if an action in conf matches the input event
                for action_event in curr_event_conf:
                    if action_event["type"] == type and action_event["code"] == code and action_event["value"] == value:
                        return action_event["action"]


#Turn the blinking cursor off
#print("\033[?25l", end="")

index=0
while True:
    clear_screen()
    draw_choices(index)
    key = get_key()
    if key == 1:
        if index != 0:
            index -= 1
    elif key == 2:
        if index != len(choices)-1:
            index += 1
    elif key == 3:
        break

#Prepare the output
output.append(menu["menu"][index]["Name"])
output.append(menu["menu"][index]["Path"])
if "Env" in menu["menu"][index] and len(menu["menu"][index]["Env"]) > 0:
    #f = open("ENV", "w")
    for env in menu["menu"][index]["Env"]:
        output.append(env)
        #f.write(env)
        #f.write("\n")
    #f.close()
#print("Selected", menu["menu"][index]["Name"])
#return 20
#exit()

print("|".join(output), file=sys.stderr)

    #Wait for choices
