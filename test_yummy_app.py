
import unittest
from unittest.mock import patch
from yummy_app import YummyApp
import gps_service


# =====================================================
# CAP DO 1: KIEM THU CHUC NANG TINH TIEN DON HANG
# =====================================================
class TestEasyLevel(unittest.TestCase):

    def setUp(self):
        self.app = YummyApp()

    def test_calculate_total_for_single_item(self):
        cart = {"pho": 2}
        self.assertEqual(
            self.app.calculate_order_total(cart), 100000
        )

    def test_calculate_total_for_multiple_items(self):
        cart = {"pho": 1, "bun": 1}
        self.assertEqual(
            self.app.calculate_order_total(cart), 95000
        )

    def test_calculate_total_for_empty_cart(self):
        self.assertEqual(
            self.app.calculate_order_total({}), 0.0
        )

    def test_calculate_total_with_zero_quantity(self):
        cart = {"pho": 0}
        self.assertEqual(
            self.app.calculate_order_total(cart), 0.0
        )


# =====================================================
# CAP DO 2: KIEM THU MA KHUYEN MAI
# =====================================================
class TestMediumLevel(unittest.TestCase):

    # TC01: Ma GIAM10 hop le khi online
    def test_apply_valid_promo_online(self):
        app = YummyApp(
            network_status="online",
            os_version=15
        )

        result = app.apply_promo_code(100000, "GIAM10")

        self.assertEqual(result, 90000)

    # TC02: Mat ket noi mang
    def test_apply_promo_offline(self):
        app = YummyApp(
            network_status="offline",
            os_version=15
        )

        with self.assertRaises(ConnectionError):
            app.apply_promo_code(100000, "GIAM10")

    # TC03: Ma dac biet tren OS 15
    def test_special_promo_os15(self):
        app = YummyApp(
            network_status="online",
            os_version=15
        )

        result = app.apply_promo_code(
            100000, "NEW_OS_ONLY"
        )

        self.assertEqual(result, 80000)

    # TC04: Ma dac biet tren OS 14
    def test_special_promo_os14(self):
        app = YummyApp(
            network_status="online",
            os_version=14
        )

        with self.assertRaises(ValueError):
            app.apply_promo_code(
                100000, "NEW_OS_ONLY"
            )


# =====================================================
# CAP DO 2: KIEM THU GPS BANG MOCKING
# =====================================================
class TestHardLevel(unittest.TestCase):

    # TC05: GPS nam trong vung ho tro
    @patch("yummy_app.gps_service.get_current_location")
    def test_gps_inside_supported_area(self, mock_gps):
        mock_gps.return_value = (10.0, 105.0)

        app = YummyApp()
        result = app.get_nearby_restaurants()

        expected = [
            "Nha hang Pho Ly Quoc Su",
            "Bun cha Huong Lien"
        ]

        self.assertEqual(result, expected)
        mock_gps.assert_called_once_with()

    # TC06: GPS nam ngoai vung ho tro
    @patch("yummy_app.gps_service.get_current_location")
    def test_gps_outside_supported_area(self, mock_gps):
        mock_gps.return_value = (20.0, 110.0)

        app = YummyApp()
        result = app.get_nearby_restaurants()

        self.assertEqual(result, [])
        mock_gps.assert_called_once_with()

    # TC07: GPS bi mat tin hieu
    @patch("yummy_app.gps_service.get_current_location")
    def test_gps_signal_lost(self, mock_gps):
        mock_gps.side_effect = (
            gps_service.GPSSignalLostError(
                "GPS signal lost"
            )
        )

        app = YummyApp()
        result = app.get_nearby_restaurants()

        self.assertEqual(
            result,
            "Khong the xac dinh vi tri."
        )
        mock_gps.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()