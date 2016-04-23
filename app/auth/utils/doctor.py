def get_doctor_by_id(id):
    from ..models import Doctor
    return Doctor.query.filter_by(id=id).first()
