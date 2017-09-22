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


	def mutate(self):
		"Mutates the individual"
		genotype = super().get_genotype()
		if super().get_tree_size(genotype) > 1:
			lists = super().get_all_lists(genotype)
			selected = super().select_elements_from_list(lists, 1)
			max_size = super().get_size() - len(selected[0][0])
			if max_size >= 1:
				number_arguments = super().get_number_terminals(selected[0][1])
				list_s = genotype
				for index in selected[0][0][0 : len(selected[0][0]) - 1]:
					list_s = list_s[index]

				new_tree = []
				while True:
					new_tree = super().generate_subtree([['log', 2], ['sum', 2]], max_size)
					super().put_terminals_on_tree(new_tree, number_arguments)
					if super().get_number_terminals(new_tree) == number_arguments:
						break
				list_s[selected[0][0][len(selected[0][0]) - 1]] = new_tree



	def cross(self, other_individual):
		"Returns a new individual using crossover operation"
		new_genotype = super().get_genotype_of_cross(other_individual)
		new_individual = individualKeijzer7(super().get_size(), \
			super().get_number_arguments(), new_genotype)
		return new_individual


individual = individualKeijzer7(4, 5)
print(individual.get_genotype())
individual.mutate()
print("\n\n")
print(individual.get_genotype())