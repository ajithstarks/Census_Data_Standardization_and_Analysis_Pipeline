# %%
# Ensure necessary libraries are installed
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

libraries = [
    'pandas',
    'pymongo',
    'streamlit',
    'mysql-connector-python',
    'python-docx',
    'requests'
]

for lib in libraries:
    try:
        __import__(lib)
    except ImportError:
        install(lib)

# Now, import the libraries
import pandas as pd
import pymongo
import streamlit as st
import mysql.connector
import requests
from io import BytesIO
from docx import Document


# %%
def connect_mysql():
    try:
        # Replace these variables with your MySQL connection details
        username = 'project'
        password = 'Project-321'
        hostname = 'localhost'
        database_name = 'census_2011'

        # Connect to MySQL database
        mysql_connection = mysql.connector.connect(
            host=hostname,
            user=username,
            password=password,
            database=database_name
        )
        print("MySQL connection established successfully.")
        return mysql_connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        st.error(f"Error connecting to MySQL: {err}")
        return None


# %%
# Connect to MongoDB
def connect_mongo():
    try:
        uri = "mongodb+srv://project:Project321@myatlasclusteredu.43hutqm.mongodb.net/?retryWrites=true&w=majority&appName=myAtlasClusterEDU"
        mongo_client = pymongo.MongoClient(uri)
        db=mongo_client['census']
        collection = db["census"]
        print("MongoDB connection established successfully.")
        return collection
    except Exception as e:
        print(f"An error occurred while connecting to MongoDB: {e}")
        st.error(f"An error occurred while connecting to MongoDB: {e}")
        return None


# %%
# Upload the docx file into data frame
def fetch_docx(doc_url):
    # Fetching the docx file from GitHub
    response = requests.get(doc_url)
    docx_bytes = BytesIO(response.content)
    # Creating a Document object
    doc = Document(docx_bytes)
    # Extracting data from the docx file
    data = [paragraph.text for paragraph in doc.paragraphs]
    return data

# %%
# Fetch data from URLs
def get_raw_data():
    try:
        # Attempt to fetch data from URLs
        data_url = "https://github.com/ajithstarks/dataset/raw/main/census_2011.xlsx"
        doc_url = "https://github.com/ajithstarks/dataset/raw/main/Telangana.docx"
        df = pd.read_excel(data_url)
        df1 = fetch_docx(doc_url)
    except Exception as e:
        # If fetching fails, handle the error and fallback to local files
        print(f"An error occurred while fetching data from URLs: {e}")
        print("Fetching from local files...")
        try:
            df = pd.read_excel(r"E:\Data Engineer\capstone_project_files\census_2011.xlsx")
            df1 = [
                "Adilabad", 
                "Nizamabad", 
                "Karimnagar", 
                "Medak", 
                "Hyderabad", 
                "Rangareddy", 
                "Mahbubnagar", 
                "Nalgonda", 
                "Warangal", 
                "Khammam"
            ]
            print("Data fetched from local files successfully.")
        except Exception as e:
            # If local file reading also fails, raise the error
            print(f"An error occurred while fetching local files: {e}")
            return None, None
    return df, df1
#df, df1 = get_raw_data()

