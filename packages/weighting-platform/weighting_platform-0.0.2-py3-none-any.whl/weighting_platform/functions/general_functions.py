""" Содержит общие, многоразовые функции"""


def form_point_name(course: str, point_type_str: str):
    """ Формирует название точки доступа, который передается в QSB, что бы тот его
    открыл. Как правило, оно состоит из направления (course) который передает
    QSB (оно может быть external или internal). Название точки формируется
    сложиение направления и слова point_type_str, т.е должно получиться что-то типа:
    EXTERNAL_GATE или INTERNAL_PHOTOCELL"""
    gate_name_full = '_'.join((course.upper(), point_type_str.upper()))
    return gate_name_full


def get_change_percent(first_weight, second_weight):
    """ Вернуть процент изменения second_weight относительно first_weight """
    difference = second_weight - first_weight
    percent = difference/first_weight * 100
    return abs(percent)


def if_dlinnomer_moved(first_weight, second_weight, min_percent=30):
    """ Возвращает True, если понимает, что машина переместилась по весам
    (весы изменились более чем на min_percent процентов) """
    percent = get_change_percent(first_weight, second_weight)
    if percent >= min_percent:
        return True


def send_round_status(stage, info=None, timer=None, weight=None, qpi=None):
    """ Отправляет статус заезда (stage) и дополнительную информацию для
     отображения статуса заезда.
    STAGE - BEFORE_WEIGHING; WEIGHING; AFTER_WEIGHING
    INFO - """
    info = {'STAGE': stage.upper(),
            'INFO': info.upper(),
            'TIMER': timer.upper(),
            'WEIGHT': weight}
    send_status(info, qpi)


def send_status(*msg, qpi=None):
    """ Используется в других функциях для вывода статуса в стандартный поток,
    либо для отправки статуса выполнения клиентам """
    print("MSG", msg)
    if qpi:
        qpi.broadcast_sending(msg)

