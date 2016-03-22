import os
import random
import sys
import operator

# show instructions
# show prompt
# DONE to finish
# clear and update with the number of battles
# submit
# clear and show each battle
# show results

#clear screen
def clear():
	if os.name == 'nt':
		os.system('cls')
	else:
		os.system('clear')

def do_battle(matchups, items):
	show_header()
	show_battle_instructions(len(matchups), msg=None)
	print('')
	run_battles(matchups, items)

def get_matchups(items):
	list_size = len(items)
	matchups = []

	#for each item in the list (a)
	for a in range(0, list_size):
		# find each opponent in the list (b)
		for b in range(a + 1, list_size):
			matchup = [a, b]
			#shuffle the order of a and b
			random.shuffle(matchup)
			matchups.append(matchup)
	
	#then randomize the whole list of matchups
	random.shuffle(matchups)

	return matchups

#get user input to create a list of items
def input_list():
	items = []
	while True:
		item = input("> ").lower()
		#test for duplicate	
		if item in items:
			msg = "\nThat has already been entered, please enter a unique item."
		#test for blank entry
		elif item == "":
			msg = "\nNothing entered"
		#test for exit
		elif item == 'exit':
			sys.exit()
		#test for removal ('remove' + string OR 'remove' + index)
		elif 'remove' in item:
			#the 2nd word should be a string or index of an item in the list
			item_to_remove = item.split()[1].strip()
			#look for string first
			if item_to_remove in items:
				items.remove(item_to_remove)
				msg = "Removed '{}'".format(item_to_remove)
			# if string isn't found, try integer for index
			else:
				try:
					index = int(item_to_remove) - 1
				except ValueError:
					msg = "Could not remove '{}'".format(item_to_remove)
				else:
				#if the integer is within the size of the list
					if index <= len(items) and len(items):
						#remove at index
						item_removed = items.pop(index)
						msg = "Removed '{}'".format(item_removed)
					#if string and integer search fail
					else:
						msg = "Could not remove '{}'".format(item_to_remove)
		#test for submittal
		elif 'go!' in item:
			list_ready = is_list_ready(len(items))
			if list_ready:
				matchups = get_matchups(items)
				do_battle(matchups, items)
				break
			else:
				msg = "List must have at least 2 items"
		#if none of the above, set no message, append the item, refresh the display
		else:	
			msg = None
			items.append(item)
		update_display(items, msg)

def is_list_ready(list_length):
	if list_length >= 2:
		return True
	else:
		return False

def print_list(items):
	count = 1
	for item in items:
		print('{}: {}'.format(count, item))
		count += 1

def run_battles(matchups, items):
	winners = {}
	while len(matchups) > 0:
		#display instead?
		option_a = items[matchups[0][0]]
		option_b = items[matchups[0][1]]
		print('**************')
		print('1: {}'.format(option_a))
		print('2: {}'.format(option_b))
		print('**************')
		choice = input('> ').lower()
		if choice == '1':
			if option_a in winners:
				winners[option_a] += 1
			else:
				winners[option_a] = 1
			del matchups[0]
			msg = None
		elif choice == '2':
			if option_b in winners:
				winners[option_b] += 1
			else:
				winners[option_b] = 1
			del matchups[0]
			msg = None
		elif choice == 'exit':
			sys.exit()
		else:
			msg = "Enter either 1 or 2"
		update_battle_display(matchups, msg)
	show_results(winners)

def show_battles_msg(n):
	battles = int(n * (n - 1) / 2)
	print('\nWith {} items, this list will do {} battles'.format(n, battles))

#show header always
#clear screen before showing
def show_header():
	clear()
	print("""
**************
** List War **
**************
Prioritize your list with 1-on-1 battles.
""")

def show_battle_instructions(remaining_matchups, msg):
	print('{} battles remaining'.format(remaining_matchups))
	print("Choose a winner by typing '1' or '2'")
	print("Type 'exit' to quit.")
	if msg:
		print(msg)

#show these instructions in the list-build phase
def show_instructions(list_length, msg):
	list_ready = is_list_ready(list_length)
	print("Type 'remove' and then the item name or item number to remove it.")
	print("Type 'exit' to quit.")
	if list_ready:
		show_battles_msg(list_length)
		print("Type 'go!' when ready.")
	else:
		print("\nYour list is too short! Please enter at least 2 items.")
	if msg:
		print(msg)

def show_results(winners):
	show_header()
	print('Winners:')

	#sort the winners dictionary, returns a list of tuples
	sorted_list = sorted(winners.items(), key=operator.itemgetter(1))
	sorted_list.reverse()

	numbered_list = list(enumerate(sorted_list, 1))

	for item in numbered_list:
		print('{}: {} ({})'.format(item[0], item[1][0], item[1][1]))

def update_battle_display(matchups, msg):
	show_header()
	show_battle_instructions(len(matchups), msg)
	print('')

def update_display(items, msg):
	show_header()
	show_instructions(len(items), msg)
	print('')
	print_list(items)

#play the game
def game():
	show_header()
	show_instructions(list_length=0, msg=None)
	print('')
	input_list()

game()