# %%
# Rename the columns
def rename_columns(df):
    # Define the mapping of old column names to new column names
    column_mapping = {
        'District code': 'DistrictID',
        'State name': 'StateName',
        'District name': 'DistrictName',
        'Population': 'Population',
        'Male': 'Male',
        'Female': 'Female',
        'Literate': 'Literate',
        'Male_Literate': 'MaleLiterate',
        'Female_Literate': 'FemaleLiterate',
        'SC': 'SC',
        'Male_SC': 'MaleSC',
        'Female_SC': 'FemaleSC',
        'ST': 'ST',
        'Male_ST': 'MaleST',
        'Female_ST': 'FemaleST',
        'Workers': 'Workers',
        'Male_Workers': 'MaleWorkers',
        'Female_Workers': 'FemaleWorkers',
        'Main_Workers': 'MainWorkers',
        'Marginal_Workers': 'MarginalWorkers',
        'Non_Workers': 'NonWorkers',
        'Cultivator_Workers': 'CultivatorWorkers',
        'Agricultural_Workers': 'AgrWorkers',
        'Household_Workers': 'HHWorkers',
        'Other_Workers': 'OtherWorkers',
        'Hindus': 'Hindus',
        'Muslims': 'Muslims',
        'Christians': 'Christians',
        'Sikhs': 'Sikhs',
        'Buddhists': 'Buddhists',
        'Jains': 'Jains',
        'Others_Religions': 'Others_Religions',
        'Religion_Not_Stated': 'RelNotStated',
        'LPG_or_PNG_Households': 'LPGHH',
        'Housholds_with_Electric_Lighting': 'ElecLightHH',
        'Households_with_Internet': 'InternetHH',
        'Households_with_Computer': 'ComputerHH',
        'Rural_Households': 'RuralHH',
        'Urban_Households': 'UrbanHH',
        'Households': 'TotalHH',
        'Below_Primary_Education': 'BelowPrimaryEdu',
        'Primary_Education': 'PrimaryEdu',
        'Middle_Education': 'MiddleEdu',
        'Secondary_Education': 'SecondaryEdu',
        'Higher_Education': 'HigherEdu',
        'Graduate_Education': 'GradEdu',
        'Other_Education': 'OtherEdu',
        'Literate_Education': 'LitEdu',
        'Illiterate_Education': 'IllitEdu',
        'Total_Education': 'TotalEdu',
        'Age_Group_0_29': 'AgeGroup0_29',
        'Age_Group_30_49': 'AgeGroup30_49',
        'Age_Group_50': 'AgeGroup50',
        'Age not stated': 'AgeNotStated',
        'Households_with_Bicycle': 'BicycleHH',
        'Households_with_Car_Jeep_Van': 'CarJeepVanHH',
        'Households_with_Radio_Transistor': 'RadioTransHH',
        'Households_with_Scooter_Motorcycle_Moped': 'ScooterMotorMopedHH',
        'Households_with_Telephone_Mobile_Phone_Landline_only': 'PhoneLandlineHH',
        'Households_with_Telephone_Mobile_Phone_Mobile_only': 'MobileOnlyHH',
        'Households_with_TV_Computer_Laptop_Telephone_mobile_phone_and_Scooter_Car': 'TVCompLaptopHH',
        'Households_with_Television': 'TVHH',
        'Households_with_Telephone_Mobile_Phone': 'PhoneHH',
        'Households_with_Telephone_Mobile_Phone_Both': 'PhoneBothHH',
        'Condition_of_occupied_census_houses_Dilapidated_Households': 'DilapHouseHH',
        'Households_with_separate_kitchen_Cooking_inside_house': 'SepKitchenHH',
        'Having_bathing_facility_Total_Households': 'BathFacHH',
        'Having_latrine_facility_within_the_premises_Total_Households': 'LatrineFacHH',
        'Ownership_Owned_Households': 'OwnedHH',
        'Ownership_Rented_Households': 'RentedHH',
        'Type_of_bathing_facility_Enclosure_without_roof_Households': 'BathFacEnclosureHH',
        'Type_of_fuel_used_for_cooking_Any_other_Households': 'OtherFuelHH',
        'Type_of_latrine_facility_Pit_latrine_Households': 'PitLatrineHH',
        'Type_of_latrine_facility_Other_latrine_Households': 'OtherLatrineHH',
        'Type_of_latrine_facility_Night_soil_disposed_into_open_drain_Households': 'NightSoilLatrineHH',
        'Type_of_latrine_facility_Flush_pour_flush_latrine_connected_to_other_system_Households': 'FlushLatrineHH',
        'Not_having_bathing_facility_within_the_premises_Total_Households': 'NoBathFacHH',
        'Not_having_latrine_facility_within_the_premises_Alternative_source_Open_Households': 'NoLatrineFacHH',
        'Main_source_of_drinking_water_Un_covered_well_Households': 'UncoveredWellWaterHH',
        'Main_source_of_drinking_water_Handpump_Tubewell_Borewell_Households': 'HandpumpWaterHH',
        'Main_source_of_drinking_water_Spring_Households': 'SpringWaterHH',
        'Main_source_of_drinking_water_River_Canal_Households': 'RiverCanalWaterHH',
        'Main_source_of_drinking_water_Other_sources_Households': 'OtherWaterHH',
        'Main_source_of_drinking_water_Other_sources_Spring_River': 'OtherWaterHH_River',
        'Location_of_drinking_water_source_Near_the_premises_Households': 'NearPremisesWaterHH',
        'Location_of_drinking_water_source_Within_the_premises_Households': 'WithinPremisesWaterHH',
        'Main_source_of_drinking_water_Tank_Pond_Lake_Households': 'PondLakeWaterHH',
        'Main_source_of_drinking_water_Tapwater_Households': 'TapWaterHH',
        'Main_source_of_drinking_water_Tubewell_Borehole_Households': 'BoreholeWaterHH',
        'Household_size_1_person_Households': 'HHSize1Person',
        'Household_size_2_persons_Households': 'HHSize2Persons',
        'Household_size_1_to_2_persons': 'HHSize1To2Persons',
        'Household_size_3_persons_Households': 'HHSize3Persons',
        'Household_size_3_to_5_persons_Households': 'HHSize3To5Persons',
        'Household_size_4_persons_Households': 'HHSize4Persons',
        'Household_size_5_persons_Households': 'HHSize5Persons',
        'Household_size_6_8_persons_Households': 'HHSize6_8Persons',
        'Household_size_9_persons_and_above_Households': 'HHSize9AbovePersons',
        'Location_of_drinking_water_source_Away_Households': 'AwayWaterSourceHH',
        'Married_couples_1_Households': 'MarriedCouple1HH',
        'Married_couples_2_Households': 'MarriedCouple2HH',
        'Married_couples_3_Households': 'MarriedCouple3HH',
        'Married_couples_3_or_more_Households': 'MarriedCouple3OrMoreHH',
        'Married_couples_4_Households': 'MarriedCouple4HH',
        'Married_couples_5__Households': 'MarriedCouple5HH',
        'Married_couples_None_Households': 'MarriedCoupleNoneHH',
        'Power_Parity_Less_than_Rs_45000': 'PowerParityLess45000',
        'Power_Parity_Rs_45000_90000': 'PowerParity45000_90000',
        'Power_Parity_Rs_90000_150000': 'PowerParity90000_150000',
        'Power_Parity_Rs_45000_150000': 'PowerParity45000_150000',
        'Power_Parity_Rs_150000_240000': 'PowerParity150000_240000',
        'Power_Parity_Rs_240000_330000': 'PowerParity240000_330000',
        'Power_Parity_Rs_150000_330000': 'PowerParity150000_330000',
        'Power_Parity_Rs_330000_425000': 'PowerParity330000_425000',
        'Power_Parity_Rs_425000_545000': 'PowerParity425000_545000',
        'Power_Parity_Rs_330000_545000': 'PowerParity330000_545000',
        'Power_Parity_Above_Rs_545000': 'PowerParityAbove545000',
        'Total_Power_Parity': 'TotalPowerParity'
    }

    # Rename the columns in the DataFrame
    df = df.rename(columns=column_mapping)
    return df

# Rename the columns using the function
#df = rename_columns(df)


# %%
# Function to process state names
def process_state_names(df, df1):
    # Function to format the state name
    def format_state_name(name):
        return ' '.join([word.capitalize() if word.lower() != 'and' else word.lower() for word in name.split()])

    # Apply the function to the 'StateName' column
    df['StateName'] = df['StateName'].apply(format_state_name)

    # Change the state names to Ladakh
    df.loc[(df['StateName'] == 'Jammu and Kashmir') & df['DistrictName'].str.contains('Leh|Kargil', case=False, na=False), 'StateName'] = 'Ladakh'

    # Change the state names to Telangana
    for district in df1:
        df.loc[df['DistrictName'].str.contains(district, case=False, na=False), 'StateName'] = 'Telangana'

    return df

#df = process_state_names(df, df1)


