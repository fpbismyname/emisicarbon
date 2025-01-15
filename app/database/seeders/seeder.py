from app.extensions import *

def seed():    
    # List of data for seeding
    # users data
    usersData = [{
        "username" : "Admin Emisi Karbon",
        "email" : "admin@gmail.com",
        "password_hash" : generate_password('111'),
        "role" : "admin",
        "created_at" : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    },{
        "username" : "Garuda Company",
        "email" : "garudacompany@business.com",
        "password_hash" : generate_password('garuda256'),
        "role" : "company",
        "created_at" : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    },{
        "username" : "Steven Beam",
        "email" : "steven@gmail.com",
        "password_hash" : generate_password('steven256'),
        "role" : "user",
        "created_at" : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }]
    # sources data
    sourcesData = [{
        "source_id" : 1,
        "source_name" : "Pertanian",
        "description" : "Emisi yang ditimbulkan dari aktivitas pertanian tertentu",
        "created_at" : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    },{
        "source_id" : 2,
        "source_name" : "Pabrik",
        "description" : "Emisi yang ditimbulkan dari aktivitas pabrik tertentu",
        "created_at" : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    },{
        "source_id" : 3,
        "source_name" : "Transportasi",
        "description" : "Emisi yang ditimbulkan dari aktivitas transportasi",
        "created_at" : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }]
    # carbon factor data
    carbonFactorsData = [{
        "source_id" : 1,
        "description" : "1.2 Liter per kg CO2",
        "conversion_factor" : 1.2,
        "unit" : "Liter per kg CO2",
    },{
        "source_id" : 2,
        "description" : "12 Kwh per kg CO2",
        "conversion_factor" : 12,
        "unit" : "Kwh per kg CO2",
    },{
        "source_id" : 3,
        "description" : "20 km/h per kg CO2",
        "conversion_factor" : 20,
        "unit" : "km/h per kg CO2",
    }]
    
    # List of table database for seeding process
    listSeed = json.dumps([{
        "users" : usersData,
        "sources" : sourcesData,
        "carbon_factors" : carbonFactorsData,
    }])
    
    # Seeding process
    listData = json.loads(listSeed)
    for table_name, table_value in listData[0].items():
        try:
            if table_name == "Users":
                from app.database.models.Users import Users
                data = Users(username=table_value.username, email=table_value.email)
                data.password_hash = table_value.password_hash
                db.session.add(data)
                db.session.commit()
            else:
                metadata = MetaData()
                table = Table(table_name, metadata, autoload_with=db.engine)
                db.session.execute(table.insert().values(table_value))
        except IntegrityError:
            click.echo(f" > Duplicated detected data entry '{table_name}'")
            db.session.rollback()
    db.session.commit()