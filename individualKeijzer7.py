#!/usr/bin/python3
from individual import individual
import numbers
import math


class individualKeijzer7(individual):
	"The representation for a genetic programming keijzer7 individual"

	def __init__(self, size, number_arguments, genotype = None):
		"Initializes the tree with its genotype"
		super().__init__(size, number_arguments, \
			[['log', 2], ['sum', 2]], genotype)


	def classify_datum_with_values(self, datum_and_values):
		"Classifies the data based on the genotype using recursion"
		# returns the same number if there isn't a function
		if isinstance(datum_and_values, numbers.Number):
			return datum_and_values

		# classifies for log function
		elif datum_and_values[0] == 'log':
			base = self.classify_datum_with_values(datum_and_values[1])
			exponent = self.classify_datum_with_values(datum_and_values[2])
			if math.fabs(base) < 2:
				base = 2
			if math.fabs(exponent) < 1:
				exponent = 1
			return math.log(math.fabs(exponent), math.fabs(base))

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


	def cross(self, other_individual):
		"Returns a new individual using crossover operation"
		new_genotype = super().get_genotype_of_cross(other_individual)
		new_individual = individualKeijzer7(super().get_size(), \
			super().get_number_arguments(), new_genotype)
		return new_individual


individual = individualKeijzer7(4, 10)
print(individual.get_genotype())
individual.mutate()
print("\n\n")
print(individual.get_genotype())