class LocationFinder:
    def __init__(self):
        self.coordinates = {
            "A":  (10.8532733433, 106.7715069217), # Khu C
            "BB": (10.852302    , 106.771424    ), # Khu D
            "B":  (10.8514838933, 106.7713101400),
            "TT": (10.8512819350, 106.7719588833), # Toa trung Tam
            "C":  (10.851238    , 106.772669), 
            "CC": (10.851554    , 106.772746), # Toa Viet Duc
            "D":  (10.851198    , 106.773302),
            "DD": (10.851641    , 106.773369), # Maker Space
            "E":  (10.852292    , 106.773450),
            "F":  (10.852364    , 106.772835),
            "G":  (10.853240    , 106.772932), # Go
            "H":  (10.853319    , 106.772592),
            "I":  (10.853541    , 106.772572),
            "K":  (10.853686    , 106.771636),
        }
        
        self.name_mapping = {
            "khu c": "A",
            "khu d": "BB",
            "toa trung tam": "TT",
            "toa viet duc": "CC",
            "maker space": "DD",
            "go": "G"
        }

    def get_key(self, name):
        return self.name_mapping.get(name.lower(), "Không tìm thấy")

if __name__ == "__main__":
    finder = LocationFinder()
    name = input("Nhập tên khu vực: ")
    print(f"Mã khu vực: {finder.get_key(name)}")