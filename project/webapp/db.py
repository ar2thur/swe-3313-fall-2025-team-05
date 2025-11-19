import click
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


@click.command("init-db")
def init_db():
    """Create all database tables, if they do not exist."""

    # This must be imported here to prevent circular imports
    from webapp import create_app
    import webapp.models

    app = create_app()

    with app.app_context():
        db.create_all()
        click.echo("Database initialized.")



@click.command("seed-db")
def seed_db():
    """Adds seed data to database after its initialized."""

    from webapp import create_app
    from webapp.models import User, InventoryItem, Logistics

    app = create_app()

    with app.app_context():

        if not User.query.filter_by(email="ronsemail@example.com").first():
            ron = User(
                name="Ron Swanson",
                password="36e230203d860d1d34654e0c3ece4b3b9a26c22aec43648256adf57dbbdbaede",
                email="ronsemail@example.org",
                is_admin=True
            )

            inventory = [
                InventoryItem(
                    is_available=True,
                    name="F16 Viper",
                    description=(
                        """
                        A lightweight, highly maneuverable multirole fighter 
                        designed for air superiority and precision strike missions. 
                        Known for its agility, advanced avionics, and reliable operational 
                        performance across diverse combat environments.
                        """
                    ),
                    cost=27_000_000_000,
                    picture_path="NULL"
                ),
                InventoryItem(
                    is_available=True,
                    name="F22 Raptor",
                    description=(
                        """
                        A fifth-generation stealth air superiority fighter
                        featuring unmatched maneuverability, advanced sensor 
                        fusion, and supercruise capability. Designed to dominate 
                        contested airspace with precision and survivability.
                        """
                    ),
                    cost=35_000_000_000,
                    picture_path="NULL"
                ),
                InventoryItem(
                    is_available=True,
                    name="F35 Lightning II",
                    description=(
                        """
                        A cutting-edge multirole stealth aircraft built for 
                        strike, intelligence, and electronic warfare missions. 
                        Integrates next-generation sensors, networked data sharing, 
                        and short-takeoff capabilities depending on variant.
                        """
                    ),
                    cost=8_250_000_000,
                    picture_path="NULL"
                ),
                InventoryItem(
                    is_available=True,
                    name="C17 Globemaster",
                    description=(
                        """
                        A strategic transport aircraft built to carry large 
                        payloads across intercontinental distances. Capable 
                        of rapid deployments, airdrops, and operations on short 
                        or unprepared runways.
                        """
                    ),
                    cost=900_000_000,
                    picture_path="NULL"
                ),
                InventoryItem(
                    is_available=True,
                    name="F15 Strike Eagle",
                    description=(
                        """
                        A twin-engine, long-range, all-weather fighter that 
                        delivers exceptional speed and payload capacity. Optimized 
                        for deep-strike missions while maintaining strong air-to-air 
                        capability.
                        """
                    ),
                    cost=870_000_000,
                    picture_path="NULL"
                ),
                InventoryItem(
                    is_available=True,
                    name="ATACMS",
                    description=(
                        """
                        A long-range, precision-guided surface-to-surface missile 
                        capable of neutralizing high-value targets at extended distances. 
                        Known for its speed, accuracy, and destructive payload.
                        """
                    ),
                    cost=100_000_000,
                    picture_path="NULL"
                ),
                InventoryItem(
                    is_available=True,
                    name="PrSM",
                    description=(
                        """
                        A next-generation long-range strike missile offering extended 
                        reach and advanced guidance. Designed to provide precision engagement 
                        against strategic ground targets with improved lethality and flexibility.
                        """
                    ),
                    cost=1_100_000_000,
                    picture_path="NULL"
                ),
                InventoryItem(
                    is_available=True,
                    name="UH-60 Black Hawk",
                    description=(
                        """
                        A versatile, highly durable utility helicopter used for troop transport, 
                        medevac, and cargo missions. Recognized for its reliability, maneuverability, 
                        and performance in demanding environments.
                        """
                    ),
                    cost=1_000_000_000,
                    picture_path="NULL"
                )
            ]

            logsitics = Logistics() # This defaults all columns to our needed seed data

            db.session.add(ron)
            db.session.add(logsitics)
            db.session.add_all(inventory)

            db.session.commit()

            click.echo("Added all seed data to database.")




