from feedback_man.models import Teacher, Course
import functools
import re

def search_teacher_name(name: str):
    """
    Search for teachers matching the given name in the database.
    Returns a QuerySet of all teachers who fit the search.
    """
    return Teacher.objects.filter(teacher_name__iregex=regex_token_search(name))

def search_course_name(name: str):
    """"
    Search for courses matching the given name in the database.
    Returns a QuerySet of all courses who fit the search.
    """
    return Course.objects.filter(course_name__iregex=regex_token_search(name))

def regex_token_search(query: str):
    """
    Create a regular expression for searching the database by matching for zero or more characters between
    each token in the query.
    """
    #regex of all tokens in the passed name with zero or more characters in between/on the ends of each
    return functools.reduce(lambda regex, token: regex + re.escape(token+"*+"), query.split(), r"*+")