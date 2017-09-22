#!/usr/bin/python3
from __future__ import division
from abc import ABC, abstractmethod
import copy
import random


class individual(ABC):
	"The representation for a genetic programming individual"

	def __init__(self, size, number_arguments, genotype):
		"Initializes the tree with its genotype"
		self.number_arguments = number_arguments
		self.size = size
		
		if genotype is None:
			self.genotype = self.generate_genotype(size)
		else:
			self.genotype = genotype


	def generate_terminal_list(self, list_functions):
		"Generates a list with a terminal"
		generated_list = self.generate_function_list(list_functions)
		generated_list[random.randint(0, len(generated_list) - 2) + 1] = 'XX'
		return generated_list


	def generate_function_list(self, list_functions):
		"Generates a list with a function and its arguments"
		selected_function = \
			list_functions[random.randint(0, len(list_functions) - 1)]
		generated_list = [selected_function[0]]
		for index in range(selected_function[1]):
			generated_list.append(random.random())
		return generated_list


	def generate_subtree(self, list_functions, size):
		"Generates a random subtree with maximum size"
		current_list = self.generate_function_list(list_functions)
		if size > 1:
			self.generate_subtree_h(current_list, list_functions, 0, \
				size - 1, 1 / (size - 1))
		return current_list


	def put_terminals_on_tree(self, tree, n_arguments):
		"Defines the places of the terminals"
		# get all possibilities
		lists = self.get_all_lists(tree)
		if lists == []:
			if len(tree) - 1 >= n_arguments:
				self.put_terminals_on_everyplace([tree], [0], n_arguments)
				return
			else:
				return

		# delete general elements
		indexes_deletion = []
		for index1 in range(len(lists)):
			for index2 in range(len(lists)):
				if index1 == index2:
					continue
				elif self.more_specific(lists[index1][0], lists[index2][0]) \
					and index1 not in indexes_deletion:
					indexes_deletion.append(index1)
		number_deleted = 0
		for index in indexes_deletion:
			del lists[index - number_deleted]
			number_deleted += 1

		# puts the terminals on the list
		lists_terminal = self.select_elements_from_list(lists, n_arguments)
		if len(lists_terminal) == n_arguments:
			for element in lists_terminal:
				self.put_terminal_on_list(tree, element[0])
		else:
			sum_size = 0
			put = n_arguments
			for element in lists_terminal:
				sum_size += len(element[1]) - 1
			if sum_size < n_arguments:
				return
			for element in lists_terminal:
				put = self.put_terminals_on_everyplace(tree, element[0], put)


	def put_terminal_on_list(self, list_s, places):
		"Puts terminal on a list"
		list_n = list_s
		for place in places:
			list_n = list_n[place]
		list_n[random.randint(0, len(list_n) - 2) + 1] = 'XX'


	def put_terminals_on_everyplace(self, list_s, places, n_put):
		"Puts terminal on everyplace of a list"
		list_n = list_s
		for place in places:
			list_n = list_n[place]
		for index in range(1, len(list_n)):
			if n_put == 0:
				return 0
			else:
				list_n[index] = 'XX'
				n_put -= 1
		return n_put


	def more_specific(self, list1, list2):
		"Returns if list2 is more specific than list1"
		if len(list1) >= len(list2):
			return False
		else:
			for index in range(len(list1)):
				if list2[index] != list1[index]:
					return False
		return True


	def select_elements_from_list(self, lists, number):
		"Selects elements from list"
		if number >= len(lists):
			return lists
		else:
			select_list = []
			while number > 0:
				selected_index = random.randint(0, len(lists) - 1)
				select_list.append(lists[selected_index])
				del lists[selected_index]
				number -= 1
			return select_list


	def generate_subtree_h(self, current_list, list_functions, \
		index_depth, max_size, x_value):
		"Generates a subtree with maximum size defined"
		if index_depth == max_size:
			return random.random()
		list_size = len(current_list) - 1
		for index in range(list_size):
			if random.random() <= (1 - x_value / \
				((1 - index_depth * x_value) * list_size)):
				new_list = self.generate_function_list(list_functions)
				self.generate_subtree_h(new_list, list_functions, \
					index_depth + 1, max_size, x_value)
				current_list[index + 1] = new_list


	def get_size(self):
		"Gets the maximum size"
		return self.size


	def get_number_arguments(self):
		"Gets the number of arguments necessary"
		return self.number_arguments


	def get_genotype(self):
		"Returns the individual's genotype"
		return self.genotype


	def classify(self, values):
		"Classifies the data based on the genotype"
		datum_and_values = self.get_datum_with_values(values)
		return self.classify_datum_with_values(datum_and_values)


	def get_datum_with_values_h(self, values, vi, g_list):
		"Gets the datum with the values recursively"
		for index in range(len(g_list)):
			if g_list[index] == 'XX':
				g_list[index] = values[vi]
				vi += 1
			elif type(g_list[index]) is list:
				vi = self.get_datum_with_values_h(values, vi, g_list[index])
		return vi


	def get_datum_with_values(self, values):
		"Gets the datum with the values"
		if len(values) != self.get_number_arguments():
			print("Error on values' length")
			exit(1)

		genotype_copy = copy.deepcopy(self.get_genotype())
		self.get_datum_with_values_h(values, 0, genotype_copy)
		return genotype_copy


	def get_all_lists(self, lists):
		"Gets all lists for crossover"
		list_all = []
		self.get_all_lists_h(lists, [], list_all)
		return list_all


	def get_tree_size(self, list_tree):
		"Gets the tree's size"
		tree_string = str(list_tree)
		maximum = -1
		deep = 0

		for index in range(len(tree_string)):
			if tree_string[index] == '[':
				deep += 1
				if maximum < deep:
					maximum = deep
			elif tree_string[index] == ']':
				deep -= 1
		return maximum


	def get_number_terminals(self, tree):
		"Gets the number of terminals"
		return str(tree).count("XX")


	def get_all_lists_h(self, current_list, iuh, list_all):
		"Gets all lists for crossover recursively"
		for index in range(len(current_list)):
			if type(current_list[index]) is list:
				list_indexes = iuh[:]
				list_indexes.append(index)
				list_all.append([list_indexes] + [copy.deepcopy(current_list[index])] +
					[[self.get_tree_size(current_list[index])]])
				self.get_all_lists_h(current_list[index], list_indexes, list_all)


	def get_genotype_of_cross(self, other_individual):
		"Returns a new genotype using crossover operation"
		# get possibilities for crossover
		this_list = self.get_all_lists(self.get_genotype())
		other_list = other_individual.get_all_lists(self.get_genotype())
		possibilities = []
		for tl in this_list:
			for ol in other_list:
				if len(tl[0]) + ol[2][0] <= self.get_size():
					if str(tl).count("XX") == str(ol).count("XX"):
						possibilities.append(tl)
						possibilities.append(ol)

		# selects genotypes for crossover
		random_index = random.randint(0, len(possibilities) / 2 - 1)
		indexes_substitution = possibilities[2 * random_index][0]
		genotypes_substitution = possibilities[2 * random_index + 1][1]

		# generates another individual with genotype from crossover
		new_genotype = copy.deepcopy(self.get_genotype())
		list_substitution = new_genotype
		for index in range(len(indexes_substitution) - 1):
			list_substitution = list_substitution[indexes_substitution[index]]
		list_substitution[indexes_substitution[len(indexes_substitution) - 1]] = \
			genotypes_substitution
		return new_genotype


	@abstractmethod
	def classify_datum_with_values(self, datum_and_values):
		"Classifies the data based on the genotype using recursion"
		pass


	@abstractmethod
	def generate_genotype(self, size):
		"Generates the individual's genotype"
		pass


	def mutate(self):
		"Mutates the individual"
		pass


	@abstractmethod
	def cross(self, other_individual):
		"Returns a new individual using crossover operation"
		pass