#!/usr/bin/python3
from individual import individual
import numbers
import math
import random
import copy


class individualKeijzer7(individual):
	"The representation for a genetic programming keijzer7 individual"

	def __init__(self, size, number_arguments):
		"Initializes the tree with its genotype"
		super().__init__(size, number_arguments)


	def __init__(self, genotype, size, number_arguments):
		"Initializes the tree passing the genotype"
		super().__init__(genotype, size, number_arguments)


	def generate_genotype(self, size):
		"Generates the individual's genotype"
		return ['sum', ['log', 10, ['log', 10, 'XX']], 3]


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
		# get possibilities for crossover
		this_list = super().get_all_lists()
		other_list = super().get_all_lists()
		possibilities = []
		for tl in this_list:
			for ol in other_list:
				if len(tl[0]) + ol[2][0] <= self.get_size():
					possibilities.append(tl)
					possibilities.append(ol)

		# selects genotypes for crossover
		random_index = random.randint(0, len(possibilities) - 1)
		indexes_substitution = possibilities[random_index][0]
		genotypes_substitution = possibilities[random_index + 1][1]

		# generates another individual with genotype from crossover
		new_genotype = copy.deepcopy(super().get_genotype())
		list_substitution = new_genotype
		print(new_genotype)
		print(indexes_substitution)
		print(genotypes_substitution)
		for index in range(len(indexes_substitution) - 1):
			list_substitution = list_substitution[indexes_substitution[index]]
		list_substitution[indexes_substitution[len(indexes_substitution) - 1]] = \
			genotypes_substitution
		print(new_genotype)
		new_individual = individualKeijzer7(new_genotype, super().get_size(), \
			super().get_number_arguments())
		return new_individual


individual = individualKeijzer7(7, 1)
individual2 = individualKeijzer7(7, 1)
print(individual.classify([100]))
i = individual.cross(individual2)