import nltk as nt
import itertools as itt

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/paraphrase', methods=['GET'])
def paraphrase():
    """Creates a list of paraphrased trees based on the input flat tree and limit.

    Returns:
        paraphrases_json: A formatted and limited JSON serialized list of all paraphrases.
    """

    default_limit = 20

    # Get 'tree' and 'limit' arguments
    flat_tree = request.args.get('tree')
    limit = request.args.get('limit')

    # Check if 'tree' argument is entered
    if flat_tree:
        # Limit validation
        if limit is None or int(limit) <= 0:
            limit = default_limit
        else:
            limit = int(limit)

        paraphrases = get_paraphrases(flat_tree)
        paraphrases_limited = limit_list(paraphrases, limit)
        paraphrases_json = format_return(paraphrases_limited)

        return paraphrases_json
    else:
        return "The Tree sentence is not entered. Try again!"


def get_paraphrases(flat_tree):
    """Creates a list of paraphrased trees based on the input flat tree.

    Args:
        flat_tree: A string containing a tree in '(S (NP (..)) (..) ..)' format.

    Returns:
        flat_tree_combinations: A list of all paraphrases in '(S (NP (..)) (..) ..)' format.
    """

    tree = nt.Tree.fromstring(flat_tree)
    all_tree_positions = [i for i in tree.treepositions()]

    positions_to_swap = get_positions_for_label(tree, all_tree_positions, "NP")
    grouped_positions = group_positions(positions_to_swap)
    position_combinations = get_all_combinations(grouped_positions)

    # Swap each branch of the tree should start from the leaves, so the first indexes should be the closest
    # to the leaves
    group_id_reverse = sorted(list(grouped_positions.keys()), key=len, reverse=True)

    tree_combinations = get_tree_combinations(tree, position_combinations, grouped_positions, group_id_reverse)

    # Format all tree combinations from Tree[..] into '(S (NP (..)) (..) ..)'
    flat_tree_combinations = [combination._pformat_flat("", "()", False) for combination in tree_combinations]

    return flat_tree_combinations


def get_positions_for_label(tree, all_tree_positions, label):
    """Returns the positions of all nodes in the tree that match the specified label.

    Args:
        tree: A string containing a tree in '(S (NP (..)) (..) ..)' format.
        all_tree_positions: A list of all positions in the tree.
        label: The label to search for.

    Returns:
        positions_to_swap: A list of positions of all nodes in the tree that match the specified label.
    """

    label_positions = []
    positions_to_swap = []

    # Goes through each position and adds the chosen one based on the label
    for i in all_tree_positions:
        # Check if the item not tree leaves
        if type(tree[i]) != str:
            if tree[i].label() == label:
                label_positions.append(i)

    # Goes through each label position and adds only ones can be swapped
    for k in label_positions:
        for m in label_positions:
            if k[:-1] == m[:-1] and k != m:
                positions_to_swap.append(k)
                break

    return positions_to_swap


def group_positions(positions_to_swap):
    """Groups the positions of all nodes that should be swapped together.

    Args:
        positions_to_swap: A list of positions of all nodes that should be swapped together.

    Returns:
        grouped_positions: A dictionary containing the groups of positions that should be swapped together.
    """

    grouped_positions = {}

    for i in positions_to_swap:
        str_i = "".join(list(map(str, i)))
        group_id = str_i[:-1]
        if group_id not in grouped_positions.keys():
            grouped_positions[group_id] = (i,)
        else:
            grouped_positions[group_id] += (i,)

    return grouped_positions


def get_all_combinations(grouped_positions):
    """Returns all possible combinations of node swaps for the given groups.

    Args:
        grouped_positions: A dictionary containing the groups of positions that should be swapped together.

    Returns:
        position_combinations_grouped: A list of all possible combinations of node swaps for the given groups.
    """

    node_combinations = {}

    # All position combinations for each certain node
    for i in grouped_positions.keys():
        node_combinations[i] = tuple(itt.permutations(grouped_positions[i]))

    position_combinations = list(itt.product(*node_combinations.values()))
    position_combinations_grouped = [dict(zip(grouped_positions.keys(), i)) for i in position_combinations]

    return position_combinations_grouped


def get_tree_combinations(tree, all_position_combinations, grouped_positions, group_id_reverse):
    """Returns all possible paraphrased trees based on the input flat tree.

    Args:
        tree: A string containing a tree in '(S (NP (..)) (..) ..)' format.
        all_position_combinations: A list of all possible combinations of node swaps for the given groups.
        grouped_positions: A dictionary containing the groups of positions that should be swapped together.
        group_id_reverse: A list of group IDs in reverse order of length.

    Returns:
        tree_combinations: A list of all possible paraphrased trees based on the input flat tree.
    """

    tree_combinations = []
    for i in all_position_combinations:
        new_tree = tree.copy(deep=True)
        for j in group_id_reverse:
            change_values = grouped_positions[j]
            set_values = [new_tree[i[j][k]] for k in range(len(change_values))]

            # Swap tree branches
            for k in range(len(change_values)):
                new_tree[change_values[k]] = set_values[k]

        tree_combinations.append(new_tree)

    return tree_combinations


def limit_list(paraphrase_list, limit):
    """Limits the number of paraphrases returned to the specified limit.

    Args:
        paraphrase_list: A list of paraphrased trees.
        limit: The maximum number of paraphrases to return.

    Returns:
        paraphrase_list_limited: A list of paraphrased trees limited to the specified limit.
    """

    limit_range = min(int(limit), len(paraphrase_list))
    paraphrase_list_limited = [paraphrase_list[i] for i in range(limit_range)]

    return paraphrase_list_limited


def format_return(paraphrases_list):
    """Formats the list of paraphrases as a JSON object.

    Args:
        paraphrases_list: A list of paraphrased trees.

    Returns:
        paraphrases_json: A formatted and serialized JSON object containing the list of paraphrases.
    """

    value = [{"tree": i} for i in paraphrases_list]
    paraphrases_json = jsonify(paraphrases=value)

    return paraphrases_json


if __name__ == '__main__':
    app.run()
