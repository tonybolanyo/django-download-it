from django.core.management.color import no_style
from django.db import connection, models
from django.test import TestCase

"""
How to test CustomField?
The most common approach to this problem is simple, if annoying:
declare all test-specific models in test/models.py, but don’t include
the test app in INSTALLED APPS. In your test suite’s setup method,
monkey-patch your settings to include the test app and run Django’s
syncdb command, and un-patch your settings in the teardown method.

Dynamically altering your settings in the test suite keeps your production
database clean—a rogue syncdb won’t suddenly create dozens of useless new
tables. My biggest gripe with this approach, though, is that it forces you to
separate your test code into two files. The tests become much harder to read,
and the file of test models inevitably becomes a crufty mess.


See original post by Akshay Shah:
http://www.akshayshah.org/post/testing-django-fields/
"""


class TestModel(models.Model):

    """
    By making all the test models inherit from this abstract model,
    You can have: no raw SQL, no test tables in production, and
    model definitions alongside the test code.

    See original post by Akshay Shah:
    http://www.akshayshah.org/post/testing-django-fields/
    """

    class Meta:
        abstract = True

    @classmethod
    def create_table(cls):
        # Cribbed from Django's management commands.
        raw_sql, refs = connection.creation.sql_create_model(
            cls, no_style(), [])
        create_sql = u'\n'.join(raw_sql).encode('utf-8')
        cls.delete_table()
        cursor = connection.cursor()
        try:
            cursor.execute(create_sql)
        finally:
            cursor.close()

    @classmethod
    def delete_table(cls):
        cursor = connection.cursor()
        try:
            cursor.execute('DROP TABLE IF EXISTS %s' % cls._meta.db_table)
        except:
            # Catch anything backend-specific here.
            # (E.g., MySQLdb raises a warning if the table didn't exist.)
            pass
        finally:
            cursor.close()


class ModelTestCase(TestCase):

    """
    Add a little funcionality to Django's builtin `TestCase` class
    to avoid boilerplate table management in all tests setups and
    teardowns code.

    See original post by Akshay Shah:
    http://www.akshayshah.org/post/testing-django-fields/
    """

    temporary_models = tuple()

    def setUp(self):
        self._map_over_temporary_models('create_table')
        super(ModelTestCase, self).setUp()

    def tearDown(self):
        self._map_over_temporary_models('delete_table')
        super(ModelTestCase, self).tearDown()

    def _map_over_temporary_models(self, method_name):
        for m in self.temporary_models:
            try:
                getattr(m, method_name)()
            except AttributeError:
                raise TypeError("%s doesn't support table mgmt." % m)
