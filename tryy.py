def display_all_data():
    # rossz
    applicants = Applicant.select(Applicant.applicant_id, Applicant.name, Applicant.application_date, Applicant.city,
                                  Applicant.status, Applicant.school, School.name.alias("school_name"))\
        .join(School, join_type=JOIN.LEFT_OUTER)\
        .naive()

    for person in applicants:
        print("\nAPPLICANT ID: {}\nNAME: {}\nAPPLIED ON: {}-{}-{}\nCITY: {}\nSTATUS: {}\nSCHOOL: {}\n"
              .format(person.applicant_id,
                      person.name,
                      person.application_date.year,
                      person.application_date.month,
                      person.application_date.day,
                      person.city,
                      person.status,
                      person.school_name))

    # jo...
    applicants = Applicant.select()
    for person in applicants:
        school_name = "None"
        if person.school is not None:
            school_name = person.school.name
        print("\nAPPLICANT ID: {}\nNAME: {}\nAPPLIED ON: {}-{}-{}\nCITY: {}\nSTATUS: {}\nSCHOOL: {}\n"
              .format(person.applicant_id,
                      person.name,
                      person.application_date.year,
                      person.application_date.month,
                      person.application_date.day,
                      person.city,
                      person.status,
                      school_name))
