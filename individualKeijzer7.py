#!/usr/bin/python3
from individual import individual
import numbers
import math


class individualKeijzer7(individual):
	"The representation for a genetic programming keijzer7 individual"

	def __init__(self, size, number_arguments, genotype = None):
		"Initializes the tree with its genotype"
		super().__init__(size, number_arguments, genotype)


	def generate_genotype(self, size):
		"Generates the individual's genotype"
		while True:
			subtree = super().generate_subtree([['log', 2], ['sum', 2]], size)
			super().put_terminals_on_tree(subtree, super().get_number_arguments())
			if super().get_number_terminals(subtree) == super().get_number_arguments():
				break
		return subtree


	def classify_datum_with_values(self, datum_and_values):
		"Classifies the data based on the genotype using recursion"
		# returns the same number if there isn't a function
		if isinstance(datum_and_values, numbers.Number):
			return datum_and_values

		# classifies for log function
		elif datum_and_values[0] == 'log':
			base = self.classify_datum_with_values(datum_and_values[1])
			exponent = self.classify_datum_with_values(datum_and_values[2])
			return math.log(exponent, base)

		# classifies for sum function
		elif datum_and_values[0] == 'sum':
			factor1 = self.classify_datum_with_values(datum_and_values[1])
			factor2 = self.classify_datum_with_values(datum_and_values[2])
			return factor1 + factor2

		# an error has happened
		else:
			print("An error occurred on genotype format: %s" % 
				(str(datum_and_values)))
			exit(1)


	def mutate(self):
		"Mutates the individual"
		pass


	def cross(self, other_individual):
		"Returns a new individual using crossover operation"
		new_genotype = super().get_genotype_of_cross(other_individual)
		new_individual = individualKeijzer7(super().get_size(), \
			super().get_number_arguments(), new_genotype)
		return new_individual


individual = individualKeijzer7(3, 0)
print(individual.get_genotype())