# %%
# Function to fill missing values and calculate missing percentage
def fill_missing_values_and_percentage(df):
    # Function to calculate the percentage of missing data for each column
    def calculate_missing_percentage(df):
        missing_percentage = df.isnull().sum() * 100 / len(df)
        return missing_percentage

    # Calculate missing data percentage before filling
    missing_percentage_before = calculate_missing_percentage(df)

    # Function to fill missing values
    def fill_missing_values(df):
        # Population = Male + Female
        if 'Population' in df.columns and 'Male' in df.columns and 'Female' in df.columns:
            df['Population'] = df['Population'].fillna(df['Male'] + df['Female'])

        # Literate = MaleLiterate + FemaleLiterate
        if 'MaleLiterate' in df.columns and 'FemaleLiterate' in df.columns:
            df['Literate'] = df['MaleLiterate'].fillna(0) + df['FemaleLiterate'].fillna(0)

        # Population = Young_and_Adult + Middle_Aged + Senior_Citizen + AgeNotStated
        if all(col in df.columns for col in ['Young_and_Adult', 'Middle_Aged', 'Senior_Citizen', 'AgeNotStated']):
            df['Population'] = df['Population'].fillna(df['Young_and_Adult'].fillna(0) + df['Middle_Aged'].fillna(0) + df['Senior_Citizen'].fillna(0) + df['AgeNotStated'].fillna(0))

        # Households = RuralHH + UrbanHH
        if 'RuralHH' in df.columns and 'UrbanHH' in df.columns:
            df['TotalHH'] = df['RuralHH'].fillna(0) + df['UrbanHH'].fillna(0)

        # SC = MaleSC + FemaleSC
        if 'SC' in df.columns and 'MaleSC' in df.columns and 'FemaleSC' in df.columns:
            df['SC'] = df['SC'].fillna(df['MaleSC'] + df['FemaleSC'])

        # ST = MaleST + FemaleST
        if 'ST' in df.columns and 'MaleST' in df.columns and 'FemaleST' in df.columns:
            df['ST'] = df['ST'].fillna(df['MaleST'] + df['FemaleST'])

        # Workers = MaleWorkers + FemaleWorkers
        if 'Workers' in df.columns and 'MaleWorkers' in df.columns and 'FemaleWorkers' in df.columns:
            df['Workers'] = df['Workers'].fillna(df['MaleWorkers'] + df['FemaleWorkers'])
        
        df.fillna(0, inplace=True)

        return df

    # Fill missing values
    df_filled = fill_missing_values(df)

    # Calculate missing data percentage after filling
    missing_percentage_after = calculate_missing_percentage(df_filled)

    # Compare the percentages before and after
    comparison = pd.DataFrame({
        'Before': missing_percentage_before,
        'After': missing_percentage_after,
        'Difference': missing_percentage_before - missing_percentage_after
    }).sort_values(by='Difference', ascending=False)

    return df_filled, comparison

# Fill missing values and get the percentage comparison
#df_filled, comparison = fill_missing_values_and_percentage(df)

# %%
# Function to load data to MongoDB
def load_data_to_mongodb(df_filled):
    try:
        # Convert DataFrame to dictionary format
        data_dict = df_filled.to_dict(orient='records')
        # Insert data into MongoDB
        connect_mongo().insert_many(data_dict)
        print("Data inserted into MongoDB successfully.")
    except Exception as e:
        print(f"An error occurred while loading data to MongoDB: {e}")

# Assuming df_filled is defined somewhere earlier in the code
#load_data_to_mongodb(df_filled)

