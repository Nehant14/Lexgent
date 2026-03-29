"""Typed payload schemas used by the agent pipeline."""

from dataclasses import dataclass
from typing import Any


@dataclass
class DraftRequest:
    agreement_type: str
    party_a: str
    party_b: str
    jurisdiction: str
    payment_terms: str
    confidentiality_level: str
    liability_cap: str
    term_months: int
    extra_notes: str = ""


@dataclass
class DraftContext:
    summary: str
    normalized_fields: dict[str, Any]


@dataclass
class RetrievedClause:
    clause_id: str
    title: str
    text: str
    score: float



# @dataclass :

# What this automatically creates:
# __init__(self, name, age)
# __repr__() → readable string representation
# __eq__() → comparison between objects

# without it : 
# class Person:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age


# with it:
# @dataclass
# class Person:
#     name: str
#     age: int = 18
