class SpotTypeChoices:
    STREET = "S"
    SHOP = "$"
    PARK = "P"
    DIY = "D"
    # Krak has Private and Work in Progress, but I don't see the point
    # Their tag of Famous is kinda cool. Don't know about the Famous and Minute tags.

    CHOICES = (
        (STREET, "Street"),
        (SHOP, "Shop"),
        (PARK, "Skatepark"),
        (DIY, "DIY"),
    )
