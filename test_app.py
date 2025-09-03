import unittest
from app import validate_donation_amount, app

class TestDonationValidation(unittest.TestCase):
    
    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_amount_less_than_1_should_fail(self):
        """Test that amounts less than 1 fail validation"""
        # Test with 0
        is_valid, error_msg = validate_donation_amount(0)
        self.assertFalse(is_valid)
        self.assertIn("at least $1", error_msg)
        
        # Test with negative number
        is_valid, error_msg = validate_donation_amount(-5)
        self.assertFalse(is_valid)
        self.assertIn("at least $1", error_msg)
        
        # Test with 0.5
        is_valid, error_msg = validate_donation_amount(0.5)
        self.assertFalse(is_valid)
        self.assertIn("at least $1", error_msg)
        
        # Test with 0.99
        is_valid, error_msg = validate_donation_amount(0.99)
        self.assertFalse(is_valid)
        self.assertIn("at least $1", error_msg)
    
    def test_amount_greater_than_100_should_fail(self):
        """Test that amounts greater than 100 fail validation"""
        # Test with 101
        is_valid, error_msg = validate_donation_amount(101)
        self.assertFalse(is_valid)
        self.assertIn("cannot exceed $100", error_msg)
        
        # Test with 200
        is_valid, error_msg = validate_donation_amount(200)
        self.assertFalse(is_valid)
        self.assertIn("cannot exceed $100", error_msg)
        
        # Test with 100.01
        is_valid, error_msg = validate_donation_amount(100.01)
        self.assertFalse(is_valid)
        self.assertIn("cannot exceed $100", error_msg)
    
    def test_valid_amounts_should_pass(self):
        """Test that valid amounts (1-100) pass validation"""
        valid_amounts = [1, 1.0, 1.5, 10, 25.50, 50, 99.99, 100]
        
        for amount in valid_amounts:
            with self.subTest(amount=amount):
                is_valid, error_msg = validate_donation_amount(amount)
                self.assertTrue(is_valid, f"Amount {amount} should be valid")
                self.assertIsNone(error_msg)
    
    def test_invalid_input_types_should_fail(self):
        """Test that invalid input types fail validation"""
        invalid_inputs = ["abc", "", "ten", None, "1.5.3", "1,000"]
        
        for invalid_input in invalid_inputs:
            with self.subTest(input=invalid_input):
                is_valid, error_msg = validate_donation_amount(invalid_input)
                self.assertFalse(is_valid)
                self.assertIn("valid number", error_msg)
    
    def test_boundary_values(self):
        """Test boundary values"""
        # Test exact boundary values
        is_valid, error_msg = validate_donation_amount(1)
        self.assertTrue(is_valid)
        self.assertIsNone(error_msg)
        
        is_valid, error_msg = validate_donation_amount(100)
        self.assertTrue(is_valid)
        self.assertIsNone(error_msg)
    
    def test_string_numbers(self):
        """Test string representations of numbers"""
        # Valid string numbers
        is_valid, error_msg = validate_donation_amount("50")
        self.assertTrue(is_valid)
        self.assertIsNone(error_msg)
        
        is_valid, error_msg = validate_donation_amount("25.75")
        self.assertTrue(is_valid)
        self.assertIsNone(error_msg)
        
        is_valid, error_msg = validate_donation_amount("0.5")
        self.assertFalse(is_valid)
        
        is_valid, error_msg = validate_donation_amount("150")
        self.assertFalse(is_valid)

class TestFlaskRoutes(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_blog_page_loads(self):
        """Test that blog page loads successfully"""
        response = self.app.get('/blog')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Blog Posts', response.data)
        self.assertIn(b'Support Our Blog', response.data)
    
    def test_donation_form_validation_via_post(self):
        response = self.app.post('/donate', data={'amount': '0.5'}, follow_redirects=True)
        self.assertIn(b'at least $1', response.data)
        
        response = self.app.post('/donate', data={'amount': '150'}, follow_redirects=True)
        self.assertIn(b'cannot exceed $100', response.data)
        
        response = self.app.post('/donate', data={'amount': '25.50'}, follow_redirects=True)
        self.assertIn(b'Thank you for your donation', response.data)

if __name__ == '__main__':
    unittest.main(verbosity=2)
