import unittest
from constraint_network import Constraint, ConstraintNetwork
from csp_node import CspNode


class TestCspNode(unittest.TestCase):
    def test_csp_node(self):
        initial_domains = {
            "x": {0, 1, 2, 3},
            "y": {0, 1, 2, 3, 4, 5},
            "z": {4, 5, 6, 7}
        }
        constraint_network = ConstraintNetwork(
            constraints={
                "c1": Constraint(
                    name="c1",
                    variables=['x', 'y'],
                    expression='x > y'
                ),
                "c2": Constraint(
                    name="c2",
                    variables=['x', 'y', 'z'],
                    expression='x + y > z'
                )
            },
            domains=initial_domains
        )

        CspNode.set_constraint_network(constraint_network)
        CspNode.set_constraints(constraint_network.constraints)
        csp_node = CspNode(
            domains=initial_domains
        )
        csp_node.initialize_csp()
        csp_node.domain_filtering()


if __name__ == '__main__':
    unittest.main()
