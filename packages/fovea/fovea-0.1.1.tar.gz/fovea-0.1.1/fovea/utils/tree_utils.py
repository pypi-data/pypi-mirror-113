"""
Utils to handle nested data structures

Install dm_tree first:
https://tree.readthedocs.io/en/latest/api.html
"""
import collections

try:
    import tree

    """
    # prefix all methods with `tree_`, can be generated as:
    
    for k in tree.__all__:
        if k.isupper():
            print(f'TREE_{k} = tree.{k}')
        else:
            print(f'tree_{k} = tree.{k}')
    """
    tree_is_nested = tree.is_nested
    tree_assert_same_structure = tree.assert_same_structure
    tree_unflatten_as = tree.unflatten_as
    tree_flatten = tree.flatten
    tree_flatten_up_to = tree.flatten_up_to
    tree_flatten_with_path = tree.flatten_with_path
    tree_flatten_with_path_up_to = tree.flatten_with_path_up_to
    tree_map_structure = tree.map_structure
    tree_map_structure_up_to = tree.map_structure_up_to
    tree_map_structure_with_path = tree.map_structure_with_path
    tree_map_structure_with_path_up_to = tree.map_structure_with_path_up_to
    tree_traverse = tree.traverse

except ImportError:
    raise ImportError("Please install dm_tree first: `pip install dm_tree`")


def is_sequence(obj):
    """
    Returns:
      True if the sequence is a collections.Sequence and not a string.
    """
    return isinstance(obj, collections.abc.Sequence) and not isinstance(obj, str)


def is_mapping(obj):
    """
    Returns:
      True if the sequence is a collections.Mapping
    """
    return isinstance(obj, collections.abc.Mapping)
