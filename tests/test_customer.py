def test_customer_initial_state(sample_customer):
    assert sample_customer.name == "Anna"
    assert sample_customer.email == "anna@test.com"
    assert sample_customer.city == "Warszawa"
    assert sample_customer.is_active == True

def test_customer_can_be_deactivated(sample_customer):
    sample_customer.deactivate()
    assert sample_customer.is_active == False

def test_customer_starts_active(sample_customer):
    assert sample_customer.is_active == True

