from http.server import HTTPServer, BaseHTTPRequestHandler
import xgboost as xgb
import pandas as pd
import json
import hashlib

import warnings
warnings.filterwarnings("ignore")

with open("utils/features.json", 'r') as f:
    column_names = json.load(f)

with open("utils/stats.json", 'r') as f:
    stats = json.load(f)

class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):

        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))
        
        post_data = json.loads(post_data)

        
        if len(post_data) == 20:   
            predicted_price = process_data(post_data)
            response = {'predicted_price': predicted_price}
        else:                       
            car_info = process(post_data)
            retrain_left = retrain(car_info)
            response = {'retrain_left' : retrain_left}

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        json_response = json.dumps(response)
        self.wfile.write(json_response.encode())

def process_data(features):
    
    car_info = process(features)            # return dataframe for prediction
    predicted_price = predict(car_info)
    predicted_price = predicted_price.tolist()
    predicted_price = predicted_price[0]
    return predicted_price

def process(features):

    manufacturer = features[0]
    model = features[1]
    year = features[2]
    mileage = features[3]
    mpg = features[4]

    transmission = features[5]
    cylinders = features[6]
    injection_type = features[7]
    horsepower = features[8]
    turbo = features[9]

    drivetrain = features[10]
    fuel_type = features[11]
    exterior_color = features[12]
    interior_color = features[13]
    seller_rating = features[14]

    driver_rating = features[15]
    driver_reviews_num = features[16]
    accidents = features[17]
    one_owner = features[18]
    personal_use = features[19]

    if len(features) == 21:
        actual_price = features[20]

    zeros = {col: 0 for col in column_names}
    car_info = pd.DataFrame([zeros])

    # 1- Manufacturer
    car_info.loc[0, 'manufacturer_' + manufacturer] = 1

    # 2- Model
    found = False
    for col in car_info.columns:
        if "model_" + model == col:
            car_info.loc[0, col] = 1
            found = True

    if not found:
        car_info.loc[0, 'model_Other'] = 1
    
    # 3- Year
    found = False
    for col in car_info.columns:
        if "year_" + year == col:
            car_info.loc[0, col] = 1
            found = True

    if not found:
        car_info.loc[0, 'year_Other'] = 1
    
    # 4- Mileage
    car_info['mileage'] = car_info['mileage'].astype(float)
    car_info.loc[0, 'mileage'] = (float(mileage) - stats['mileage'][0]) / stats['mileage'][1]

    # 5- MPG
    car_info['mpg'] = car_info['mpg'].astype(float)
    car_info.loc[0, 'mpg'] = (float(mpg) - stats['mpg'][0]) / stats['mpg'][1]

    # 6- Transmission
    car_info.loc[0, 'transmission_' + transmission] = 1

    # 7- Cylinders
    if cylinders != 'Other':
        cylinders += '.0'

    car_info.loc[0, 'cylinders_' + cylinders] = 1

    # 8- Injection Type
    car_info.loc[0, 'injection_type_' + injection_type] = 1

    # 9- Horsepower
    car_info['horsepower'] = car_info['horsepower'].astype(float)
    car_info.loc[0, 'horsepower'] = (float(horsepower) - stats['horsepower'][0]) / stats['horsepower'][1]

    # 10- Turbo 
    car_info.loc[0, 'turbo_' + turbo] = 1

    # 11- Drivetrain
    car_info.loc[0, 'drivetrain_' + drivetrain] = 1

    # 12- Fuel type
    car_info.loc[0, 'fuel_type_' + fuel_type.lower()] = 1

    # 13- Exterior Color
    car_info.loc[0, 'exterior_color_' + exterior_color.lower()] = 1

    # 14- Interior Color
    car_info.loc[0, 'interior_color_' + interior_color.lower()] = 1
    
    # 15- Seller Rating
    car_info['seller_rating'] = car_info['seller_rating'].astype(float)
    car_info.loc[0, 'seller_rating'] = (float(seller_rating) - stats['seller_rating'][0]) / stats['seller_rating'][1]

    # 16- Driver Rating
    car_info['driver_rating'] = car_info['driver_rating'].astype(float)
    car_info.loc[0, 'driver_rating'] = (float(driver_rating) - stats['driver_rating'][0]) / stats['driver_rating'][1]

    # 17- Driver Reviews Num
    car_info['driver_reviews_num'] = car_info['driver_reviews_num'].astype(float)
    car_info.loc[0, 'driver_reviews_num'] = (float(driver_reviews_num) - stats['driver_reviews_num'][0]) / stats['driver_reviews_num'][1]

    # 18- Accidents
    car_info.loc[0, 'accidents_or_damage_' + accidents] = 1

    # 19- One Owner  
    car_info.loc[0, 'one_owner_' + one_owner] = 1

    # 20- Personal Use
    car_info.loc[0, 'personal_use_only_' + personal_use] = 1

    # removing outliers
    for col in car_info.columns:
        if car_info[col].dtype in ['int64', 'float64']:  
            if car_info[col].nunique() > 2:  
                    car_info[col] = car_info[col].clip(lower=-2, upper=2)
    
    
    if len(features) == 21:
        car_info['price'] = float(actual_price)
    else:
        car_info.drop(columns=['price'], inplace=True)

    return car_info

def predict(car_info):
    model = xgb.Booster()
    model.load_model('utils/xgboost_custom.model')
    dmatrix = xgb.DMatrix(car_info)
    predicted_price = model.predict(dmatrix)
    return predicted_price

model_hash = None

samples = []

def retrain(car_info):
    global samples 

    samples.append(car_info)
    print("\n", len(samples), "training samples waiting in queue")

    if len(samples) >= 3:
        print("\nRetraining in progress!\n")

        model = xgb.Booster()
        model.load_model('utils/xgboost_custom.model')

        training_instances = pd.concat(samples)
        X_train = training_instances.drop(columns=['price']) 
        y_train = training_instances['price']

        dmatrix = xgb.DMatrix(X_train, label=y_train)
        model.update(dmatrix, iteration=100)

        model_hash_before = hashlib.md5(open('utils/xgboost_custom.model', 'rb').read()).hexdigest()
        model.save_model('utils/xgboost_custom.model')
        model_hash_after = hashlib.md5(open('utils/xgboost_custom.model', 'rb').read()).hexdigest()
        
        if model_hash_before != model_hash_after:
            print("-- Model file has been updated --")
        else:
            print("-- Model file hasn't been updated --")

        model_hash = model_hash_after
        samples = []  

# else:
#     print("\nThe data is already present!")

    return len(samples)

if __name__ == '__main__':
    server_address = ('localhost', 5500)
    httpd = HTTPServer(server_address, MyHandler)
    print(f'Starting server at http://{server_address[0]}:{server_address[1]}')
    httpd.serve_forever()
