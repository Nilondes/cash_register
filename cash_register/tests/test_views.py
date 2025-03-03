from django.test import TestCase
from api.models import Item, ItemAmount
from django.urls import reverse


class TransactionViewTestCase(TestCase):
    def setUp(self):
        self.item_1 = Item.objects.create(title="Item 1", price=1)
        self.item_2 = Item.objects.create(title="Item 2", price=2)
        self.item_amount_1 = ItemAmount.objects.create(item=self.item_1, amount=5)
        self.item_amount_2 = ItemAmount.objects.create(item=self.item_2, amount=3)


    def test_unknown_item(self):
        items = [1,2,3]
        resp = self.client.post(reverse('create_check'), {
                                                          "items": items
                                                            }
                                )
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.data['error'], "Указанные товары не найдены")

    def test_valid_items(self):
        items = [self.item_1.pk, self.item_2.pk]
        resp = self.client.post(reverse('create_check'), {
                                                          "items": items
                                                            }
                                )
        self.assertEqual(resp.status_code, 200)
