import argparse
from datetime import datetime, timedelta
import json
import sys

parser = argparse.ArgumentParser(description='Extract call data from the hangouts file. Use either -i or -n to run the program.')
parser.add_argument('-i', '--interactive', action='store_true', help='Use interactive mode')
parser.add_argument('-n', '--name', dest='name', help='Name of the contact')
parser.add_argument('-f', '--file', dest='file', default='Hangouts.json', help='Name of the json file (default: Hangouts.json)')
args = parser.parse_args()

def main():
	if len(sys.argv) == 1:
		parser.print_help() 
		exit(0)
	if args.interactive:
		print("Enabled interactive mode. Make sure the Hangouts.json file is in the same directory.")
		events = parse_data(name=None)
		name = input("Give the name of the contact to analyze:")
		parse_calls(events, name)
		exit(1)
	if args.name is None:
		parser.print_help() 
		exit(0)
	events = parse_data(args.name)
	parse_calls(events, args.name)
	exit(1)

def parse_data(name):
	with open(args.file, encoding='UTF-8') as fh:
		data = json.load(fh)

	contacts = []
	events = {}
	for conversation in data["conversations"]:
		if "conversation" not in conversation["conversation"] or \
			"participant_data" not in conversation["conversation"]["conversation"]:
			continue		
		conversationData = conversation["conversation"]["conversation"]
		for participant in conversationData["participant_data"]:
			if "fallback_name" in participant:
				contact = participant["fallback_name"]
				contacts.append(contact)
				if name is None or name == contact:
					events[contact] = conversation["events"]

	if name is None:
		print("List of contacts:\n")
		for contact in sorted(set(contacts)):
			print(contact)
			
	return events				

def to_str_date(timestamp):
	ts = int(timestamp)
	ts = ts/1000000
	return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def to_timedelta(seconds):
	m, s = divmod(seconds, 60)
	h, m = divmod(m, 60)
	return timedelta(hours=h, minutes=m, seconds=s)
 
def parse_calls(events, name):
	total_duration = 0
	calls = []	
	for event in events[name]:
		if "hangout_event" in event and "hangout_duration_secs" in event["hangout_event"]:
			date = to_str_date(event["timestamp"])
			duration = int(event["hangout_event"]["hangout_duration_secs"])
			total_duration += duration
			
			duration = to_timedelta(duration)
			t_duration = to_timedelta(total_duration)
			calls.append({ "date": date, "duration": duration, "total_duration":  t_duration})
	
	print("Parsed", len(calls), "calls for a duration of", t_duration)
	data_dict = {"calls": calls}
	filename = f"hangout_calls_{name}.json"
	print("Saving to", filename)

	with open(filename, 'w') as fh:
	    json.dump(data_dict, fh, indent=4, sort_keys=True, default=str)

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt as e:
		print('Execution aborted')
		exit(0)