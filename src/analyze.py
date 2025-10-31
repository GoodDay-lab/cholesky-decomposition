import argparse
import json
import os
import subprocess

import matplotlib.pyplot as plt


parser = argparse.ArgumentParser(
    prog="analyze.py",
    description="Программа для построения графиков и анализа работы программы"
)
parser.add_argument('program', help="Путь к программе")
parser.add_argument('matrix', help="Путь к файлу с матрицей")
#parser.add_argument('-t', '--tests', type=int, help="Количество тестов")
args = parser.parse_args()


def norm(y_true, y_pred):
    ret = 0
    for i in range(len(y_true)):
        ret = max(ret, abs(y_true[i] - y_pred[i]))
    return ret


PLOT_DIR = "plots"
FLOAT_TYPE_SET = [16, 32, 64]
TESTS_SET = [3, 5, 10, 15, 20, 25, 30, 35, 40]

for f_type in FLOAT_TYPE_SET:
    # Собираем новую программу
    os.system("make rebuild FLOAT_T_FLAG=\"-DCUSTOM_FLOAT_T%d\"" % f_type)

    total_error1 = []
    total_error2 = []
    total_time = []

    for t_cnt in TESTS_SET:
        print(f"Тест: f{f_type} для n = {t_cnt} тестов")
        N = t_cnt
        enum = list(range(1, N+1))
        errors1 = []
        errors2 = []
        time = []
        time_type = "миллисекунды"

        for i in enum:
            process = subprocess.run([args.program, args.matrix],
                                     capture_output=True, text=True)
            results = json.loads(process.stdout)

            errors1.append(norm(results['b_orig']['data'], results['b_pred']['data']))
            errors2.append(norm(results['x_orig']['data'], results['x_pred']['data']))
            time.append(results['duration']['value'] / 1000000)

        plt.figure()
        plt.title("График ошибки невязки по \\inf-норме")
        plt.bar(enum, errors1)
        plt.ylabel("Величина ошибки")
        plt.xlabel(f"Номер теста (max_error={max(errors1):.05f}, mean_error={sum(errors1)/N:.05f})")
        plt.savefig(os.path.join(PLOT_DIR, "plot-t1-f%d-n%d.png" % (f_type, t_cnt)))
        plt.close()

        plt.figure()
        plt.title("График погрешности по \\inf-норме")
        plt.bar(enum, errors2)
        plt.ylabel("Величина ошибки")
        plt.xlabel(f"Номер теста (max_error={max(errors2):.05f}, mean_error={sum(errors2)/N:.05f})")
        plt.savefig(os.path.join(PLOT_DIR, "plot-t2-f%d-n%d.png" % (f_type, t_cnt)))
        plt.close()

        plt.figure()
        plt.title("График времени работы программы")
        plt.bar(enum, time)
        plt.ylabel("Время (мс)")
        plt.xlabel(f"Номер теста (max_error={max(time):.05f}, mean_error={sum(time)/N:.05f})")
        plt.savefig(os.path.join(PLOT_DIR, "plot-t3-f%d-n%d.png" % (f_type, t_cnt)))
        plt.close()

        total_error1.append(sum(errors1)/N)
        total_error2.append(sum(errors2)/N)
        total_time.append(sum(time)/N)

    plt.figure()
    plt.title("График средней ошибки невязки по \\inf-норме")
    plt.plot(TESTS_SET, total_error1)
    plt.ylabel("Величина ошибки")
    plt.xlabel("Количество тестов")
    plt.savefig(os.path.join(PLOT_DIR, "plot-total-t1-f%d.png" % (f_type)))
    plt.close()

    plt.figure()
    plt.title("График средней погрешности по \\inf-норме")
    plt.plot(TESTS_SET, total_error2)
    plt.ylabel("Величина ошибки")
    plt.xlabel("Количество тестов")
    plt.savefig(os.path.join(PLOT_DIR, "plot-total-t2-f%d.png" % (f_type)))
    plt.close()

    plt.figure()
    plt.title("График среднего времени работы")
    plt.plot(TESTS_SET, total_time)
    plt.ylabel("Время (мс)")
    plt.xlabel("Количество тестов")
    plt.savefig(os.path.join(PLOT_DIR, "plot-total-t3-f%d.png" % (f_type)))
    plt.close()
