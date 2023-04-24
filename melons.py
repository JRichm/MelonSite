import csv
csvFile ='./melons.csv'
melon_dict = {}

class Melon:
    def __init__(self, melon_id, common_name, price, image_url, color, seedless):
        self.melon_id = melon_id
        self.common_name = common_name
        self.price = price
        self.image_url =image_url
        self.color =color
        self.seedless = seedless
        
    def __repr__(self):
        return( f'<Melon: {self.melon_id}, {self.common_name}>')
    
    def price_str(self):
        return f'${self.price:.2f}'
    

def get_melon_by_id(melon_id):
    return melon_dict[melon_id]
    
def get_all():
    return list(melon_dict.values)
        
def printCSV(csv_file):
    with open(csv_file) as storeMelons:
        reader = csv.DictReader(storeMelons)
        reader = list(reader)
        
    for each in reader:
        print(each)
        melon_id = each['melon_id']
        newMelon = Melon(melon_id,
                         each['common_name'],
                         float(each['price']),
                         each['image_url'],
                         each['color'],
                         eval(each['seedless']))
        
        melon_dict[melon_id] = melon
        
printCSV(csvFile)