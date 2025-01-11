from app.extensions import *
from app import db
from app.database.models.Users import Users 
from app.database.models.Activities import Activities
from app.database.models.Carbon_factors import CarbonFactors
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
            
    # Activities seeder
    def activities(): 
        if not Activities.query.first():
            data = Activities(
                    user_id = 3,
                    factor_id= 1,
                    amount= 10,
                    activity_date= datetime.now(),
                    report_date= datetime.now()
                )
            data2 = Activities(
                    user_id = 2,
                    factor_id= 2,
                    amount= 30,
                    activity_date= datetime.now(),
                    report_date= datetime.now()
                )
            db.session.add(data)
            db.session.add(data2)
            db.session.commit()
    
    # Sources seeder
    def sources():
        if not Sources.query.first():
            data = Sources(source_name="Pabrik", description="Emisi pabrik")
            data2 = Sources(source_name="Kendaraan", description="Emisi kendaraan")
            db.session.add(data)
            db.session.add(data2)
            db.session.commit()
        
    # Emissions seeder
    def emissions():
        if not Emissions.query.first():
            data = Emissions(
                    user_id=3,
                    source_id=1,
                    amount=10,
                    emission_date=datetime.now(),
                    report_date=datetime.now()
                )
            data2 = Emissions(
                    user_id=2,
                    source_id=2,
                    amount=30,
                    emission_date=datetime.now(),
                    report_date=datetime.now()
                )
            db.session.add(data)
            db.session.add(data2)
            db.session.commit()
    
    # Carbon factor seeder
    def carbonFactor():
        if not CarbonFactors.query.first():
            data = CarbonFactors(
                    source_id=1,
                    description="1 Liter per co2",
                    conversion_factor=1,
                    unit="Liter"
                )
            data2 = CarbonFactors(
                    source_id=2,
                    description="1 Kwh per co2",
                    conversion_factor=1,
                    unit="Kwh"
                )
            db.session.add(data)
            db.session.add(data2)
            db.session.commit()
        
    # Goals seeder
    def goals():
        if not Goals.query.first():
            data = Goals(
                    user_id=3,
                    target_emission=504,
                    deadline=datetime.now()
                )
            data2 = Goals(
                    user_id=2,
                    target_emission=1200,
                    deadline=datetime.now()
                )
            db.session.add(data)
            db.session.add(data2)
            db.session.commit()
        
    # Offsets seeder
    def offsets():
        if not Offsets.query.first():
            data = Offsets(
                    user_id=2,
                    project_name="Penanaman 1000 bibit Pohon Jati",
                    offset_amount=90,
                    offset_date=datetime.now()
                )
            data2 = Offsets(
                    user_id=3,
                    project_name="Penanaman 1000 pohon sawit",
                    offset_amount=120,
                    offset_date=datetime.now()
                )
            db.session.add(data)
            db.session.add(data2)
            db.session.commit()
        
    # reports seeder
    def reports():
        if not Reports.query.first():
            data = Reports(
                    user_id=3,
                    start_date=datetime.now() - timedelta(days=1),
                    end_date=datetime.now() + timedelta(days=7),
                    total_emission=120
                )
            data2 = Reports(
                    user_id=2,
                    start_date=datetime.now() - timedelta(days=1),
                    end_date=datetime.now() + timedelta(days=5),
                    total_emission=140
                )
            db.session.add(data)
            db.session.add(data2)
            db.session.commit()
            
    users()
    sources()
    carbonFactor()
    activities()
    emissions()
    goals()
    offsets()
    reports()
    