# %%
def create_snowflake_star_schema():
    try:
        # Connect to MySQL using context manager
        with connect_mysql() as connection:
            if connection:
                # Create a cursor object using context manager
                with connection.cursor() as cursor:
                    # Define the schema creation queries
                    schema_queries = [
                        """DROP TABLE IF EXISTS Demographics""",
                        """DROP TABLE IF EXISTS District""",
                        """DROP TABLE IF EXISTS State""",
                        """
                        CREATE TABLE IF NOT EXISTS State (
                            StateID INT AUTO_INCREMENT PRIMARY KEY,
                            StateName VARCHAR(255) NOT NULL,
                            UNIQUE INDEX idx_statename (StateName)
                        )
                        """,
                        """
                        CREATE TABLE IF NOT EXISTS District (
                            DistrictID INT AUTO_INCREMENT PRIMARY KEY,
                            StateID INT,
                            DistrictName VARCHAR(255) NOT NULL,
                            Population FLOAT,
                            Male FLOAT,
                            Female FLOAT,
                            MaleLiterate FLOAT,
                            FemaleLiterate FLOAT,
                            INDEX idx_districtname (DistrictName),
                            INDEX idx_stateid (StateID),
                            FOREIGN KEY (StateID) REFERENCES State(StateID)
                        )
                        """,
                        """
                        CREATE TABLE IF NOT EXISTS Demographics (
                            DemographicsID INT AUTO_INCREMENT PRIMARY KEY,
                            DistrictID INT,
                            SC FLOAT,
                            MaleSC FLOAT,
                            FemaleSC FLOAT,
                            ST FLOAT,
                            MaleST FLOAT,
                            FemaleST FLOAT,
                            MainWorkers FLOAT,
                            MarginalWorkers FLOAT,
                            NonWorkers FLOAT,
                            CultivatorWorkers FLOAT,
                            AgrWorkers FLOAT,
                            HHWorkers FLOAT,
                            OtherWorkers FLOAT,
                            Hindus FLOAT,
                            Muslims FLOAT,
                            Christians FLOAT,
                            Sikhs FLOAT,
                            Buddhists FLOAT,
                            Jains FLOAT,
                            OtherReligions FLOAT,
                            RelNotStated FLOAT,
                            LPGHH FLOAT,
                            ElecLightHH FLOAT,
                            InternetHH FLOAT,
                            ComputerHH FLOAT,
                            RuralHH FLOAT,
                            UrbanHH FLOAT,
                            TotalHH FLOAT,
                            BelowPrimaryEdu FLOAT,
                            PrimaryEdu FLOAT,
                            MiddleEdu FLOAT,
                            SecondaryEdu FLOAT,
                            HigherEdu FLOAT,
                            GradEdu FLOAT,
                            OtherEdu FLOAT,
                            LitEdu FLOAT,
                            IllitEdu FLOAT,
                            TotalEdu FLOAT,
                            AgeGroup0_29 FLOAT,
                            AgeGroup30_49 FLOAT,
                            AgeGroup50 FLOAT,
                            AgeNotStated FLOAT,
                            BicycleHH FLOAT,
                            CarJeepVanHH FLOAT,
                            RadioTransHH FLOAT,
                            ScooterMotorMopedHH FLOAT,
                            PhoneLandlineHH FLOAT,
                            MobileOnlyHH FLOAT,
                            TVCompLaptopHH FLOAT,
                            TVHH FLOAT,
                            PhoneHH FLOAT,
                            PhoneBothHH FLOAT,
                            DilapHouseHH FLOAT,
                            SepKitchenHH FLOAT,
                            BathFacHH FLOAT,
                            LatrineFacHH FLOAT,
                            OwnedHH FLOAT,
                            RentedHH FLOAT,
                            BathFacEnclosureHH FLOAT,
                            OtherFuelHH FLOAT,
                            PitLatrineHH FLOAT,
                            OtherLatrineHH FLOAT,
                            NightSoilLatrineHH FLOAT,
                            FlushLatrineHH FLOAT,
                            NoBathFacHH FLOAT,
                            NoLatrineFacHH FLOAT,
                            UncoveredWellWaterHH FLOAT,
                            HandpumpWaterHH FLOAT,
                            SpringWaterHH FLOAT,
                            RiverCanalWaterHH FLOAT,
                            OtherWaterHH FLOAT,
                            NearPremisesWaterHH FLOAT,
                            WithinPremisesWaterHH FLOAT,
                            PondLakeWaterHH FLOAT,
                            TapWaterHH FLOAT,
                            BoreholeWaterHH FLOAT,
                            HHSize1Person FLOAT,
                            HHSize2Persons FLOAT,
                            HHSize1To2Persons FLOAT,
                            HHSize3Persons FLOAT,
                            HHSize3To5Persons FLOAT,
                            HHSize4Persons FLOAT,
                            HHSize5Persons FLOAT,
                            HHSize6_8Persons FLOAT,
                            HHSize9AbovePersons FLOAT,
                            AwayWaterSourceHH FLOAT,
                            MarriedCouple1HH FLOAT,
                            MarriedCouple2HH FLOAT,
                            MarriedCouple3HH FLOAT,
                            MarriedCouple3OrMoreHH FLOAT,
                            MarriedCouple4HH FLOAT,
                            MarriedCouple5HH FLOAT,
                            MarriedCoupleNoneHH FLOAT,
                            PowerParityLess45000 FLOAT,
                            PowerParity45000_90000 FLOAT,
                            PowerParity90000_150000 FLOAT,
                            PowerParity45000_150000 FLOAT,
                            PowerParity150000_240000 FLOAT,
                            PowerParity240000_330000 FLOAT,
                            PowerParity150000_330000 FLOAT,
                            PowerParity330000_425000 FLOAT,
                            PowerParity425000_545000 FLOAT,
                            PowerParity330000_545000 FLOAT,
                            PowerParityAbove545000 FLOAT,
                            TotalPowerParity FLOAT,
                            INDEX idx_demographics_districtid (DistrictID),
                            INDEX idx_mainworkers (MainWorkers),
                            INDEX idx_marginalworkers (MarginalWorkers),
                            INDEX idx_totalhh (TotalHH),
                            INDEX idx_lpg_hh (LPGHH),
                            INDEX idx_hindus (Hindus),
                            INDEX idx_muslims (Muslims),
                            INDEX idx_christians (Christians),
                            INDEX idx_sikhs (Sikhs),
                            INDEX idx_buddhists (Buddhists),
                            INDEX idx_jains (Jains),
                            INDEX idx_otherreligions (OtherReligions),
                            INDEX idx_internet_hh (InternetHH),
                            INDEX idx_belowprimaryedu (BelowPrimaryEdu),
                            INDEX idx_primaryedu (PrimaryEdu),
                            INDEX idx_middleedu (MiddleEdu),
                            INDEX idx_secondaryedu (SecondaryEdu),
                            INDEX idx_higheredu (HigherEdu),
                            INDEX idx_gradedu (GradEdu),
                            INDEX idx_otheredu (OtherEdu),
                            INDEX idx_bicycle_hh (BicycleHH),
                            INDEX idx_car_jeep_van_hh (CarJeepVanHH),
                            INDEX idx_radio_trans_hh (RadioTransHH),
                            INDEX idx_scooter_motor_moped_hh (ScooterMotorMopedHH),
                            INDEX idx_dilap_house_hh (DilapHouseHH),
                            INDEX idx_sep_kitchen_hh (SepKitchenHH),
                            INDEX idx_bath_fac_hh (BathFacHH),
                            INDEX idx_latrine_fac_hh (LatrineFacHH),
                            INDEX idx_hhsize1person (HHSize1Person),
                            INDEX idx_hhsize2persons (HHSize2Persons),
                            INDEX idx_hhsize3persons (HHSize3Persons),
                            INDEX idx_hhsize3to5persons (HHSize3To5Persons),
                            INDEX idx_hhsize4persons (HHSize4Persons),
                            INDEX idx_hhsize5persons (HHSize5Persons),
                            INDEX idx_hhsize6_8persons (HHSize6_8Persons),
                            INDEX idx_hhsize9abovepersons (HHSize9AbovePersons),
                            INDEX idx_powerparityless45000 (PowerParityLess45000),
                            INDEX idx_powerparity45000_90000 (PowerParity45000_90000),
                            INDEX idx_powerparity90000_150000 (PowerParity90000_150000),
                            INDEX idx_powerparity150000_240000 (PowerParity150000_240000),
                            INDEX idx_powerparity240000_330000 (PowerParity240000_330000),
                            INDEX idx_powerparity330000_425000 (PowerParity330000_425000),
                            INDEX idx_powerparity425000_545000 (PowerParity425000_545000),
                            INDEX idx_powerparityabove545000 (PowerParityAbove545000),
                            INDEX idx_nearpremiseswater_hh (NearPremisesWaterHH),
                            INDEX idx_marriedcouple1hh (MarriedCouple1HH),
                            INDEX idx_marriedcouple2hh (MarriedCouple2HH),
                            INDEX idx_marriedcouple3hh (MarriedCouple3HH),
                            INDEX idx_marriedcouple3ormorehh (MarriedCouple3OrMoreHH),
                            FOREIGN KEY (DistrictID) REFERENCES District(DistrictID)
                        )
                        """
                    ]

                    # Execute schema queries
                    for query in schema_queries:
                        try:
                            cursor.execute(query)
                            print("Table created successfully.")
                        except mysql.connector.Error as err:
                            print(f"Error creating table: {err}")

                # Commit changes (outside of the cursor block)
                connection.commit()

    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")

# Call the function to create the schema
#create_snowflake_star_schema()


# %%


def fetch_states_from_mongodb():
    try:
        # Connect to MongoDB
        states_data = list(connect_mongo().distinct("StateName"))

        return states_data
    
    except Exception as e:
        print(f"An error occurred while fetching data from MongoDB: {e}")
        return None

