class Constraint(object):
    BLACKLISTED_SUBSTRINGS_IN_EVAL = [
        'rm',
        'rf',
        'import',
        '__',
        'lambda',
        'def'
    ]

    def __init__(self, name, variables, expression):
        """
        name: string
        variables: list or tuple
        expression: string
        """
        self.name = name
        self.ordered_variables = list(variables)
        self.variables = set(variables)
        self.function = self.make_function(self.ordered_variables, expression)
        self.expression = expression

    def __repr__(self):
        return self.expression

    def is_satisfied(self, *values, **value_map):
        """
        values: dict(variable: value)
        """
        return self.function(*values, **value_map)

    def has_input_variable(self, variable):
        return variable in self.variables

    @staticmethod
    def make_function(variables, expression, environment=globals()):
        for substring in Constraint.BLACKLISTED_SUBSTRINGS_IN_EVAL:
            if substring in expression:
                raise Exception('Attempted to run blacklisted command')
        return eval("(lambda " + ', '.join(variables) + ": " + expression + ")", environment)


class Variable(object):
    """
    Superclass
    """
    def __init__(self, name, domain):
        self.name = name
        self.domain = domain


class ConstraintNetwork(object):
    """
    Superclass
    """
    def __init__(self, constraints, domains):
        """
        :param constraints: dict {constraint_name: constraint_instance}
        :param domains: dict {domain_name: set(values)}
        :return:
        """
        self.constraints = constraints
        self.domains = domains
        self.variable_constraints_cache = {}

    def get_constraints_by_variable(self, variable, current_constraint=None):
        """
        current_constraint is excluded from the result
        :param variable:
        :param current_constraint:
        :return:
        """
        hash_key = hash(
            variable +
            ('' if current_constraint is None else "__" + current_constraint.expression)
        )
        if hash_key in self.variable_constraints_cache:
            return self.variable_constraints_cache[hash_key]

        constraints = set()
        for constraint_name in self.constraints:
            constraint = self.constraints[constraint_name]
            if constraint != current_constraint and constraint.has_input_variable(variable):
                constraints.add(constraint)

        self.variable_constraints_cache[hash_key] = constraints
        return constraints

    def get_num_unsatisfied_constraints(self, domains):
        num_unsatisfied_constraints = 0
        for constraint in self.constraints.itervalues():
            variables = {}
            for variable in constraint.ordered_variables:
                variables[variable] = None
                for value in domains[variable]:
                    variables[variable] = value
                    break
            if not constraint.is_satisfied(*variables.itervalues()):
                num_unsatisfied_constraints += 1
        return num_unsatisfied_constraints
