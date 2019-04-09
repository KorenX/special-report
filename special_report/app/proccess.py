import ..db.SpecialReport as dbReport
import ..ml.image_handler as image_handler


def proccess_frame(handler, frame):
    identified_persons = handler.handle_data(frame)
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

