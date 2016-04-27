from . import doctor

@doctor.route('/')
def home():
    return 'Admin Page'