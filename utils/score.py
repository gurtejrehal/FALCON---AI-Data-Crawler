import json
import copy


class Score:
    """
    Finding Score for difference in Test Data and Recurring Test Data

    """

    def make_hash(self, o):

        """
        Makes a hash from a dictionary, list, tuple or set to any level, that contains
        only other hashable types (including any lists, tuples, sets, and
        dictionaries).

        :return: hash of Nested Dictionary
        """

        if isinstance(o, (set, tuple, list)):

            return tuple([self.make_hash(e) for e in o])

        elif not isinstance(o, dict):

            return hash(o)

        new_o = copy.deepcopy(o)
        for k, v in new_o.items():
            new_o[k] = self.make_hash(v)

        return hash(tuple(frozenset(sorted(new_o.items()))))

    def json_matrix(self, x):

        """
        hashing nested dictionaries using make_hash()
        hashing list using hash(frozenset())
        hashing strings using hash()

        :param: x -> JSON
        :return: Tuple of path, types.
        """


        path = []
        types = []
        common_hash = []

        for k, v in x.items():

            if isinstance(v, dict):
                """
                check entity is a dictionary
                """

                for k1, v1 in v.items():

                    if isinstance(v1, list):
                        """
                        check Dictionary entity has a List
                        example: images
                        """

                        if isinstance(v1[0], dict):
                            """
                            Check list is, List of Dictionary
                            example: (old) ingredients
                            """

                            for k2, v2 in enumerate(v1):
                                types.append(type(v2))
                                path.append(k + '.' + k1 + '.' + next(iter(v2)) + '.' + str(k2))
                                common_hash.append(hash(frozenset(v2)))


                        elif isinstance(v1[0], str):
                            """
                            check whether List is simply a List
                            example: images
                            """

                            path.append(k + '.' + k1)
                            types.append(type(v1))
                            common_hash.append(hash(frozenset(v1)))


                    elif isinstance(v1, dict):
                        """
                        check Dictionary entity has a Dictionary
                        example: product dimensions
                        """

                        for k3, v3 in v1.items():
                            path.append(k + '.' + k1 + '.' + k3)
                            types.append(type(v3))
                            common_hash.append(hash(v3))


                    elif isinstance(v1, str):
                        """
                        check Dictionary entity has a string
                        example: product_name
                        """

                        path.append(k + '.' + k1)
                        types.append(type(v1))
                        common_hash.append(hash(v1))


            elif isinstance(v, list):
                """
                check entity is a list
                """

                for k4, v4 in enumerate(v):
                    """
                    check List entity has a Dictionary
                    example: reviews, (new) ingredients
                    """

                    if isinstance(v4, dict):
                        types.append(type(v4))
                        path.append(k + '.' + str(k4))
                        common_hash.append(hash(frozenset(v4)))

        return (path, types)

    def total_score(self, a, b):
        """
        Calculate the score with below configurations:

        None : Type,
        Type : None,
        Same : Same,
        Type1 : Type2

        Two Dictionaries are equal, score will be 0,
        else we calculate the score.

        :param: a -> Test Data
        :param: b -> Recurring Test Data
        :return: Final score
        """

        score = 0
        if self.make_hash(a) != self.make_hash(b):
            # Total number of entries in old and new json
            check_list = (list(set().union(self.json_matrix(a)[0], self.json_matrix(b)[0])))

        # weights
        weight_config = {
            "None to Type": 2,
            "Type to None": -3,
            "Same Type": 0,
            "Type change": 1
        }

        # score calculate
        for i in range(len(check_list)):
            try:
                index_a = self.json_matrix(a)[0].index(check_list[i])
                index_b = self.json_matrix(b)[0].index(check_list[i])
            except ValueError:
                pass

            if (check_list[i] in self.json_matrix(a)[0]) and (check_list[i] in self.json_matrix(b)[0]):
                # same type
                if self.json_matrix(a)[1][index_a] == self.json_matrix(b)[1][index_b]:
                    score += weight_config.get("Same Type")

                # Type change
                else:
                    score += weight_config.get("Type change")

            elif (check_list[i] not in self.json_matrix(a)[0]) and (check_list[i] in self.json_matrix(b)[0]):
                # none to type
                score += weight_config.get("None to Type")

            elif (check_list[i] in self.json_matrix(a)[0]) and (check_list[i] not in self.json_matrix(b)[0]):
                # type to none
                score += weight_config.get("Type to None")

        return score
