from app import db, application
from app.models import base_model


class Device(base_model.BaseModel):
    """
    Device model class
    """
    __tablename__ = "devices"
    device_id = db.Column(db.String(50), primary_key=True)
    brand = db.Column(db.String(50))
    board = db.Column(db.String(50))
    build_id = db.Column(db.String(100))
    creation_date = db.Column(db.Date())
    device = db.Column(db.String(50))
    hardware = db.Column(db.String(50))
    manufacturer = db.Column(db.String(50))
    model = db.Column(db.String(50))
    release = db.Column(db.String(50))
    release_type = db.Column(db.String(50))
    product = db.Column(db.String(50))
    sdk = db.Column(db.Integer)
    events = db.relationship("Event", backref="device", lazy="dynamic")
    traffic_events = db.relationship("TrafficEvent", backref="device", lazy="dynamic")
    application_traffic_events = db.relationship("ApplicationTrafficEvent", backref="device", lazy="dynamic")
    mobile_traffic_events = db.relationship("MobileTrafficEvent", backref="device", lazy="dynamic")
    wifi_traffic_events = db.relationship("WifiTrafficEvent", backref="device", lazy="dynamic")
    telephony_events = db.relationship("TelephonyObservationEvent", backref="device", lazy="dynamic")
    gsm_events = db.relationship("GsmEvent", backref="device", lazy="dynamic")
    cdma_events = db.relationship("CdmaEvent", backref="device", lazy="dynamic")
    connectivity_events = db.relationship("ConnectivityEvent", backref="device", lazy="dynamic")
    state_change_events = db.relationship("StateChangeEvent", backref="device", lazy="dynamic")

    def __init__(self, device_id, brand=None, board=None, build_id=None, device=None, hardware=None,
                 manufacturer=None, model=None, release=None, release_type=None, product=None, sdk=None,
                 creation_date=None):
        self.device_id = device_id
        self.brand = brand
        self.board = board
        self.build_id = build_id
        self.device = device
        self.hardware = hardware
        self.manufacturer = manufacturer
        self.model = model
        self.release = release
        self.release_type = release_type
        self.product = product
        self.sdk = sdk
        self.creation_date = creation_date

    def __repr__(self):
        return "<Device %r, device_id %r>" % (self.device, self.device_id)

    @staticmethod
    def get_device_or_add_it(args):
        """
        Search a device and retrieve it if exist, else create a new one and retrieve it adding it in a new session.
        """
        from datetime import datetime
        if "device_id" in args:
            device = Device.query.filter(Device.device_id == args["device_id"]).first()
            if not device:
                device = Device(
                    device_id=args["device_id"],
                    brand=args["brand"],
                    board=args["board"],
                    build_id=args["build_id"],
                    device=args["device"],
                    hardware=args["hardware"],
                    manufacturer=args["manufacturer"],
                    model=args["model"],
                    release=args["release"],
                    release_type=args["release_type"],
                    product=args["product"],
                    sdk=args["sdk"],
                    creation_date=datetime.now())
                db.session.add(device)
                try:
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    application.logger.error("Error adding device to database - " + str(e))
            return device
        else:
            return None
