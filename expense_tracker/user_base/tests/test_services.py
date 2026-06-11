from decimal import Decimal

from django.test import TestCase

from user_base.services import split_by_equal,split_by_percent
class SplitByEqualTests(TestCase):

    def test_equal_split_900_between_3_people(self):

        class DummyUser:
            id = 1

        payer = DummyUser()

        result = split_by_equal(
            [1, 2, 3],
            payer,
            Decimal("900")
        )

        amounts = {
            item["user_id"]: item["amount"]
            for item in result
        }

        self.assertEqual(amounts[1], Decimal("300.00"))
        self.assertEqual(amounts[2], Decimal("300.00"))
        self.assertEqual(amounts[3], Decimal("300.00"))

    def test_equal_split_handles_rounding(self):

        class DummyUser:
            id = 1

        payer = DummyUser()

        result = split_by_equal(
            [1, 2, 3],
            payer,
            Decimal("100")
        )

        amounts = sorted(
            [item["amount"] for item in result],
            reverse=True
        )

        self.assertEqual(
            sum(amounts),
            Decimal("100.00")
        )

        self.assertEqual(
            amounts,
            [
                Decimal("33.34"),
                Decimal("33.33"),
                Decimal("33.33")
            ]
        )
    def test_percentage_split(self):

        class DummyUser:
            id = 1

        payer = DummyUser()

        members = [
            {"user": 1, "percentage": 50},
            {"user": 2, "percentage": 30},
            {"user": 3, "percentage": 20},
        ]

        result = split_by_percent(
            members,
            Decimal("1000"),
            payer
        )

        amounts = {
            item["user_id"]: item["amount"]
            for item in result
        }

        self.assertEqual(
            amounts[1],
            Decimal("500.00")
        )

        self.assertEqual(
            amounts[2],
            Decimal("300.00")
        )

        self.assertEqual(
            amounts[3],
            Decimal("200.00")
        )