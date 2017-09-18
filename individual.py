#!/usr/bin/python3
from abc import ABC, abstractmethod
import copy


class individual(ABC):
	"The representation for a genetic programming individual"

	def __init__(self, size, number_arguments):
		"Initializes the tree with its genotype"
		self.genotype = self.generate_genotype(size)
		self.number_arguments = number_arguments


	def get_number_arguments(self):
		"Gets the number of arguments necessary"
		return self.number_arguments


	def get_genotype(self):
		"Returns the individual's genotype"
		return self.genotype


	def classify(self, values):
		"Classifies the data based on the genotype"
		# gets the datum with the values
		datum_and_values = self.get_datum_with_values(values)
		return self.classify_datum_with_values(datum_and_values)


	def get_datum_with_values_h(self, values, vi, g_list):
		"Gets the datum with the values recursivelly"
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