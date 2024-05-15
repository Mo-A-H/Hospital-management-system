class Person:
    """Common parent class for Patient and Doctor"""

    def __init__(self, first_name, surname):
        """
        Args:
            first_name (string): First name
            surname (string): Surname
        """
        self.first_name = first_name
        self.surname = surname
        self.family = None



class Patient(Person):
    """Patient class, inheriting from Person"""

    def __init__(self, first_name, surname, age, mobile, postcode):
        """
        Args:
            first_name (string): First name
            surname (string): Surname
            age (int): Age
            mobile (string): the mobile number
            postcode (string): postcode
        """
        super().__init__(first_name, surname)
        self.age = age
        self.mobile = mobile
        self.postcode = postcode
        self.symptoms = []
        self.__doctor = None
        self.family = surname
        

    
    
    def full_name(self) :
        """full name is first_name and surname"""
        #.2
        return f"{self.first_name} {self.surname}"


    def get_doctor(self) :
        #.3
        return self.__doctor

    def link(self, doctor):
        """Args: doctor(string): the doctor full name"""
        self.__doctor = doctor

    def add_symptom(self, symptom):
        """Add a symptom to the patient"""
        self.symptoms.append(symptom)

    def print_symptoms(self):
        """Prints all the symptoms"""
        if self.symptoms:
            print(f"Symptoms: {', '.join(self.symptoms)}")
        else:
            print("No symptoms recorded.")


    def __str__(self):
        doctor_name = self.__doctor.full_name() if self.__doctor else "Not Assigned"
        return f'{self.full_name():^30}|{doctor_name:^30}|{self.age:^5}|{self.mobile:^15}|{self.postcode:^10}'

class Doctor(Person):
    """Doctor class, inheriting from Person"""

    def __init__(self, first_name, surname, speciality):
        """
        Args:
            first_name (string): First name
            surname (string): Surname
            speciality (string): Doctor's speciality
        """
        super().__init__(first_name, surname)
        self.speciality = speciality
        self.patients = [] 
        self.__appointments = []

    
    def full_name(self) :
        #.1
        return f"{self.first_name} {self.surname}"


    def get_first_name(self) :
        #.2
        return self.first_name

    def set_first_name(self, new_first_name):
        #.3
        self.first_name = new_first_name

    def get_surname(self) :
        #.4
        return self.surname

    def set_surname(self, new_surname):
        #.5
        self.surname = new_surname

    def get_speciality(self) :
        #.6
        return self.speciality

    def set_speciality(self, new_speciality):
        #.7
        self.speciality = new_speciality

    def add_patient(self, patient):
        self.patients.append(patient)


    def __str__(self):
        return f'{self.full_name():^30}|{self.speciality:^15}'

    def to_dict(self):
        """Convert doctor object to dictionary"""
        return {'first_name': self.first_name, 'surname': self.surname, 'speciality': self.speciality}

