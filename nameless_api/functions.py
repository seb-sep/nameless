from feedback_man.models import Teacher
import functools
import re

def search_teacher_name(name: str):
    """
    Search for teachers matching the given name in the database.
    Returns a QuerySet of all teachers who fit the search.
    """

    #regex of all tokens in the passed name with zero or more characters in between/on the ends of each
    regex_str = functools.reduce(lambda regex, token: regex + re.escape(token+"*+"), name.split(), r"*+")

    return Teacher.objects.filter(teacher_name__iregex=regex_str)