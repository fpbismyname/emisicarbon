from app.extensions import *
from app import db
from app.database.models.Users import Users 
from app.database.models.Activities import Activities
from app.database.models.Carbonfactors import CarbonFactors
from app.database.models.Emissions import Emissions
from app.database.models.Goals import Goals
from app.database.models.Offsets import Offsets
from app.database.models.Reports import Reports
from app.database.models.Sources import Sources
def seed():
    
    # Users seeder
    def users():
        if not Users.query.first():
            data = Users(email='admin@gmail.com', username='Admin Emisi', role='admin')
            data.set_password(password='admin256')
            data2 = Users(email='garudacompany@gmail.com', username='Garuda Company', role='company')
            data2.set_password(password='garuda256')
            data3 = Users(email='steven@gmail.com', username='Steven Beam', role='user')
            data3.set_password(password='steven256')
            db.session.add(data)
            db.session.add(data2)
            db.session.add(data3)
            db.session.commit()
            
    # Sources seeder
    def sources():
        if not Sources.query.first():
            data = Sources(source_name="Pabrik", description="Emisi pabrik")
            data2 = Sources(source_name="Kendaraan", description="Emisi kendaraan")
            db.session.add(data)
            db.session.add(data2)
            db.session.commit()
        
    # Carbon factor seeder
    def carbonFactor():
        if not CarbonFactors.query.first():
            data = CarbonFactors(
                    source_id=1,
                    description="0.5 Liter",
                    conversion_factor=0.5,
                    unit="Liter"
                )
            data2 = CarbonFactors(
                    source_id=2,
                    description="0.8 Liter",
                    conversion_factor=0.8,
                    unit="Km/h"
                )
            db.session.add(data)
            db.session.add(data2)
            db.session.commit()
    
    # Call all seeder
    users()
    sources()
    carbonFactor()