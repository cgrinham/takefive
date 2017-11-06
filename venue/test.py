from django.test import TestCase
from venue.models import Member
from datetime import datetime


class MemberTestCase(TestCase):
    def setUp(self):
        Member.objects.create(
                              firstname='Sam',
                              lastname='Brooks',
                              email='sam@brooks.com',
                              dateofbirth=datetime(2017, 11, 2),
                              appearances=3,
                              )

    def test_members_are_real(self):
        sam = Member.objects.get(firstname='Sam')
        self.assertEqual(sam, 'Sam Brooks')
