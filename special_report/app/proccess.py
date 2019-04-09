from special_report.db.SpecialReport import DB_SetArrival, DB_GetReport, DB_ResetArrivals


def proccess_frame(handler, **kwargs):
    identified_persons = handler.handle_data(**kwargs)

    print("Identified persons", identified_persons)

    for key, val in identified_persons.items():
        DB_SetArrival(key, val)

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
    DB_ResetArrivals()

