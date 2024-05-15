import json
import datetime
from Person import Doctor,Patient
from collections import defaultdict
import calendar


class Admin:
    """A class that deals with the Admin operations"""

    def __init__(self, username, password, address=''):
        """
        Args:
            username (string): Username
            password (string): Password
            address (string, optional): Address Defaults to ''
        """
        self.__username = username
        self.__password = password
        self.__address = address
        
    @classmethod
    def load_from_file(cls, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                return cls(data['username'], data['password'], data['address'])
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Error loading admin details: {e}")
    
    
    def save_admin_details(self, filename):
        """Save admin details to a file."""
        data = {
            'username': self.__username,
            'password': self.__password,
            'address': self.__address
        }
        with open(filename, 'w') as file:
            json.dump(data, file, indent=2)

    def update_admin_details(self):
        """Allows the user to update and change username, password, and address"""
        try:
            print('Choose the field to be updated:')
            print(' 1 Username')
            print(' 2 Password')
            print(' 3 Address')
            op = int(input('Input: '))

            if op == 1:
                # .14: Implement the logic to update the username
                new_username = input('Enter the new username: ')
                self.__username = new_username
                print('Username updated.')

            elif op == 2:
                # .15: Implement the logic to update the password
                new_password = input('Enter the new password: ')
                # validate the password
                if new_password == input('Enter the new password again: '):
                    self.__password = new_password
                    print('Password updated.')
                else:
                    print('Passwords do not match. Password not updated.')

            elif op == 3:
                # .16: Implement the logic to update the address
                new_address = input('Enter the new address: ')
                self.__address = new_address
                print('Address updated.')

            else:
                print('Invalid operation chosen.')

        except ValueError:
            print('Invalid input. Please enter a valid option (1, 2, or 3).')

    def load_admin_details(self, filename):
        """Load admin details from a file."""
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.__username = data.get('username', '')
                self.__password = data.get('password', '')
                self.__address = data.get('address', '')
        except FileNotFoundError:
            print(f"File '{filename}' not found. Starting with default admin details.")

    
    def view(self, a_list):
        """Print a list of printables"""
        for index, item in enumerate(a_list):
            print(f'{index+1:3}|{item}')

    def login(self):
        """A method that deals with the login"""
        print("-----Login-----")
        while True:
           try:
               username = input('Enter the username: ')
               password = input('Enter the password: ')
               if username == self.__username and password == self.__password:
                   return username
               else:
                   raise ValueError("Invalid username or password")
           except ValueError as e:
               print(f"Error: {e}")
               
    def find_index(self, index, doctors):
        """Check that the doctor id exists"""
        if index in range(0, len(doctors)):
            return True
        else:
            return False
        
    def save_patients(self, filename, patients, discharged_patients):
        """Save all patients' data to a file."""
        data = {
            'active_patients': [],
            'discharged_patients': []
        }

        for patient in patients:
            data['active_patients'].append({
                'first_name': patient.first_name,
                'surname': patient.surname,
                'age': patient.age,
                'mobile': patient.mobile,
                'postcode': patient.postcode,
                'symptoms': patient.symptoms,
                'doctor': patient.get_doctor().full_name() if patient.get_doctor() else None
            })

        for discharged_patient in discharged_patients:
            data['discharged_patients'].append({
                'first_name': discharged_patient.first_name,
                'surname': discharged_patient.surname,
                'age': discharged_patient.age,
                'mobile': discharged_patient.mobile,
                'postcode': discharged_patient.postcode,
                'symptoms': discharged_patient.symptoms,
                'doctor': discharged_patient.get_doctor().full_name() if discharged_patient.get_doctor() else None
            })

        with open(filename, 'w') as file:
            json.dump(data, file, indent=2)

    def load_patients(self, filename,doctors):
        """Load all patients' data from a file."""
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                active_patients = []
                discharged_patients = []

                # Load active patients
                for patient_data in data.get('active_patients', []):
                    patient = Patient(
                        patient_data['first_name'],
                        patient_data['surname'],
                        patient_data['age'],
                        patient_data['mobile'],
                        patient_data['postcode']
                    )
                    patient.symptoms = patient_data['symptoms']

                    doctor_name = patient_data['doctor']
                    if doctor_name:
                        doctor = next((d for d in doctors if d.full_name() == doctor_name), None)
                        if doctor:
                            patient.link(doctor)

                    active_patients.append(patient)

                # Load discharged patients (if present)
                for discharged_patient_data in data.get('discharged_patients', []):
                    discharged_patient = Patient(
                        discharged_patient_data['first_name'],
                        discharged_patient_data['surname'],
                        discharged_patient_data['age'],
                        discharged_patient_data['mobile'],
                        discharged_patient_data['postcode']
                    )
                    discharged_patient.symptoms = discharged_patient_data['symptoms']

                    doctor_name = discharged_patient_data['doctor']
                    if doctor_name:
                        doctor = next((d for d in doctors if d.full_name() == doctor_name), None)
                        if doctor:
                            discharged_patient.link(doctor)

                    discharged_patients.append(discharged_patient)

                return active_patients, discharged_patients
        except FileNotFoundError:
            print(f"File '{filename}' not found. Starting with empty lists of patients.")
            return [], []
    
    def patient_management(self, patients):
        """A method that deals with registering, viewing, updating, deleting patients."""
        print("-----Patient Management-----")

        # menu
        print('Choose the operation:')
        print(' 1 - Register')
        print(' 2 - View')
        print(' 3 - Update')
        

        op = input('Input: ')

        # register
        if op == '1':
            print("-----Register-----")
            self.register_patient(patients)

        # view
        elif op == '2':
            print("-----List of Patients-----")
            self.view(patients)

        # update
        elif op == '3':
            print("-----Update Patient Details-----")
            self.update_patient(patients)

        else:
            print('Invalid operation chosen. Please choose option 1,2 or 3')
    
    def validate_age(self, age):
        """Validate age as a positive integer."""
        try:
            age = int(age)
            if age <= 0:
                raise ValueError("Age must be a positive integer.")
            return age
        except ValueError:
            raise ValueError("Invalid age. Please enter a positive integer.")
                
    def register_patient(self, patients):
        """Register a new patient."""
        first_name = input("Enter the patient's first name: ")
        surname = input("Enter the patient's surname: ")
        age = input("Enter the patient's age: ")
        mobile = input("Enter the patient's mobile number: ")
        postcode = input("Enter the patient's postcode: ")

        try:
            age = self.validate_age(age)
            new_patient = Patient(first_name, surname, age, mobile, postcode)
            patients.append(new_patient)
            print('Patient registered successfully.')
            self.save_patients('patients_data.json', patients, [])

        except ValueError as e:
            print(f"Error registering patient: {e}")

    def update_patient(self, patients):
        """Update patient details."""
        print('ID |          Full Name           | Age |    Mobile     | Postcode ')
        self.view(patients)

        try:
            patient_index = int(input('Enter the ID of the patient to be updated: ')) - 1
            if patient_index in range(len(patients)):
                patient = patients[patient_index]

                print("Choose the field to be updated:")
                print("1 - Age")
                print("2 - Mobile")
                print("3 - Postcode")

                choice = input("Enter your choice: ")

                if choice == '1':
                    new_age = input('Enter the new age: ')
                    try:
                        new_age = self.validate_age(new_age)
                        patient.age = new_age
                        print('Patient details updated.')
                    except ValueError as e:
                        print(f"Error updating patient details: {e}")

                elif choice == '2':
                    new_mobile = input('Enter the new mobile number: ')
                    if len(new_mobile) == 11 and new_mobile.isdigit():
                        patient.mobile = new_mobile
                        print('Patient details updated.')
                    else:
                        print('Invalid mobile number format. Mobile number must be 11 digits long and contain only digits.')

                elif choice == '3':
                    new_postcode = input('Enter the new postcode: ')
                    patient.postcode = new_postcode
                    print('Patient details updated.')

                else:
                    print('Invalid choice. No details updated.')

                # Save the updated list of patients to the JSON file
                self.save_patients('patients_data.json', patients, [])

            else:
                print('The ID entered was not found.')

        except ValueError:
            print('Invalid input. Please enter a valid ID.')

    
    def save_doctors(self, filename, doctors):
        """Save all doctors' data to a file."""
        data = [{'first_name': doctor.first_name, 'surname': doctor.surname, 'speciality': doctor.speciality} for doctor in doctors]
        with open(filename, 'w') as file:
            json.dump(data, file, indent=2)

    def load_doctors(self, filename):
        """Load all doctors' data from a file."""
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                return [Doctor(doctor['first_name'], doctor['surname'], doctor['speciality']) for doctor in data]
        except FileNotFoundError:
            print(f"File '{filename}' not found. Starting with an empty list of doctors.")
            return []    
                
    def get_doctor_details(self):
        """Get the details needed to add a doctor"""
        # .2 get the first name, surname, and speciality of the doctor
        while True:
            try:
                first_name = input("Enter the doctor's first name: ")
                surname = input("Enter the doctor's surname: ")
                speciality = input("Enter the doctor's speciality: ")

            # Validate inputs
                if all([first_name, surname, speciality]):
                    return first_name, surname, speciality
                else:
                    raise ValueError("All fields must be filled.")
            except ValueError as e:
                 print(f"Error: {e}")

    def doctor_management(self, doctors):
        """A method that deals with registering, viewing, updating, deleting doctors"""
        print("-----Doctor Management-----")

        # menu
        print('Choose the operation:')
        print(' 1 - Register')
        print(' 2 - View')
        print(' 3 - Update')
        print(' 4 - Delete')

        
        op = input('Input: ')

        # register
        if op == '1':
            print("-----Register-----")

            # get the doctor details
            print('Enter the doctor\'s details:')
            
            first_name, surname, speciality = self.get_doctor_details()

            
            name_exists = any(
                doctor.get_first_name() == first_name and doctor.get_surname() == surname
                for doctor in doctors
            )

            
            if name_exists:
                print('Name already exists. Doctor not registered.')
            else:
                
                doctors.append(Doctor(first_name, surname, speciality))
                print('Doctor registered.')

        # View
        elif op == '2':
            print("-----List of Doctors-----")
           
            self.view(doctors)

        # Update
        elif op == '3':
            while True:
                print("-----Update Doctor`s Details-----")
                print('ID |          Full name           |  Speciality')
                self.view(doctors)
                try:
                    index = int(input('Enter the ID of the doctor: ')) - 1
                    doctor_index = self.find_index(index, doctors)
                    if doctor_index:
                        break
                    else:
                        print("Doctor not found")

                except ValueError:
                    print('The ID entered is incorrect')

            # menu
            print('Choose the field to be updated:')
            print(' 1 First name')
            print(' 2 Surname')
            print(' 3 Speciality')
            op = input('Input: ')  # make the user input lowercase

            
            if op == '1':
                new_first_name = input('Enter the new first name: ')
                doctors[index].set_first_name(new_first_name)
                print('Doctor details updated.')
            elif op == '2':
                new_surname = input('Enter the new surname: ')
                doctors[index].set_surname(new_surname)
                print('Doctor details updated.')
            elif op == '3':
                new_speciality = input('Enter the new speciality: ')
                doctors[index].set_speciality(new_speciality)
                print('Doctor details updated.')
            else:
                print('Invalid operation chosen.')

        # Delete
        elif op == '4':
            print("-----Delete Doctor-----")
            print('ID |          Full Name           |  Speciality')
            self.view(doctors)

            try:
                doctor_index = int(input('Enter the ID of the doctor to be deleted: ')) - 1
                if self.find_index(doctor_index, doctors):
                    
                    del doctors[doctor_index]
                    print('Doctor deleted.')
                else:
                    print('The ID entered is incorrect')
            except ValueError:
                print('Invalid input. Please enter a valid ID.')

        else:
            print('Invalid operation chosen. Check your spelling!')

    def view_patient(self, patients):
        """Print a list of patients"""
        print("-----View Patients-----")
        print('ID |          Full Name           |      Doctor`s Full Name      | Age |    Mobile     | Postcode ')
        
        self.view(patients)

    def assign_doctor_to_patient(self, patients, doctors):
        """Allow the admin to assign a doctor to a patient"""
        print("-----Assign-----")
        print("-----Patients-----")
        self.view_patient(patients)

        try:
            patient_index = int(input('Please enter the patient ID: ')) - 1
            if patient_index in range(len(patients)):
                patient = patients[patient_index]
                patients[patient_index].print_symptoms()
                # Option to add symptoms
                new_symptom = input('Add a new symptom (press enter to skip): ')
                if new_symptom:
                    patients[patient_index].add_symptom(new_symptom)

                print("-----Doctors Select-----")
                print('--------------------------------------------------')
                print('ID |          Full Name           |  Speciality   ')
                self.view(doctors)

                try:
                    doctor_index = int(input('Please enter the doctor ID: ')) - 1
                    if self.find_index(doctor_index, doctors):
                        patients[patient_index].link(doctors[doctor_index])
                        print('The patient is now assigned to the doctor.')

                        # Book an appointment for the patient
                        self.book_appointment(patient)
                    else:
                        print('The ID entered was not found.')
                except ValueError:
                    print('The ID entered is incorrect')
            else:
                print('The ID entered was not found.')
        except ValueError:
            print('The ID entered is incorrect')
            
    def discharge(self, patients, discharge_patients):
        """Allow the admin to discharge a patient when treatment is done"""
        print("-----Discharge Patient-----")

        while True:
            print("Do you want to discharge a patient? (Y/N)")
            user_choice = input().upper()

            if user_choice == 'N':
               break  # Exit the loop if the user enters 'N'
            elif user_choice == 'Y':
               
                self.view_patient(patients)

                try:
                  patient_index = int(input('Enter the ID of the patient to be discharged: ')) - 1
                  if patient_index in range(len(patients)):
                    # Remove the patient from the list of active patients
                    discharged_patient = patients.pop(patient_index)

                    # Add the discharged patient to the list of discharged patients
                    discharge_patients.append(discharged_patient)
                    print('The patient has been discharged.')
                  else:
                     print('The ID entered was not found.')
                except ValueError:
                     print('Invalid input. Please enter a valid ID.')
            else:
              print('Invalid input. Please enter Y or N.')


    def view_discharge(self, discharged_patients):
        """Prints the list of all discharged patients"""
        print("-----Discharged Patients-----")
        
        self.view_patient(discharged_patients)

    def update_details(self):
        """Allows the user to update and change username, password, and address"""
        try:
            print('Choose the field to be updated:')
            print(' 1 Username')
            print(' 2 Password')
            print(' 3 Address')
            op = int(input('Input: '))

            if op == 1:
           
               new_username = input('Enter the new username: ')
               self.__username = new_username
               print('Username updated.')

            elif op == 2:
           
                new_password = input('Enter the new password: ')
            # validate the password
                if new_password == input('Enter the new password again: '):
                    self.__password = new_password
                    print('Password updated.')
                else:
                    print('Passwords do not match. Password not updated.')

            elif op == 3:
           
                new_address = input('Enter the new address: ')
                self.__address = new_address
                print('Address updated.')

            else:
               print('Invalid operation chosen.')

        except ValueError:
               print('Invalid input. Please enter a valid option (1, 2, or 3).')
               
    def group_patients_by_family(self, patients):
        """Group patients by their family (surname)"""
        grouped_patients = {}
        for patient in patients:
            if patient.family in grouped_patients:
                grouped_patients[patient.family].append(patient)
            else:
                grouped_patients[patient.family] = [patient]
        return grouped_patients
    
    def view_patients_grouped_by_family(self, patients):
        """Print a list of patients grouped by family"""
        print("-----View Patients Grouped by Family-----")
        grouped_patients = self.group_patients_by_family(patients)
        for family, family_patients in grouped_patients.items():
            print(f'Family: {family}')
            print('ID |          Full Name           |      Doctor`s Full Name      | Age |    Mobile     | Postcode ')
            self.view(family_patients)
            print('--------------------------------------------------')        
    
    def book_appointment(self, patient):
        """Allow the admin to book an appointment for a patient"""
        print("-----Book Appointment-----")
        appointment_date = input('Enter the appointment date (YYYY-MM-DD): ')

        #validation for the appointment date
        if not appointment_date or not self.validate_date_format(appointment_date):
            print('Invalid date format. Appointment not booked.')
            return

        # Create the appointment data
        appointment_data = {
            'patient': {
                'first_name': patient.first_name,
                'surname': patient.surname,
            },
            'doctor': patient.get_doctor().full_name(),
            'date': appointment_date,
        }

        # Save the appointment data to the JSON file
        appointments_filename = 'appointments.json'
        appointments = self.load_appointments(appointments_filename)
        appointments.append(appointment_data)
        self.save_appointments(appointments_filename, appointments)

        print('Appointment booked successfully.')
    
    def view_appointments(self):
        """View all appointments"""
        print("-----View All Appointments-----")
        appointments_filename = 'appointments.json'
        appointments = self.load_appointments(appointments_filename)

        if not appointments:
            print("No appointments found.")
            return

        print('Patient Name                 | Doctor Name                  | Appointment Date')
        print('---------------------------------------------------------------')
        for appointment in appointments:
            patient_name = f"{appointment['patient']['first_name']} {appointment['patient']['surname']}"
            doctor_name = appointment['doctor']
            appointment_date = appointment['date']
            print(f'{patient_name:^30}|{doctor_name:^30}|{appointment_date:^20}')

    
    def validate_date_format(self, date_str):
        """Validate the date format (YYYY-MM-DD)"""
        try:
            datetime.datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def save_appointments(self, filename, appointments):
        """Save all appointments' data to a file."""
        with open(filename, 'w') as file:
            json.dump(appointments, file, indent=2)

    def load_appointments(self, filename):
        """Load all appointments' data from a file."""
        try:
            with open(filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        
    def generate_management_report(self, patients, discharged_patients, doctors):
        """Generate a management report."""
        print("----- Management Report -----")

        # Total number of doctors
        total_doctors = len(doctors)
        print(f'Total number of doctors: {total_doctors}')

        # Total number of patients per doctor
        total_patients_per_doctor = defaultdict(int)
        for patient in patients:
            doctor = patient.get_doctor()
            if doctor:
                total_patients_per_doctor[doctor.full_name()] += 1

        print("Total number of patients per doctor:")
        for doctor_name, patient_count in total_patients_per_doctor.items():
            print(f'{doctor_name}: {patient_count}')

        # Total number of appointments per month per doctor
        total_appointments_per_month = defaultdict(lambda: defaultdict(int))
        for appointment in self.load_appointments('appointments.json'):
            doctor_name = appointment['doctor']
            appointment_month = appointment['date'][5:7]
            total_appointments_per_month[doctor_name][appointment_month] += 1

        print("Total number of appointments per month per doctor:")
        for doctor_name, month_counts in total_appointments_per_month.items():
            print(f'{doctor_name}:')
            for month, count in month_counts.items():
                month_name = calendar.month_name[int(month)]
                print(f'  {month_name}: {count}')

        # Total number of patients based on the illness type
        total_patients_based_on_illness = defaultdict(int)
        for patient in patients:
            for symptom in patient.symptoms:
                total_patients_based_on_illness[symptom] += 1

        print("Total number of patients based on the illness type:")
        for illness, patient_count in total_patients_based_on_illness.items():
            print(f'{illness}: {patient_count}')
            
    def relocate_patients(self, patients, doctors):
        """
        Relocate patients from one doctor to another using patient IDs.
        """
        print("----- Relocate Patients -----")

        # Display a list of current doctors
        print("Current Doctors:")
        for idx, doctor in enumerate(doctors, start=1):
            print(f"{idx}. {doctor.full_name()} ({doctor.speciality})")

        # Get the current doctor's ID
        current_doctor_id = int(input("Enter the ID of the current doctor: ")) - 1

        if current_doctor_id < 0 or current_doctor_id >= len(doctors):
            print("Invalid doctor ID.")
            return

        current_doctor = doctors[current_doctor_id]

        # Display a list of patients under the current doctor
        current_doctor_patients = [patient for patient in patients if patient.get_doctor() == current_doctor]
        print(f"\nPatients under {current_doctor.full_name()}:")
        for idx, patient in enumerate(current_doctor_patients, start=1):
            print(f"{idx}. {patient.full_name()} (ID: {idx})")

        if not current_doctor_patients:
            print("No patients found under this doctor.")
            return

        # Get the patient's ID to be relocated
        patient_id = int(input("\nEnter the ID of the patient to be relocated: ")) - 1

        if patient_id < 0 or patient_id >= len(current_doctor_patients):
            print("Invalid patient ID.")
            return

        patient_to_relocate = current_doctor_patients[patient_id]

        # Display a list of available doctors for relocation
        print("\nAvailable Doctors for Relocation:")
        for idx, doctor in enumerate(doctors, start=1):
            if doctor != current_doctor:
                print(f"{idx}. {doctor.full_name()} ({doctor.speciality})")

        # Get the new doctor's ID
        new_doctor_id = int(input("Enter the ID of the new doctor: ")) - 1

        if new_doctor_id < 0 or new_doctor_id >= len(doctors):
            print("Invalid new doctor ID.")
            return

        new_doctor = doctors[new_doctor_id]

        # Relocate the patient
        patient_to_relocate.link(new_doctor)
        print(f"\n{patient_to_relocate.full_name()} (ID: {patient_id + 1}) has been relocated to {new_doctor.full_name()}.")

        # Update the doctor's patient lists
        current_doctor.patients = [patient for patient in current_doctor.patients if patient != patient_to_relocate]
        new_doctor.patients.append(patient_to_relocate)        
        