# Imports

from Admin import Admin


def main():
    """
    the main function to be ran when the program runs
    """

    # Initialising the actors
        
    filename_admin_details = 'admin_details.json'

    try:
        # Load admin details from a file
        admin = Admin.load_from_file(filename_admin_details)
    except ValueError as e:
        print(e)
        return  # Exit the program if admin details cannot be loaded

    

    doctors = admin.load_doctors('doctors_data.json')

    filename = 'patients_data.json'

    try:
        # Load patients' data from a file
        patients, discharged_patients = admin.load_patients(filename, doctors)

    except Exception as e:
        print(f"Error loading patients: {e}")
        patients = []
        discharged_patients = []

    # keep trying to login till the login details are correct
    while True:
        if admin.login():
            running = True  # allow the program to run
            break
        else:
            print('Incorrect username or password.')

    while running:
        # print the menu
        print('Choose the operation:')
        print(' 1- Register/view/update/delete doctor') 
        print(' 2- Discharge patients')
        print(' 3- View discharged patient')
        print(' 4- Assign doctor to a patient')
        print(' 5- Update admin details')
        print(' 6- View patients grouped by family')
        print(' 7- View all appointments')
        print(' 8- Register/view/update patient')  
        print(' 9- Generate Management Report')
        print(' 10- Relocate Patients')
        print(' 11- Quit')

        # get the option
        op = input('Option: ')

        if op == '1':
            # 1- Register/view/update/delete doctor
         #.1
           admin.doctor_management(doctors)

        elif op == '2':
            # 2- View or discharge patients
            #.2
           print("----- Patient Management -----")
           admin.view_patient(patients)
           admin.discharge(patients, discharged_patients)

        elif op == '3':
            # 3 - view discharged patients
            #.4
             admin.view_discharge(discharged_patients)

        elif op == '4':
            # 4- Assign doctor to a patient
            admin.assign_doctor_to_patient(patients, doctors)
            
        elif op == '5':
            # 5- Update admin detais
            admin.update_admin_details()
            admin.save_admin_details(filename_admin_details)
            
        elif op == '6':
        # View Patients Grouped by Family
            admin.view_patients_grouped_by_family(patients)  
            
        elif op == '7':
            # 8 - View All Appointments
            admin.view_appointments() 
        
        elif op == '8':
            # 8 - Register/view/update patient
            admin.patient_management(patients)
                
        elif op == '9':
            # 9 - generate reports
            admin.generate_management_report(patients, discharged_patients, doctors) 
            
        elif op == '10':
            # 10 - Relocate Patients
            admin.relocate_patients(patients, doctors)     

        elif op == '11':
            # 11 - Quit
            #.5
            admin.save_patients(filename, patients, discharged_patients)
            admin.save_doctors('doctors_data.json', doctors)
            print("Exiting the program.")
            break

        else:
            # the user did not enter an option that exists in the menu
            print('Invalid option. Try again')

if __name__ == '__main__':
    main()

