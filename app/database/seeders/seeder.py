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
            data = Users(email='admin@gmail.com', username='Admin Account', role='admin')
            data.set_password(password='AdMin123')
            data2 = Users(email='fajar@gmail.com', username='Fajar PB', role='admin')
            data2.set_password(password='fajar')
            db.session.add(data)
            db.session.add(data2) 
            db.session.commit()
            
    # Activities seeder
    def activities(): 
        if not Activities.query.first():
            data = Activities(
                    user_id = 1,
                    factor_id= 1,
                    amount= 10,
                    activity_date= datetime.now(),
                    report_date= datetime.now()
                )
            db.session.add(data)
            db.session.commit()
    
    # Sources seeder
    def sources():
        if not Sources.query.first():
            data = Sources(source_name="Pabrik Manufaktur", description="Emisi co2 Pabrik Manufaktur")
            db.session.add(data)
            db.session.commit()
        
    # Emissions seeder
    def emissions():
        if not Emissions.query.first():
            data = Emissions(
                    user_id=1,
                    source_id=1,
                    amount=1,
                    emission_date=datetime.now(),
                    report_date=datetime.now()
                )
            db.session.add(data)
            db.session.commit()
    
    # Carbon factor seeder
    def carbonFactor():
        if not CarbonFactors.query.first():
            data = CarbonFactors(
                    source_id=1,
                    description="1 Ton Kwh per co2",
                    conversion_factor=1,
                    unit="Ton"
                )
            db.session.add(data)
            db.session.commit()
        
    # Goals seeder
    def goals():
        if not Goals.query.first():
            data = Goals(
                    user_id=1,
                    target_emission=504,
                    deadline=datetime.now()
                )
            db.session.add(data)
            db.session.commit()
        
    # Offsets seeder
    def offsets():
        if not Offsets.query.first():
            data = Offsets(
                    user_id=1,
                    project_name="Penanaman 1000 bibit Pohon Jati",
                    offset_amount=90,
                    offset_date=datetime.now()
                )
            db.session.add(data)
            db.session.commit()
        
    # reports seeder
    def reports():
        if not Reports.query.first():
            data = Reports(
                    user_id=1,
                    start_date=datetime.now() - timedelta(days=1),
                    end_date=datetime.now() + timedelta(days=5),
                    total_emission=120
                )
            db.session.add(data)
            db.session.commit()
            
    users()
    sources()
    carbonFactor()
    activities()
    emissions()
    goals()
    offsets()
    reports()
    