#!/usr/bin/python3
from abc import ABC, abstractmethod
import copy
import random


class individual(ABC):
	"The representation for a genetic programming individual"

	def __init__(self, size, number_arguments, genotype):
		"Initializes the tree with its genotype"
		if genotype is None:
			self.genotype = self.generate_genotype(size)
		else:
			self.genotype = genotype
		self.number_arguments = number_arguments
		self.size = size


	def generate_terminal_list(self, list_functions):
		"Generates a list with a terminal"
		generated_list = self.generate_function_list(list_functions)
		generated_list[random.randint(0, len(generated_list) - 2) + 1] = 'XX'
		print(generated_list)
		return generated_list


	def generate_function_list(self, list_functions):
		"Generates a list with a function and its arguments"
		selected_function = list_functions[random.randint(0, len(list_functions) - 1)]
		generated_list = [selected_function[0]]
		for index in range(selected_function[1]):
			generated_list.append(random.random())
		return generated_list


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


	def get_all_lists(self):
		"Gets all lists for crossover"
		genotype = self.get_genotype()
		list_all = []
		self.get_all_lists_h(genotype, [], list_all)
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
		this_list = self.get_all_lists()
		other_list = other_individual.get_all_lists()
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


	@abstractmethod
	def mutate(self):
		"Mutates the individual"
		pass


	@abstractmethod
	def cross(self, other_individual):
		"Returns a new individual using crossover operation"
		pass