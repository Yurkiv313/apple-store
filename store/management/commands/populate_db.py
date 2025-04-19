from django.core.management.base import BaseCommand
from store.models import Category, Product
from decimal import Decimal
import random


class Command(BaseCommand):
    help = "Populate the database with demo categories and products"

    def handle(self, *args, **kwargs):
        self.stdout.write("⛔ Clean data...")
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write("✅ Create category...")
        categories = {
            "Apple Smartphones": Category.objects.create(
                name="Apple Smartphones",
                description=(
                    "Discover the latest range of Apple smartphones, "
                    "including iPhone models with advanced features, "
                    "stunning displays, and powerful performance."
                ),
            ),
            "Apple Laptops": Category.objects.create(
                name="Apple Laptops",
                description=(
                    "Explore Apple's lineup of laptops including the "
                    "MacBook Air and MacBook Pro, built for speed, "
                    "reliability, and creativity."
                ),
            ),
            "Apple Earphones": Category.objects.create(
                name="Apple Earphones",
                description=(
                    "Experience immersive sound with Apple earphones "
                    "including AirPods and AirPods Pro — seamless "
                    "connectivity and crystal-clear audio."
                ),
            ),
            "Smart Watches": Category.objects.create(
                name="Smart Watches",
                description=(
                    "Stay connected and track your health with Apple "
                    "Watch and other wearables. Smart technology for "
                    "an active lifestyle."
                ),
            ),
        }

        smartphones = [
            ("iPhone 13", 899, "3240", "6.1", "Pink"),
            ("iPhone 13 mini", 799, "2406", "5.4", "Midnight"),
            ("iPhone 13 Pro", 999, "3095", "6.1", "Graphite"),
            ("iPhone 13 Pro Max", 1099, "4352", "6.7", "Sierra Blue"),
            ("iPhone 14", 999, "3279", "6.1", "Red"),
            ("iPhone 14 Plus", 1099, "4325", "6.7", "Starlight"),
            ("iPhone 14 Pro", 1199, "3200", "6.1", "Deep Purple"),
            ("iPhone 14 Pro Max", 1299, "4323", "6.7", "Space Black"),
            ("iPhone 15", 1099, "3300", "6.1", "Blue"),
            ("iPhone 15 Plus", 1199, "4383", "6.7", "Green"),
            ("iPhone 15 Pro", 1299, "3400", "6.1", "Natural Titanium"),
            ("iPhone 15 Pro Max", 1399, "4422", "6.7", "White Titanium"),
            ("iPhone 13 Alpine", 899, "3240", "6.1", "Alpine Green"),
            ("iPhone 14 Yellow", 999, "3279", "6.1", "Yellow"),
            ("iPhone 14 Blue", 999, "3279", "6.1", "Blue"),
            ("iPhone 15 Pink", 1099, "3300", "6.1", "Pink"),
            ("iPhone 15 Black", 1099, "3300", "6.1", "Black"),
            ("iPhone 13 RED", 899, "3240", "6.1", "Red"),
            ("iPhone 14 Pro Gold", 1199, "3200", "6.1", "Gold"),
            ("iPhone 15 Pro Max Blue", 1399, "4422", "6.7", "Blue Titanium"),
        ]

        laptops = [
            ("MacBook Air M1", 999, "4379", "13.3", "Space Gray"),
            ("MacBook Pro M1", 1299, "5120", "13.3", "Silver"),
            ("MacBook Air M2", 1199, "4300", "13.6", "Midnight"),
            ("MacBook Pro M2", 1499, "5500", "13.6", "Silver"),
            ("MacBook Pro 14", 1999, "6000", "14.2", "Space Gray"),
            ("MacBook Pro 16", 2499, "8000", "16.2", "Silver"),
            ("MacBook Air Retina", 1099, "4500", "13.3", "Gold"),
            ("MacBook 12-inch", 899, "4000", "12", "Rose Gold"),
            ("MacBook Pro Intel 13", 1299, "5000", "13.3", "Silver"),
            ("MacBook Pro Intel 15", 1799, "7200", "15.4", "Space Gray"),
            ("MacBook Air 2017", 749, "3500", "13.3", "Silver"),
            ("MacBook Pro 2016", 999, "4500", "13.3", "Space Gray"),
            ("MacBook Pro 2015", 899, "4200", "15.4", "Silver"),
            ("MacBook 2016", 799, "4100", "12", "Rose Gold"),
            ("MacBook Pro M3", 1899, "6800", "14.2", "Space Black"),
            ("MacBook Air M3", 1599, "4700", "13.6", "Silver"),
            ("MacBook Pro Touch Bar", 1499, "5200", "13.3", "Gray"),
            ("MacBook Air Gold", 999, "4300", "13.3", "Gold"),
            ("MacBook Pro Silver", 1399, "5000", "14", "Silver"),
            ("MacBook Pro Midnight", 1699, "5500", "14", "Midnight"),
        ]

        earphones = [
            ("AirPods 2nd Gen", 129, "", "", "White"),
            ("AirPods 3rd Gen", 179, "", "", "White"),
            ("AirPods Pro", 249, "", "", "White"),
            ("AirPods Pro 2", 299, "", "", "White"),
            ("AirPods Max", 549, "", "", "Space Gray"),
            ("EarPods Lightning", 29, "", "", "White"),
            ("Beats Fit Pro", 199, "", "", "Black"),
            ("Beats Studio Buds", 149, "", "", "Red"),
            ("Beats Solo3", 199, "", "", "Black"),
            ("Powerbeats Pro", 249, "", "", "Navy"),
            ("AirPods SE", 99, "", "", "White"),
            ("AirPods Lite", 79, "", "", "White"),
            ("AirPods Max Blue", 549, "", "", "Blue"),
            ("AirPods Max Pink", 549, "", "", "Pink"),
            ("AirPods Pro MagSafe", 269, "", "", "White"),
            ("BeatsX", 129, "", "", "Black"),
            ("AirPods Pro Lite", 229, "", "", "White"),
            ("EarPods USB-C", 29, "", "", "White"),
            ("Beats Studio Pro", 329, "", "", "Black"),
            ("AirPods Max Silver", 549, "", "", "Silver"),
        ]

        watches = [
            ("Apple Watch Series 3", 199, "", "1.5", "Silver"),
            ("Apple Watch Series 4", 249, "", "1.78", "Black"),
            ("Apple Watch Series 5", 299, "", "1.78", "Gold"),
            ("Apple Watch SE", 279, "", "1.78", "Silver"),
            ("Apple Watch Series 6", 399, "", "1.78", "Red"),
            ("Apple Watch Series 7", 429, "", "1.9", "Blue"),
            ("Apple Watch Series 8", 449, "", "1.9", "Pink"),
            ("Apple Watch Ultra", 799, "", "1.99", "Titanium"),
            ("Apple Watch Ultra 2", 899, "", "1.99", "Titanium"),
            ("Apple Watch Nike", 399, "", "1.78", "Black"),
            ("Apple Watch Hermes", 1299, "", "1.78", "Silver"),
            ("Apple Watch Edition", 1499, "", "1.78", "Graphite"),
            ("Apple Watch SE 2", 329, "", "1.78", "White"),
            ("Apple Watch Gold", 499, "", "1.78", "Gold"),
            ("Apple Watch Blue", 499, "", "1.78", "Blue"),
            ("Apple Watch Pink", 499, "", "1.78", "Pink"),
            ("Apple Watch Starlight", 529, "", "1.78", "Starlight"),
            ("Apple Watch Space Black", 599, "", "1.78", "Space Black"),
            ("Apple Watch Silver", 459, "", "1.78", "Silver"),
            ("Apple Watch Midnight", 489, "", "1.78", "Midnight"),
        ]

        def get_random_memory(category_name):
            if category_name == "Apple Smartphones":
                return random.choice(["128GB", "256GB", "512GB", "1TB"])
            elif category_name == "Apple Laptops":
                return random.choice(["256GB", "512GB", "1TB"])
            elif category_name == "Apple Earphones":
                return random.choice(["N/A", "Built-in 16GB"])
            elif category_name == "Smart Watches":
                return random.choice(["32GB", "64GB", "128GB"])
            return "N/A"

        def create_products(product_list, category):
            for name, price, battery, screen, color in product_list:
                memory = get_random_memory(category.name)

                if category.name == "Apple Smartphones":
                    description = f"""
                    <h3>{name} - The Perfect Balance of Power and Elegance</h3>
                    <p>The {name} in stunning {color} delivers exceptional
                    performance with its:</p>
                    <ul>
                        <li>Brilliant {screen}-inch Super Retina XDR display</li>
                        <li>Powerful A15/A16 Bionic chip</li>
                        <li>Advanced dual/triple camera system</li>
                        <li>All-day battery life ({battery}mAh)</li>
                        <li>Ample {memory} storage</li>
                        <li>Industry-leading IP68 water resistance</li>
                    </ul>
                    <p>Experience the future of mobile technology with Face ID,
                    5G connectivity, and the most secure mobile platform.</p>
                    """
                elif category.name == "Apple Laptops":
                    description = f"""
                    <h3>{name} - Redefining Portable Computing</h3>
                    <p>The {name} in elegant {color} offers:</p>
                    <ul>
                        <li>Stunning {screen}-inch Retina display</li>
                        <li>Breakthrough M1/M2 chip</li>
                        <li>Up to 18 hours of battery life</li>
                        <li>Spacious {memory} SSD storage</li>
                        <li>Magic Keyboard</li>
                        <li>Advanced cooling system</li>
                    </ul>
                    <p>Perfect for professionals, students, and creatives.</p>
                    """
                elif category.name == "Apple Earphones":
                    description = f"""
                    <h3>{name} - Immersive Sound, Effortless Experience</h3>
                    <p>The {name} in classic {color} features:</p>
                    <ul>
                        <li>Active Noise Cancellation</li>
                        <li>Adaptive EQ</li>
                        <li>Spatial audio</li>
                        <li>Water resistant design</li>
                        <li>Up to 6 hours battery</li>
                        <li>Quick access to Siri</li>
                    </ul>
                    <p>Experience music and calls like never before.</p>
                    """
                elif category.name == "Smart Watches":
                    description = f"""
                    <h3>{name} - Your Essential Health Companion</h3>
                    <p>The {name} in beautiful {color} offers:</p>
                    <ul>
                        <li>Bright {screen}-inch Retina display</li>
                        <li>Advanced health monitoring</li>
                        <li>Powerful S8/S9 chip</li>
                        <li>{memory} storage</li>
                        <li>Water resistance up to 50m</li>
                        <li>Thousands of apps</li>
                    </ul>
                    <p>Stay connected and track your health.</p>
                    """
                else:
                    description = f"{name} — high-quality Apple product."

                Product.objects.create(
                    name=name,
                    price=Decimal(price),
                    category=category,
                    memory=memory,
                    battery_capacity=battery,
                    screen_size=screen,
                    color=color,
                    description=description,
                )

        create_products(smartphones, categories["Apple Smartphones"])
        create_products(laptops, categories["Apple Laptops"])
        create_products(earphones, categories["Apple Earphones"])
        create_products(watches, categories["Smart Watches"])

        self.stdout.write(
            self.style.SUCCESS("✅ Database population completed.")
        )