def insert_states(mysql_cursor, states):
    try:
        state_id_map = {}
        for state in states:
            mysql_cursor.execute("INSERT IGNORE INTO State (StateName) VALUES (%s)", (state,))
            state_id = mysql_cursor.lastrowid
            state_id_map[state] = state_id
        print("States inserted successfully.")
        return state_id_map
    except mysql.connector.Error as err:
        print(f"Error inserting states: {err}")
        return None

def load_state_data():
    state_id_map = {}  # Dictionary to store state IDs
    try:
        # Connect to MySQL
        connection = connect_mysql()
        if connection:
            # Create a cursor object
            cursor = connection.cursor()

            # Fetch states data from MongoDB
            states_data = fetch_states_from_mongodb()

            if states_data:
                # Insert states data into MySQL and get state_id map
                state_id_map = insert_states(cursor, states_data)

                if state_id_map:
                    # Commit changes
                    connection.commit()
                else:
                    print("Failed to insert states into MySQL.")

            else:
                print("No data fetched from MongoDB.")

    except Exception as e:
        print(f"An error occurred: {e}")
        if connection:
            connection.rollback()

    finally:
        # Close cursor and MySQL connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    return state_id_map

# Call the function to load state data
#state_id_map = load_state_data()

# %%
def fetch_districts_from_mongodb():
    try:
        # Fetch data from MongoDB
        districts_data = list(connect_mongo().find({}, {'DistrictName': 1, 'Population': 1, 'Male': 1, 'Female': 1, 'StateName': 1,'MaleLiterate': 1, 'FemaleLiterate': 1}))

        return districts_data

    except Exception as e:
        print(f"An error occurred while fetching data from MongoDB: {e}")
        return None

