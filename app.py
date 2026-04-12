import os
import stripe
from flask import Flask
from database import db
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    stripe.api_key = app.config["STRIPE_SECRET_KEY"]
    for folder in [app.config["UPLOAD_FOLDER"],app.config["DOWNLOAD_FOLDER"],
                   os.path.join(app.config["UPLOAD_FOLDER"],"beats"),
                   os.path.join(app.config["UPLOAD_FOLDER"],"covers"),
                   os.path.join(app.config["UPLOAD_FOLDER"],"products")]:
        os.makedirs(folder,exist_ok=True)
    from routes.main     import main_bp
    from routes.beats    import beats_bp
    from routes.services import services_bp
    from routes.store    import store_bp
    from routes.payments import payments_bp
    from routes.admin    import admin_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(beats_bp,url_prefix="/beats")
    app.register_blueprint(services_bp,url_prefix="/services")
    app.register_blueprint(store_bp,url_prefix="/store")
    app.register_blueprint(payments_bp,url_prefix="/payments")
    app.register_blueprint(admin_bp,url_prefix="/admin")
    with app.app_context():
        db.create_all()
        # Seed R2 MP3 URLs for all beats
        try:
            r2_urls = {
        'Afterlife': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Afterlife%20%5B117BPM%20A%23%20Min%5D.mp3',
        'All that pain': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/All%20that%20pain%20%5B99BPM%20A%20Maj%5D.mp3',
        'Alone again': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Alone%20again%20%5B62BPM%20A%20Min%5D.mp3',
        'Always tired': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Always%20tired%20%5B92BPM%20F%20Maj%5D.mp3',
        'Ambition': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Ambition%20%5B108BPM%20A%23%20Min%5D.mp3',
        'American murder': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/American%20murder%20%5B81BPM%20A%20Min%5D.mp3',
        'Angels Fly': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Angels%20Fly%20%5B161BPM%20D%20Min%5D.mp3',
        'Atmosphere': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Atmosphere%20%5B99BPM%20D%23%20Maj%5D.mp3',
        "Baby I can't change": 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Baby%20I%20can%27t%20change%20%5B117BPM%20A%20Maj%5D.mp3',
        "Baby please don't go": 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Baby%20please%20don%27t%20go%20%5B136BPM%20E%20Maj%5D.mp3',
        'Backwoods Drip': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Backwoods%20Drip%20%5B76BPM%20E%20Maj%5D.mp3',
        'Bartender': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Bartender%20%5B108BPM%20A%20Min%5D.mp3',
        'Blessings': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Blessings%20%5B96BPM%20F%20Min%5D.mp3',
        'Block Runner': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Block%20Runner%20%5B117BPM%20A%20Min%5D.mp3',
        'Blue Collar Flex': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Blue%20Collar%20Flex%20%5B108BPM%20E%20Min%5D.mp3',
        'Bodies drop': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Bodies%20drop%2092%20E%20minor%20%5B123BPM%20A%20Min%5D.mp3',
        'Bounce back harder': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Bounce%20back%20harder%20%5B117BPM%20F%20Maj%5D.mp3',
        'Brick & Echo': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Brick%20%26%20Echo%20%5B100BPM%20A%23%20Maj%5D.mp3',
        'Call me whenever': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Call%20me%20whenever%2078%20Eminor%20%5B103BPM%20E%20Min%5D.mp3',
        'Cemetery': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Cemetery%2088%20Eminor%20%5B172BPM%20E%20Min%5D.mp3',
        'Chicago wind': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Chicago%20wind%20%5B112BPM%20F%20Min%5D.mp3',
        'Cigarette smoke': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Cigarette%20smoke%2090%20Fmin%20%5B92BPM%20F%20Maj%5D.mp3',
        'Concrete Gospel': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Concrete%20Gospel%20%5B108BPM%20A%20Maj%5D.mp3',
        'Cracks in the ceiling': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Cracks%20in%20the%20ceiling%20%5B103BPM%20D%23%20Maj%5D.mp3',
        'DND in Tokyo': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/DND%20in%20Tokyo%20%5B100BPM%20F%20Maj%5D.mp3',
        'Diary of a musician': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Diary%20of%20a%20musician%20%5B108BPM%20A%23%20Min%5D.mp3',
        'Dirt Road Diamonds': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Dirt%20Road%20Diamonds%20%5B76BPM%20E%20Maj%5D.mp3',
        "Don't call me": 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Don%27t%20call%20me%20%5B92BPM%20F%20Min%5D.mp3',
        'Don’t leave now': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Don%E2%80%99t%20leave%20now%20%5B86BPM%20A%23%20Min%5D.mp3',
        'Drivin on E': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Drivin%20on%20E%20%5B99BPM%20D%20Maj%5D.mp3',
        'Drugs are bad': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Drugs%20are%20bad%20%5B103BPM%20F%23%20Min%5D.mp3',
        'Emotional lockdown': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Emotional%20lockdown%2090%20Fmin%20%5B92BPM%20C%20Min%5D.mp3',
        'Fallen enemies': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Fallen%20enemies%20%5B103BPM%20E%20Min%5D.mp3',
        'Fame': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Fame%20%5B99BPM%20A%23%20Min%5D.mp3',
        'Family business': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Family%20business%20%5B108BPM%20E%20Min%5D.mp3',
        'Fight': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Fight%20%5B92BPM%20A%23%20Maj%5D.mp3',
        'Finale': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Finale%20%5B117BPM%20F%20Maj%5D.mp3',
        'Fire Sign': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Fire%20Sign%20%5B89BPM%20B%20Min%5D.mp3',
        'Flight to LA': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Flight%20to%20LA%20%5B117BPM%20D%20Maj%5D.mp3',
        'Fraud life': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Fraud%20life%20%5B117BPM%20F%20Min%5D.mp3',
        'Free ninety nine': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Free%20ninety%20nine%20%5B92BPM%20F%20Maj%5D.mp3',
        'Fuck it': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Fuck%20it%20%5B117BPM%20E%20Min%5D.mp3',
        'G unified': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/G%20unified%20%5B89BPM%20F%20Maj%5D.mp3',
        'GPS': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/GPS%20%5B144BPM%20A%20Maj%5D.mp3',
        'Gangster Blues': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Gangster%20Blues%20%5B83BPM%20B%20Min%5D.mp3',
        'Gave It My All': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Gave%20It%20My%20All%20%5B100BPM%20F%20Maj%5D.mp3',
        'Get up': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Get%20up%20%5B103BPM%20E%20Min%5D.mp3',
        'Ghosts': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Ghosts%20%5B129BPM%20A%20Maj%5D.mp3',
        'Good die young': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Good%20die%20young%20%5B103BPM%20E%20Min%5D.mp3',
        'Graduation': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Graduation%20%5B117BPM%20E%20Min%5D.mp3',
        'Gravel & Gold': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Gravel%20%26%20Gold%20%5B89BPM%20E%20Min%5D.mp3',
        'Greatness in my blood': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Greatness%20in%20my%20blood%20%5B117BPM%20F%20Maj%5D.mp3',
        'Grind season': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Grind%20season%20%5B108BPM%20E%20Min%5D.mp3',
        'Guns in the guitar case': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Guns%20in%20the%20guitar%20case%20%5B108BPM%20F%20Maj%5D.mp3',
        'Haters': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Haters%20%5B92BPM%20E%20Maj%5D.mp3',
        'Heaven sent': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Heaven%20sent%2064%20Eminor%20%5B86BPM%20A%20Min%5D.mp3',
        'Heights': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Heights%20%5B108BPM%20E%20Maj%5D.mp3',
        'Hellfire club': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Hellfire%20club%20%5B62BPM%20F%20Maj%5D.mp3',
        'Hollywood Ghosts': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Hollywood%20Ghosts%20%5B108BPM%20B%20Min%5D.mp3',
        'Hometown hero': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Hometown%20hero%20%5B92BPM%20E%20Min%5D.mp3',
        "I'm Good": 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/I%27m%20Good%20%5B103BPM%20D%23%20Maj%5D.mp3',
        'Insecurities': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Insecurities%20%5B108BPM%20A%23%20Min%5D.mp3',
        'Jansport': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Jansport%2098%20Ab%20Minor%20%5B100BPM%20A%20Maj%5D.mp3',
        'Last soul': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Last%20soul%2074%20Fminor%20%5B99BPM%20C%20Maj%5D.mp3',
        'Late night drive': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Late%20night%20drive%20%5B92BPM%20A%20Maj%5D.mp3',
        'Late nights': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Late%20nights%20%5B92BPM%20A%23%20Min%5D.mp3',
        'Leave it alone': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Leave%20it%20alone%20%5B86BPM%20A%20Maj%5D.mp3',
        'Lessons on Lessons': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Lessons%20on%20Lessons%20%5B96BPM%20A%20Maj%5D.mp3',
        'Let go': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Let%20go%20%5B123BPM%20F%23%20Min%5D.mp3',
        'Level 9000': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Level%209000%2067%20Ebminor%20%5B89BPM%20A%23%20Maj%5D.mp3',
        'Lexus': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Lexus%20%5B112BPM%20A%23%20Min%5D.mp3',
        'Lifes good wby': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Lifes%20good%20wby%2073%20B%20minor%20%5B96BPM%20A%20Maj%5D.mp3',
        'Love like no other': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Love%20like%20no%20other%20%5B123BPM%20A%20Maj%5D.mp3',
        'Love my life': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Love%20my%20life%20%5B99BPM%20D%20Maj%5D.mp3',
        'Lovin you every way': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Lovin%20you%20every%20way%20%5B83BPM%20B%20Min%5D.mp3',
        'MacBeatTag (1)': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/MacBeatTag%20%281%29%20%5B144BPM%20F%23%20Min%5D.mp3',
        'Mind Right': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Mind%20Right%20%5B92BPM%20F%23%20Min%5D.mp3',
        'Mission Beach': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Mission%20Beach%20%5B112BPM%20E%20Maj%5D.mp3',
        'Momma raised a G': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Momma%20raised%20a%20G%20%5B96BPM%20F%20Maj%5D.mp3',
        'Moonlight in Mexico': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Moonlight%20in%20Mexico%20%5B99BPM%20A%20Min%5D.mp3',
        'Moonshine Money': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Moonshine%20Money%20%5B108BPM%20E%20Min%5D.mp3',
        'Never forget': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Never%20forget%20%5B129BPM%20D%20Maj%5D.mp3',
        'Never give up': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Never%20give%20up%20%5B112BPM%20F%23%20Maj%5D.mp3',
        'Nevermind the City': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Nevermind%20the%20City%20%5B96BPM%20F%20Maj%5D.mp3',
        'New city': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/New%20city%20%5B96BPM%20D%20Maj%5D.mp3',
        'No Assistance': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/No%20Assistance%20%5B92BPM%20A%23%20Min%5D.mp3',
        'No Time For Breaks': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/No%20Time%20For%20Breaks%20%5B86BPM%20A%23%20Maj%5D.mp3',
        'No interference': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/No%20interference%20%5B62BPM%20F%23%20Min%5D.mp3',
        'No love lost': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/No%20love%20lost%20%5B86BPM%20A%20Min%5D.mp3',
        'No rules in this game': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/No%20rules%20in%20this%20game%20%5B86BPM%20D%20Maj%5D.mp3',
        'Not for the Weak': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Not%20for%20the%20Weak%20%5B86BPM%20A%23%20Min%5D.mp3',
        'On my way home': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/On%20my%20way%20home%20%5B86BPM%20A%23%20Min%5D.mp3',
        'Outlaw 808s': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Outlaw%20808s%20%5B78BPM%20G%20Min%5D.mp3',
        'Outlaw life': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Outlaw%20life%20%5B99BPM%20E%20Maj%5D.mp3',
        'Peace of mind': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Peace%20of%20mind%20%5B99BPM%20B%20Min%5D.mp3',
        'Pickup Truck Gospel': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Pickup%20Truck%20Gospel%20%5B117BPM%20A%20Min%5D.mp3',
        'Places I go': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Places%20I%20go%20%5B112BPM%20F%20Maj%5D.mp3',
        'Places to go': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Places%20to%20go%20%5B129BPM%20E%20Maj%5D.mp3',
        'Pour one': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Pour%20one%20%5B92BPM%20G%23%20Maj%5D.mp3',
        'Radio': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Radio%20%5B108BPM%20A%23%20Maj%5D.mp3',
        'Ramen diet': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Ramen%20diet%20%5B86BPM%20A%23%20Min%5D.mp3',
        'Reality Check': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Reality%20Check%20%5B86BPM%20A%20Min%5D.mp3',
        'River flow': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/River%20flow%20%5B92BPM%20E%20Min%5D.mp3',
        'Runnin From the Jakes': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Runnin%20From%20the%20Jakes%20%5B100BPM%20A%23%20Maj%5D.mp3',
        'Sauce Pourin': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Sauce%20Pourin%20%5B172BPM%20A%20Maj%5D.mp3',
        'Say something in code': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Say%20something%20in%20code%2090%20E%20minor%20%5B117BPM%20E%20Min%5D.mp3',
        'Shotgun & Subwoofers': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Shotgun%20%26%20Subwoofers%20%5B99BPM%20D%20Maj%5D.mp3',
        'Sideways': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Sideways%20%5B92BPM%20A%23%20Min%5D.mp3',
        'Signal': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Signal%2067%20Dbminor%20%5B89BPM%20A%20Maj%5D.mp3',
        'Sing for the moment': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Sing%20for%20the%20moment%20%5B62BPM%20D%20Maj%5D.mp3',
        'Sleepless nights': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Sleepless%20nights%20%5B112BPM%20E%20Min%5D.mp3',
        'Small Town Big Drums': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Small%20Town%20Big%20Drums%20%5B108BPM%20D%20Maj%5D.mp3',
        'Sold my soul': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Sold%20my%20soul%20%5B117BPM%20F%20Min%5D.mp3',
        'Souls': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Souls%20%5B92BPM%20A%20Min%5D.mp3',
        'Start Again': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Start%20Again%20%5B103BPM%20A%23%20Min%5D.mp3',
        'Stolen Kia': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Stolen%20Kia%20%5B172BPM%20F%20Maj%5D.mp3',
        'Strange things': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Strange%20things%20%5B62BPM%20A%23%20Maj%5D.mp3',
        'Swipin Socials': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Swipin%20Socials%20%5B92BPM%20F%20Maj%5D.mp3',
        'Switch on': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Switch%20on%20%5B89BPM%20E%20Min%5D.mp3',
        'Take no more': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Take%20no%20more%20%5B172BPM%20A%20Min%5D.mp3',
        'Takeoff': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Takeoff%20%5B108BPM%20F%20Maj%5D.mp3',
        'Taquilla takes the pain away': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Taquilla%20takes%20the%20pain%20away%20%5B96BPM%20B%20Min%5D.mp3',
        'The Hood Love Me': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/The%20Hood%20Love%20Me%20%5B92BPM%20A%20Min%5D.mp3',
        'The fall off': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/The%20fall%20off%20%5B96BPM%20E%20Min%5D.mp3',
        'This time it’s real': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/This%20time%20it%E2%80%99s%20real%20%5B99BPM%20A%20Maj%5D.mp3',
        'Throwing ones': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Throwing%20ones%20%5B70BPM%20E%20Min%5D.mp3',
        'Timeless': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Timeless%2098%20F%20minor%20%5B129BPM%20C%20Maj%5D.mp3',
        'Told you so': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Told%20you%20so%20%5B108BPM%20A%20Min%5D.mp3',
        'Touch grass': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Touch%20grass%2087%20Ebminor%20%5B86BPM%20A%23%20Maj%5D.mp3',
        'Venice Beach': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Venice%20Beach%20%5B86BPM%20A%23%20Min%5D.mp3',
        'Version of me': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Version%20of%20me%20%5B103BPM%20A%23%20Min%5D.mp3',
        'Vintage feel': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Vintage%20feel%2087%20Db%20minor%20%5B172BPM%20G%23%20Min%5D.mp3',
        'Vision Blurry': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Vision%20Blurry%20%5B92BPM%20A%23%20Maj%5D.mp3',
        'Waffle House': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Waffle%20House%20%5B108BPM%20F%23%20Min%5D.mp3',
        'We Win': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/We%20Win%20%5B86BPM%20F%23%20Min%5D.mp3',
        "What's the point?": 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/What%27s%20the%20point%3F%20%5B161BPM%20A%20Min%5D.mp3',
        'What’s wrong': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/What%E2%80%99s%20wrong%20%5B96BPM%20A%20Min%5D.mp3',
        "Where'd you go?": 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Where%27d%20you%20go%3F%20%5B92BPM%20F%20Maj%5D.mp3',
        'Whiskey in the Trap': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Whiskey%20in%20the%20Trap%20%5B62BPM%20A%20Min%5D.mp3',
        'Wicked city': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Wicked%20city%20%5B99BPM%20A%20Min%5D.mp3',
        'Window shopping': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Window%20shopping%20%5B92BPM%20C%23%20Min%5D.mp3',
        'Windy city gang': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Windy%20city%20gang%2083%20Db%20minor%20%5B172BPM%20C%23%20Min%5D.mp3',
        'Winners circle': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Winners%20circle%20%5B117BPM%20F%23%20Min%5D.mp3',
        'Wire Transfer': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Wire%20Transfer%20%5B76BPM%20F%20Maj%5D.mp3',
        'World': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/World%20%5B108BPM%20A%20Min%5D.mp3',
        'Write it down': 'https://pub-3d8b1c7a5e63475b90c0044ca074cba8.r2.dev/Write%20it%20down%20%5B83BPM%20A%23%20Maj%5D.mp3'
            }
            seeded = 0
            for b in Beat.query.all():
                if b.title in r2_urls and (not b.mp3_path or not b.mp3_path.startswith('https://pub-')):
                    b.mp3_path = r2_urls[b.title]
                    seeded += 1
            if seeded:
                db.session.commit()
                print(f'[startup] seeded {seeded} R2 URLs')
        except Exception as _r2e:
            db.session.rollback()

        from models import Product
        try:
            if not Product.query.filter_by(name="The Artist Is The Business").first():
                db.session.add(Product(product_type="digital",
                    name="The Artist Is The Business",
                    description="The complete independent artist blueprint. 9 chapters covering branding, income streams, organic growth, AI leverage, and a 90-day execution plan.",
                    price=27,tags="ebook,artist development,strategy",
                    file_path="uploads/products/artist-is-the-business-v2.html",
                    is_active=True,is_new=True))
                db.session.commit()
        except Exception:
            db.session.rollback()
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True,port=5000)
