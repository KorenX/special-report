import ..db.SpecialReport as dbReport

def recognize_in_frame():
    return 0

def proccess_frame(frame):
    identified_persons = recognize_in_frame(frame)
    for identified_person in identified_persons:
        DB_SetArrival(identified_person[0], identified_person[1])

### To Goldberg's scheduler:
def invokeGetReport(phoneNumber):
    report = DB_GetReport(phoneNumber)
    if report:
        arrivedDudes = []
        unarrivedDudes = []
        for person in report:
            if person[1]:
                arrivedDudes.append(person[0])
            else:
                unarrivedDudes.append(person[0])

    # arrivedDudesString = 'Arrived:' + ', '.join(arrivedDudes)
    # unarrivedDudesString = 'Missing:' + ', '.join(unarrivedDudes)
    
    return [arrivedDudes, unarrivedDudes]

def invokeResetArrivals():
    return DB_ResetArrivals()

