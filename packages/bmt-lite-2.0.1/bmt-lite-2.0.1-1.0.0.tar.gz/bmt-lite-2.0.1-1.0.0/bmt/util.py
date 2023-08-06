"""Utilities."""
import re


def pascal_to_snake(s: str, sep: str = "_") -> str:
    """Convert Pascal case to snake case.

    Assumes that
    a) all words are either all-lowercase or all-uppercase
    b) all 1-letter words are lowercase
    c) there are no adjacent 1-letter words
    d) there are no adjacent uppercase words

    Examples:
    PhenotypicFeature -> phenotypic_feature
    RNAProduct -> RNA_product
    FeedACamel -> feed_a_camel
    
    Optionally specify `sep` (default "_").
    """
    # add an underscore before each capital letter
    underscored = re.sub(
        r"(?<!^)(?=[A-Z])",
        sep,
        s,
    )
    # collapse any adjacent one-letter words
    collapsed = re.sub(
        r"(?<![a-zA-Z])[A-Z](?:_[A-Z](?=$|_))+",
        lambda match: match.group(0).replace("_", ""),
        underscored,
    )
    # lower-case any words containing only one uppercase letter
    lowercased = re.sub(
        r"(?<![A-Z])[A-Z](?![A-Z])",
        lambda match: match.group(0).lower(),
        collapsed,
    )
    return lowercased


def snake_to_pascal(s: str, sep: str = "_") -> str:
    """Convert snake case to Pascal case.

    This is the inverse of pascal_to_snake() when its assumptions
    are true.
    
    Optionally specify `sep` (default "_").
    """
    return re.sub(
        fr"(?:^|{sep})([a-zA-Z])",
        lambda match: match.group(1).upper(),
        s
    )