def insert_districts(mysql_cursor, districts, state_id_map):
    try:
        for district in districts:
            state_name = district.get('StateName')
            state_id = state_id_map.get(state_name)
            district_name = district.get('DistrictName')
            population = district.get('Population')
            male = district.get('Male')
            female = district.get('Female')
            MaleLiterate = district.get('MaleLiterate')
            FemaleLiterate = district.get('FemaleLiterate')

            mysql_cursor.execute("""
                INSERT IGNORE INTO District (StateID, DistrictName, Population, Male, Female, MaleLiterate, FemaleLiterate) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (state_id, district_name, population, male, female, MaleLiterate, FemaleLiterate))

        print("Districts inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error inserting districts: {err}")

def load_district_data(state_id_map):
    try:
        # Connect to MySQL
        connection = connect_mysql()
        if connection:
            # Create a cursor object
            cursor = connection.cursor()

            # Fetch districts data from MongoDB
            districts_data = fetch_districts_from_mongodb()

            if districts_data:
                # Insert districts data into MySQL
                insert_districts(cursor, districts_data, state_id_map)

                # Commit changes
                connection.commit()
            else:
                print("No data fetched from MongoDB.")

    except Exception as e:
        print(f"An error occurred: {e}")
        if connection:
            connection.rollback()

    finally:
        # Close cursor and MySQL connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Load district data using the state ID map
#load_district_data(state_id_map)

# %%
def fetch_district_data_from_mongodb():
    try:
        # Fetch data from MongoDB
        district_data = list(connect_mongo().find({}, {
            '_id': 0, 'DistrictID': 1, 'SC': 1, 'MaleSC': 1, 'FemaleSC': 1, 'ST': 1, 'MaleST': 1, 'FemaleST': 1,
            'MainWorkers': 1, 'MarginalWorkers': 1, 'NonWorkers': 1, 'CultivatorWorkers': 1, 'AgrWorkers': 1,
            'HHWorkers': 1, 'OtherWorkers': 1, 'Hindus': 1, 'Muslims': 1, 'Christians': 1, 'Sikhs': 1, 'Buddhists': 1,
            'Jains': 1, 'Others_Religions': 1, 'RelNotStated': 1, 'LPGHH': 1, 'ElecLightHH': 1, 'InternetHH': 1,
            'ComputerHH': 1, 'RuralHH': 1, 'UrbanHH': 1, 'TotalHH': 1, 'BelowPrimaryEdu': 1, 'PrimaryEdu': 1,
            'MiddleEdu': 1, 'SecondaryEdu': 1, 'HigherEdu': 1, 'GradEdu': 1, 'OtherEdu': 1, 'LitEdu': 1, 'IllitEdu': 1,
            'TotalEdu': 1, 'AgeGroup0_29': 1, 'AgeGroup30_49': 1, 'AgeGroup50': 1, 'AgeNotStated': 1, 'BicycleHH': 1,
            'CarJeepVanHH': 1, 'RadioTransHH': 1, 'ScooterMotorMopedHH': 1, 'PhoneLandlineHH': 1, 'MobileOnlyHH': 1,
            'TVCompLaptopHH': 1, 'TVHH': 1, 'PhoneHH': 1, 'PhoneBothHH': 1, 'DilapHouseHH': 1, 'SepKitchenHH': 1,
            'BathFacHH': 1, 'LatrineFacHH': 1, 'OwnedHH': 1, 'RentedHH': 1, 'BathFacEnclosureHH': 1, 'OtherFuelHH': 1,
            'PitLatrineHH': 1, 'OtherLatrineHH': 1, 'NightSoilLatrineHH': 1, 'FlushLatrineHH': 1, 'NoBathFacHH': 1,
            'NoLatrineFacHH': 1, 'UncoveredWellWaterHH': 1, 'HandpumpWaterHH': 1, 'SpringWaterHH': 1, 'RiverCanalWaterHH': 1,
            'OtherWaterHH': 1, 'NearPremisesWaterHH': 1, 'WithinPremisesWaterHH': 1, 'PondLakeWaterHH': 1, 'TapWaterHH': 1,
            'BoreholeWaterHH': 1, 'HHSize1Person': 1, 'HHSize2Persons': 1, 'HHSize1To2Persons': 1, 'HHSize3Persons': 1,
            'HHSize3To5Persons': 1, 'HHSize4Persons': 1, 'HHSize5Persons': 1, 'HHSize6_8Persons': 1, 'HHSize9AbovePersons': 1,
            'AwayWaterSourceHH': 1, 'MarriedCouple1HH': 1, 'MarriedCouple2HH': 1, 'MarriedCouple3HH': 1, 'MarriedCouple3OrMoreHH': 1,
            'MarriedCouple4HH': 1, 'MarriedCouple5HH': 1, 'MarriedCoupleNoneHH': 1, 'PowerParityLess45000': 1, 'PowerParity45000_90000': 1,
            'PowerParity90000_150000': 1, 'PowerParity45000_150000': 1, 'PowerParity150000_240000': 1, 'PowerParity240000_330000': 1,
            'PowerParity150000_330000': 1, 'PowerParity330000_425000': 1, 'PowerParity425000_545000': 1, 'PowerParity330000_545000': 1,
            'PowerParityAbove545000': 1, 'TotalPowerParity': 1
        }))

        return district_data

    except Exception as e:
        print(f"An error occurred while fetching data from MongoDB: {e}")
        return None

def insert_demographics(mysql_cursor, demographics_data):
    try:
        for demographic in demographics_data:
            mysql_cursor.execute(
                """
                INSERT IGNORE INTO Demographics (
                    DistrictID, SC, MaleSC, FemaleSC, ST, MaleST, FemaleST, MainWorkers, MarginalWorkers, NonWorkers,
                    CultivatorWorkers, AgrWorkers, HHWorkers, OtherWorkers, Hindus, Muslims, Christians, Sikhs, Buddhists,
                    Jains, OtherReligions, RelNotStated, LPGHH, ElecLightHH, InternetHH, ComputerHH, RuralHH, UrbanHH, TotalHH,
                    BelowPrimaryEdu, PrimaryEdu, MiddleEdu, SecondaryEdu, HigherEdu, GradEdu, OtherEdu, LitEdu, IllitEdu, TotalEdu,
                    AgeGroup0_29, AgeGroup30_49, AgeGroup50, AgeNotStated, BicycleHH, CarJeepVanHH, RadioTransHH, ScooterMotorMopedHH,
                    PhoneLandlineHH, MobileOnlyHH, TVCompLaptopHH, TVHH, PhoneHH, PhoneBothHH, DilapHouseHH, SepKitchenHH, BathFacHH,
                    LatrineFacHH, OwnedHH, RentedHH, BathFacEnclosureHH, OtherFuelHH, PitLatrineHH, OtherLatrineHH, NightSoilLatrineHH,
                    FlushLatrineHH, NoBathFacHH, NoLatrineFacHH, UncoveredWellWaterHH, HandpumpWaterHH, SpringWaterHH, RiverCanalWaterHH,
                    OtherWaterHH, NearPremisesWaterHH, WithinPremisesWaterHH, PondLakeWaterHH, TapWaterHH, BoreholeWaterHH, HHSize1Person,
                    HHSize2Persons, HHSize1To2Persons, HHSize3Persons, HHSize3To5Persons, HHSize4Persons, HHSize5Persons, HHSize6_8Persons,
                    HHSize9AbovePersons, AwayWaterSourceHH, MarriedCouple1HH, MarriedCouple2HH, MarriedCouple3HH, MarriedCouple3OrMoreHH,
                    MarriedCouple4HH, MarriedCouple5HH, MarriedCoupleNoneHH, PowerParityLess45000, PowerParity45000_90000, PowerParity90000_150000,
                    PowerParity45000_150000, PowerParity150000_240000, PowerParity240000_330000, PowerParity150000_330000, PowerParity330000_425000,
                    PowerParity425000_545000, PowerParity330000_545000, PowerParityAbove545000, TotalPowerParity
                ) VALUES (
                    %(DistrictID)s, %(SC)s, %(MaleSC)s, %(FemaleSC)s, %(ST)s, %(MaleST)s, %(FemaleST)s, %(MainWorkers)s, %(MarginalWorkers)s,
                    %(NonWorkers)s, %(CultivatorWorkers)s, %(AgrWorkers)s, %(HHWorkers)s, %(OtherWorkers)s, %(Hindus)s, %(Muslims)s, %(Christians)s,
                    %(Sikhs)s, %(Buddhists)s, %(Jains)s, %(Others_Religions)s, %(RelNotStated)s, %(LPGHH)s, %(ElecLightHH)s, %(InternetHH)s, %(ComputerHH)s,
                    %(RuralHH)s, %(UrbanHH)s, %(TotalHH)s, %(BelowPrimaryEdu)s, %(PrimaryEdu)s, %(MiddleEdu)s, %(SecondaryEdu)s, %(HigherEdu)s, %(GradEdu)s,
                    %(OtherEdu)s, %(LitEdu)s, %(IllitEdu)s, %(TotalEdu)s, %(AgeGroup0_29)s, %(AgeGroup30_49)s, %(AgeGroup50)s, %(AgeNotStated)s, %(BicycleHH)s,
                    %(CarJeepVanHH)s, %(RadioTransHH)s, %(ScooterMotorMopedHH)s, %(PhoneLandlineHH)s, %(MobileOnlyHH)s, %(TVCompLaptopHH)s, %(TVHH)s, %(PhoneHH)s,
                    %(PhoneBothHH)s, %(DilapHouseHH)s, %(SepKitchenHH)s, %(BathFacHH)s, %(LatrineFacHH)s, %(OwnedHH)s, %(RentedHH)s, %(BathFacEnclosureHH)s,
                    %(OtherFuelHH)s, %(PitLatrineHH)s, %(OtherLatrineHH)s, %(NightSoilLatrineHH)s, %(FlushLatrineHH)s, %(NoBathFacHH)s, %(NoLatrineFacHH)s,
                    %(UncoveredWellWaterHH)s, %(HandpumpWaterHH)s, %(SpringWaterHH)s, %(RiverCanalWaterHH)s, %(OtherWaterHH)s, %(NearPremisesWaterHH)s,
                    %(WithinPremisesWaterHH)s, %(PondLakeWaterHH)s, %(TapWaterHH)s, %(BoreholeWaterHH)s, %(HHSize1Person)s, %(HHSize2Persons)s, %(HHSize1To2Persons)s,
                    %(HHSize3Persons)s, %(HHSize3To5Persons)s, %(HHSize4Persons)s, %(HHSize5Persons)s, %(HHSize6_8Persons)s, %(HHSize9AbovePersons)s, %(AwayWaterSourceHH)s,
                    %(MarriedCouple1HH)s, %(MarriedCouple2HH)s, %(MarriedCouple3HH)s, %(MarriedCouple3OrMoreHH)s, %(MarriedCouple4HH)s, %(MarriedCouple5HH)s,
                    %(MarriedCoupleNoneHH)s, %(PowerParityLess45000)s, %(PowerParity45000_90000)s, %(PowerParity90000_150000)s, %(PowerParity45000_150000)s,
                    %(PowerParity150000_240000)s, %(PowerParity240000_330000)s, %(PowerParity150000_330000)s, %(PowerParity330000_425000)s, %(PowerParity425000_545000)s,
                    %(PowerParity330000_545000)s, %(PowerParityAbove545000)s, %(TotalPowerParity)s
                )
                """, demographic
            )
        print("Demographics data inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error inserting demographics: {err}")
        return None

def load_demographics_data():
    try:
        # Connect to MySQL
        connection = connect_mysql()
        if connection:
            # Create a cursor object
            cursor = connection.cursor()

            # Fetch district data from MongoDB
            demographics_data = fetch_district_data_from_mongodb()

            if demographics_data:
                # Insert demographics data into MySQL
                insert_demographics(cursor, demographics_data)

                # Commit changes
                connection.commit()

            else:
                print("No data fetched from MongoDB.")

    except Exception as e:
        print(f"An error occurred: {e}")
        if connection:
            connection.rollback()

    finally:
        # Close cursor and MySQL connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Call the function to load demographics data
#load_demographics_data()


# %%
def drop_mongodb_collection():
    try:
        uri = "mongodb+srv://project:Project321@myatlasclusteredu.43hutqm.mongodb.net/?retryWrites=true&w=majority&appName=myAtlasClusterEDU"
        mongo_client = pymongo.MongoClient(uri)
        db = mongo_client['census']
        collection = db["census"]
        collection.drop()
        print(f"Collection dropped successfully.")
    except Exception as e:
        print(f"An error occurred while dropping the MongoDB collection: {e}")

#drop_mongodb_collection()

# %%
st.title("Census Data Analysis")

if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()
if 'df1' not in st.session_state:
    st.session_state.df1 = pd.DataFrame()
if 'df_filled' not in st.session_state:
    st.session_state.df_filled = pd.DataFrame()
if 'comparison' not in st.session_state:
    st.session_state.comparison = pd.DataFrame()

if st.button("Fetch Census Data"):
    st.session_state.df, st.session_state.df1 = get_raw_data()
    st.balloons()
    st.success("Data fetched successfully!")

if st.button("Transform Data"):
    st.session_state.df = rename_columns(st.session_state.df)
    st.session_state.df = process_state_names(st.session_state.df, st.session_state.df1)
    st.session_state.df_filled, st.session_state.comparison = fill_missing_values_and_percentage(st.session_state.df)
    st.success("Data transformed successfully!")

if st.button("Check the transormation result"):
    st.write(st.session_state.comparison)

if st.button("Load Census Data to MongoDB"):
    drop_mongodb_collection()
    load_data_to_mongodb(st.session_state.df_filled)
    st.success("Data loaded successfully!")

if st.button("Load Data to MySQL"):
    create_snowflake_star_schema()
    state_id_map = load_state_data()
    load_district_data(state_id_map)
    # Assuming load_demographics_data() is defined similarly to load_district_data
    load_demographics_data()
    st.success("Data loaded successfully!")
    drop_mongodb_collection()


# %%
# Function to execute a query and return the result as a DataFrame
def run_query(query):
    connection = connect_mysql()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return pd.DataFrame(result)

# Function to perform analysis based on selected question
def analysis(question):
    q1 = "1. What is the total population of each district?"
    q2 = "2. How many literate males and females are there in each district?"
    q3 = "3. What is the percentage of workers (both male and female) in each district?"
    q4 = "4. How many households have access to LPG or PNG as a cooking fuel in each district?"
    q5 = "5. What is the religious composition (Hindus, Muslims, Christians, etc.) of each district?"
    q6 = "6. How many households have internet access in each district?"
    q7 = "7. What is the educational attainment distribution (below primary, primary, middle, secondary, etc.) in each district?"
    q8 = "8. How many households have access to various modes of transportation (bicycle, car, radio, television, etc.) in each district?"
    q9 = "9. What is the condition of occupied census houses (dilapidated, with separate kitchen, with bathing facility, with latrine facility, etc.) in each district?"
    q10 = "10. How is the household size distributed (1 person, 2 persons, 3-5 persons, etc.) in each district?"
    q11 = "11. What is the total number of households in each state?"
    q12 = "12. How many households have a latrine facility within the premises in each state?"
    q13 = "13. What is the average household size in each state?"
    q14 = "14. How many households are owned versus rented in each state?"
    q15 = "15. What is the distribution of different types of latrine facilities (pit latrine, flush latrine, etc.) in each state?"
    q16 = "16. How many households have access to drinking water sources near the premises in each state?"
    q17 = "17. What is the average household income distribution in each state based on the power parity categories?"
    q18 = "18. What is the percentage of married couples with different household sizes in each state?"
    q19 = "19. How many households fall below the poverty line in each state based on the power parity categories?"
    q20 = "20. What is the overall literacy rate (percentage of literate population) in each state?"

    queries = {
        q1: "select DistrictName, sum(Population) total_population from district group by DistrictName",
        q2: "select districtname,sum(maleliterate) maleliterate_count, sum(femaleliterate) femaleliterate_count from district group by districtname",
        q3: "SELECT dis.districtname, (d.MainWorkers + d.MarginalWorkers) / d.TotalHH * 100 AS WorkerPercentage FROM Demographics d join district dis on dis.districtid = d.districtid",
        q4: "SELECT dis.districtname, d.LPGHH AS HouseholdsWithLPGPNG FROM Demographics d join district dis on dis.districtid = d.districtid",
        q5: "SELECT dis.districtname, d.Hindus, d.Muslims, d.Christians, d.Sikhs, d.Buddhists, d.Jains, d.OtherReligions FROM Demographics d join district dis on dis.districtid = d.districtid",
        q6: "SELECT dis.districtname, d.InternetHH AS HouseholdsWithInternet FROM Demographics d join district dis on dis.districtid = d.districtid",
        q7: "SELECT dis.districtname, d.BelowPrimaryEdu, d.PrimaryEdu, d.MiddleEdu, d.SecondaryEdu, d.HigherEdu, d.GradEdu, d.OtherEdu FROM Demographics d join district dis on dis.districtid = d.districtid",
        q8: "SELECT dis.districtname, d.BicycleHH, d.CarJeepVanHH, d.RadioTransHH, d.ScooterMotorMopedHH FROM Demographics d join district dis on dis.districtid = d.districtid",
        q9: "SELECT dis.districtname, d.DilapHouseHH, d.SepKitchenHH, d.BathFacHH, d.LatrineFacHH FROM Demographics d join district dis on dis.districtid = d.districtid",
        q10: "SELECT dis.districtname, d.HHSize1Person, d.HHSize2Persons, d.HHSize3Persons, d.HHSize3To5Persons, d.HHSize4Persons, d.HHSize5Persons, d.HHSize6_8Persons, d.HHSize9AbovePersons FROM Demographics d join district dis on dis.districtid = d.districtid",
        q11: "SELECT s.StateName, SUM(d.TotalHH) AS TotalHouseholds FROM Demographics d join district dis on dis.DistrictId=d.DistrictId join state s on s.stateid = dis.StateId GROUP BY s.StateName",
        q12: "SELECT s.StateName, SUM(d.LatrineFacHH) AS HouseholdsWithLatrine FROM Demographics d join district dis on dis.DistrictId=d.DistrictId join state s on s.stateid = dis.StateId GROUP BY s.statename",
        q13: "SELECT s.StateName, AVG(d.TotalHH / (d.HHSize1Person + d.HHSize2Persons + d.HHSize3Persons + d.HHSize3To5Persons + d.HHSize4Persons + d.HHSize5Persons + d.HHSize6_8Persons + d.HHSize9AbovePersons)) AS AvgHouseholdSize FROM Demographics d join district dis on dis.DistrictId=d.DistrictId join state s on s.stateid = dis.StateId GROUP BY s.StateID",
        q14: "SELECT s.StateName, SUM(d.OwnedHH) AS OwnedHouseholds, SUM(d.RentedHH) AS RentedHouseholds FROM Demographics d join district dis on dis.DistrictId=d.DistrictId join state s on s.stateid = dis.StateId GROUP BY s.StateName",
        q15: "SELECT s.StateName, SUM(d.PitLatrineHH) AS PitLatrine, SUM(d.FlushLatrineHH) AS FlushLatrine, SUM(d.OtherLatrineHH) AS OtherLatrine, SUM(d.NightSoilLatrineHH) AS NightSoilLatrine FROM Demographics d join district dis on dis.DistrictId=d.DistrictId join state s on s.stateid = dis.StateId GROUP BY s.StateName",
        q16: "SELECT s.StateName, SUM(d.NearPremisesWaterHH) AS WaterNearPremises FROM Demographics d join district dis on dis.DistrictId=d.DistrictId join state s on s.stateid = dis.StateId GROUP BY s.StateName",
        q17: "SELECT s.statename, AVG(d.PowerParityLess45000) AS PowerParityLess45000, AVG(d.PowerParity45000_90000) AS PowerParity45000_90000, AVG(d.PowerParity90000_150000) AS PowerParity90000_150000, AVG(d.PowerParity45000_150000) AS PowerParity45000_150000, AVG(d.PowerParity150000_240000) AS PowerParity150000_240000, AVG(d.PowerParity240000_330000) AS PowerParity240000_330000, AVG(d.PowerParity150000_330000) AS PowerParity150000_330000, AVG(d.PowerParity330000_425000) AS PowerParity330000_425000, AVG(d.PowerParity425000_545000) AS PowerParity425000_545000, AVG(d.PowerParity330000_545000) AS PowerParity330000_545000, AVG(d.PowerParityAbove545000) AS PowerParityAbove545000 FROM Demographics d join district dis on dis.DistrictId=d.DistrictId join state s on s.stateid = dis.StateId GROUP BY s.StateName",
        q18: "SELECT s.statename, AVG(d.MarriedCouple1HH / d.TotalHH * 100) AS MarriedCouple1HHPercent, AVG(d.MarriedCouple2HH / d.TotalHH * 100) AS MarriedCouple2HHPercent, AVG(d.MarriedCouple3HH / d.TotalHH * 100) AS MarriedCouple3HHPercent, AVG(d.MarriedCouple3OrMoreHH / d.TotalHH * 100) AS MarriedCouple3OrMoreHHPercent FROM Demographics d join district dis on dis.DistrictId=d.DistrictId join state s on s.stateid = dis.StateId GROUP BY s.StateName",
        q19: "SELECT s.statename, SUM(d.PowerParityLess45000) AS BelowPovertyLine FROM Demographics d join district dis on dis.DistrictId=d.DistrictId join state s on s.stateid = dis.StateId GROUP BY s.StateName",
        q20: "SELECT s.StateName, (SUM(dis.MaleLiterate) + SUM(dis.FemaleLiterate)) / SUM(d.TotalHH) * 100 AS LiteracyRate FROM Demographics d join district dis on dis.DistrictId=d.DistrictId join state s on s.stateid = dis.StateId GROUP BY s.StateName"
    }

    query = queries.get(question, "")
    if query:
        try:
            df = run_query(query)
            st.write(df)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error('Invalid question selected.')

# SQL Analysis questions
questions = [
    "1. What is the total population of each district?",
    "2. How many literate males and females are there in each district?",
    "3. What is the percentage of workers (both male and female) in each district?",
    "4. How many households have access to LPG or PNG as a cooking fuel in each district?",
    "5. What is the religious composition (Hindus, Muslims, Christians, etc.) of each district?",
    "6. How many households have internet access in each district?",
    "7. What is the educational attainment distribution (below primary, primary, middle, secondary, etc.) in each district?",
    "8. How many households have access to various modes of transportation (bicycle, car, radio, television, etc.) in each district?",
    "9. What is the condition of occupied census houses (dilapidated, with separate kitchen, with bathing facility, with latrine facility, etc.) in each district?",
    "10. How is the household size distributed (1 person, 2 persons, 3-5 persons, etc.) in each district?",
    "11. What is the total number of households in each state?",
    "12. How many households have a latrine facility within the premises in each state?",
    "13. What is the average household size in each state?",
    "14. How many households are owned versus rented in each state?",
    "15. What is the distribution of different types of latrine facilities (pit latrine, flush latrine, etc.) in each state?",
    "16. How many households have access to drinking water sources near the premises in each state?",
    "17. What is the average household income distribution in each state based on the power parity categories?",
    "18. What is the percentage of married couples with different household sizes in each state?",
    "19. How many households fall below the poverty line in each state based on the power parity categories?",
    "20. What is the overall literacy rate (percentage of literate population) in each state?"
]

question = st.selectbox("Select Question", questions)
analysis(question)



