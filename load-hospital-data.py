import json
import boto3
import argparse

def load_hospitals(tableName):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(tableName)
    
    with open('data/hospital-data.json', 'r') as myfile:
        data=myfile.read()
    
    hospitals = json.loads(data)
    newid = 0
    with table.batch_writer() as batch:
        for hospital in hospitals["items"]:
            newid += 1
            num_licensed_beds = -1
            if 'num_licensed_beds' in hospital:
                num_licensed_beds = hospital['num_licensed_beds']
                
            num_staffed_beds = -1
            if 'num_staffed_beds' in hospital:
                num_staffed_beds = hospital['num_staffed_beds']
                
            avg_ventilator_usage = -1
            if 'avg_ventilator_usage' in hospital:
                avg_ventilator_usage = hospital['avg_ventilator_usage']
                
            state_fips = -1
            if 'state_fips' in hospital:
                state_fips = hospital['state_fips']
                
            cnty_fips = -1
            if 'cnty_fips' in hospital:
                cnty_fips = hospital['cnty_fips']
            
            fips = -1
            if 'fips' in hospital:
                fips = hospital['fips']

            batch.put_item(Item={
                'id': newid,
                'hospital_name': hospital['hospital_name'],
                'hospital_type': hospital['hospital_type'],
                'hq_address': hospital['hq_address'],
                'hq_address1': hospital['hq_address1'],
                'hq_city': hospital['hq_city'],
                'hq_state': hospital['hq_state'],
                'hq_zip_code': hospital['hq_zip_code'],
                'county_name': hospital['county_name'],
                'state_name': hospital['state_name'],
                'state_fips': state_fips,
                'cnty_fips': cnty_fips,
                'fips': fips,
                'num_licensed_beds': num_licensed_beds,
                'num_staffed_beds': num_staffed_beds,
                'num_icu_beds': hospital['num_icu_beds'],
                'adult_icu_beds': hospital['adult_icu_beds'],
                'avg_ventilator_usage': avg_ventilator_usage,
                'potential_increase_in_bed_capac': hospital['potential_increase_in_bed_capac']}
            )
            
#def create_data_catalog():
    
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--tableName')
    args = parser.parse_args()
    load_hospitals(args.tableName)
        