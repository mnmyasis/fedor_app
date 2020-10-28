from django.conf import settings
from django.db import models
import numpy as np
import pandas as pd
from directory.models import *
import time


# Этот класс будет возвращать результат стыковки
#
class Test:
    def get_match_result(self, clients_dict=ClientDirectory.objects.all()):
        pivas = Matching()
        return pivas.start(clients_dict)  # {'res' : pivas.result}


# Здесь будут алгоритмы стыковки
class Matching():
    def textConvert(text):
        return null

    def start(self, clients_dict):
        # Обозначения
        # Target - то что не понятно и нужно состыковать (переменная asna)
        # Info - это записи из справочника из которых будет выбираться подходящий вариант для Target
        start_time = time.time()
        # Инициализация Target
        # Сейчас я беру первые десять строк. Дальше нужно будет сделать поиск - что конкретно я хочу состыковать
        # cols = [x.name for x in clients_dict[0]._meta.get_fields()]
        try:
            len(clients_dict)
            cols = [x.name for x in clients_dict[0]._meta.get_fields()]
        except TypeError:
            cols = [x.name for x in clients_dict._meta.get_fields()]

        print(clients_dict)

        ss = {}
        ss['nnt'] = []
        ss['name'] = []
        ss['id'] = []
        ss['number_competitor'] = []

        for line in clients_dict:
            ss['nnt'].append(line.nnt)
            ss['name'].append(line.name)
            ss['id'].append(line.pk)
            ss['number_competitor'].append(line.number_competitor)
        # asna = (pd.DataFrame(clients_dict.values(),columns=cols))#.head(n=10)
        # asna = (pd.DataFrame(ss, columns=cols).head(n=10)
        asna = pd.DataFrame(ss, columns=cols)
        asna.rename(columns={'id': 'id_c'}, inplace=True)
        print('HUJASNA', asna)

        print('Загружены данные конкурента ', round(time.time() - start_time), 'sec')

        asna.loc[:, 'name'] = asna.loc[:, 'name'].str.replace('-', ' ')
        asna.loc[:, 'name'] = asna.loc[:, 'name'].str.replace(',', '.')
        asna.loc[:, 'name'] = asna.loc[:, 'name'].str.replace('. ', ' ', regex=False)
        asna.loc[:, 'name'] = asna.loc[:, 'name'].str.replace('/', ' ', regex=False)
        asna.loc[:, 'name'] = asna.loc[:, 'name'].str.replace('(', '')
        asna.loc[:, 'name'] = asna.loc[:, 'name'].str.replace(')', '')
        asna.loc[:, 'name'] = asna.loc[:, 'name'].str.replace('\n', '')

        print('Проведены замены ', round(time.time() - start_time), 'sec')
        print(asna)
        # Зонтичный бренд
        asna = asna.assign(brand='-')

        # Список чисел. Из названия выдергиваются все числа
        nmb = np.array([])

        for i, r in asna.iterrows():
            tmp = ''
            last_chr = ''

            to4ka = 0
            for char in r['name']:
                if char.isdigit() or (char == '.' and last_chr.isdigit()):
                    to4ka += 1 if char == '.' else 0
                    if to4ka < 2:
                        tmp = tmp + char
                elif last_chr.isdigit():
                    # print(last_chr)
                    to4ka = 0
                    tmp = tmp + ','
                last_chr = char
            nmb = np.append(nmb, tmp)

        asna = asna.assign(numbs=nmb)
        print('nmb', nmb)

        print('Из текста получены наборы чисел ', round(time.time() - start_time), 'sec')

        # Инициализация Info (сначала весь справочник)
        cols = [x.name for x in
                BaseDirectory.objects.all()[0]._meta.get_fields()]  # Замена моделей iqvia на BaseDirectory
        iqvia = pd.DataFrame(BaseDirectory.objects.all().values(), columns=cols)
        # iqvia = iqvia[iqvia['source']=='IQVIA']
        iqvia = iqvia.assign(in_pool=0)
        print(iqvia)

        iqvia.loc[:, 'umbrella_brand'] = iqvia.loc[:, 'umbrella_brand'].str.replace('(', '')
        iqvia.loc[:, 'umbrella_brand'] = iqvia.loc[:, 'umbrella_brand'].str.replace(')', '')
        iqvia.loc[:, 'dosage'] = iqvia.loc[:, 'dosage'].str.replace(',', '.')
        iqvia.loc[:, 'volwe'] = iqvia.loc[:, 'volwe'].str.replace(',', '.')

        # Список брендов из Info (уникальных)
        zont = pd.pivot_table(iqvia, index='umbrella_brand').index

        print('Загружен базовый справочник. Построен список уникальных брендов ', round(time.time() - start_time),
              'sec')

        # Для каждого Target перебор ВСЕХ брендов из списка, чтобы выяснить какой подходит
        res_dict = pd.DataFrame()  # Здесь будут все связки начиная со стыковки по бренду
        for k in zont:

            if k != '':
                # Здесь задача взять только первые два слова
                i = ''
                tmp = k.split(' ')
                if len(tmp) < 2:
                    i = tmp[0]
                else:
                    i = tmp[0] + ' ' + tmp[1]

                asna.loc[
                    asna['name'].str.contains(i + ' '), 'brand'] = k  # Здесь косяк - берется только последний бренд
                actual = asna[asna['brand'] == k]

                if not actual.empty:
                    tmp = pd.merge(iqvia[iqvia['umbrella_brand'] == k], actual, how='outer', left_on='umbrella_brand',
                                   right_on='brand')
                    res_dict = res_dict.append(tmp, ignore_index=True)

        # print(asna.loc[asna['brand']=='-'])

        print('Найдены бренды ', round(time.time() - start_time), 'sec')

        print('Итог', res_dict)
        print('Пустые', asna.loc[asna['brand'] == '-'])

        print('Добавлены записи без бренда', round(time.time() - start_time), 'sec')

        # Поиск чисел
        res_dict['dosage'] = res_dict['dosage'].str.extract(r'(\d+\.?\d*)', expand=False)  # r'\d*\.?\d*'
        res_dict['volwe'] = res_dict['volwe'].str.extract(r'(\d+\.?\d*)', expand=False)
        res_dict['numero'] = res_dict['numero'].str.extract(r'(\d+\.?\d*)', expand=False)
        res_dict = res_dict.fillna('')
        res_dict = res_dict.assign(num_prc=0)
        res_dict = res_dict.assign(num_fv=0)
        res_dict = res_dict.assign(num_leven=0)
        res_dict = res_dict.assign(rank=1)
        res_dict = res_dict.assign(final_res='')

        print('Обработаны числовые значения справочника ', round(time.time() - start_time), 'sec')

        # Перебор состыкованных
        full_count = len(res_dict.index)
        counter = 0
        old_status = 0
        new_status = 0
        for i in res_dict.index:
            counter += 1

            new_status = counter / full_count
            if new_status - old_status > 0.1:
                old_status = new_status
                print('Алгоритм пройден на: ', old_status * 100, ' %')

            tmp = []
            if res_dict.loc[i, 'dosage'] != '':
                tmp.append(float(res_dict.loc[i, 'dosage']))
            if res_dict.loc[i, 'volwe'] != '':
                tmp.append(float(res_dict.loc[i, 'volwe']))
            if res_dict.loc[i, 'numero'] != '':
                tmp.append(float(res_dict.loc[i, 'numero']))

            tqnt = 0  # Найдено совпадений
            fqnt = 0  # Кол-во элементов
            for j in res_dict.loc[i, 'numbs'].split(','):
                # print('_',j,'_')

                if len(j) > 0 and j.replace('.', '', 1).isdigit():
                    ppp = 0

                    for k in tmp:
                        if float(j) == float(k) or float(j) == float(k) * 1000 or float(j) == (float(k) / 1000):
                            # print('j ',j,' k ',k,' ',j==k)
                            ppp = 1
                    tqnt += ppp
                    fqnt += 1
            res_dict.loc[i, 'num_prc'] = (tqnt / fqnt) / 2 if fqnt != 0 else 0  # ЕСЛИ ЧТО ЗДЕСЬ МОЖЕТ БЫТЬ ПРОБЛЕМА
            # print('ЦФРЫ ',tqnt)

            # Поиск формы выпуска
            form_tmp = res_dict.loc[i, 'fv_short']
            form_tmp = form_tmp.replace('+', ' ')
            form_tmp = form_tmp.split(' ')[0]
            res_dict.loc[i, 'num_fv'] = 0.33 if res_dict.loc[i, 'name'].find(form_tmp) != -1 else 0

            # Левенштейн на минималках
            client_arr = res_dict.loc[i, 'name'].split(' ')
            info_arr = (res_dict.loc[i, 'tn_fv'] + ' ' + res_dict.loc[i, 'full_corp'] + ' ' + res_dict.loc[
                i, 'corp_rus']).split(' ')

            # Фильтры исключающие слова из менее чем 2 букв
            target = 0
            while target < len(client_arr):
                if len(client_arr[target]) < 2:
                    del client_arr[target]
                else:
                    target += 1

            target = 0
            while target < len(info_arr):
                if len(info_arr[target]) < 3:
                    del info_arr[target]
                else:
                    target += 1

            # Попарное сопоставление двух товаров
            text_tmp = 0
            t_tmp = 0
            for cc in client_arr:
                for ii in info_arr:
                    t_tmp += 1 if ii.find(cc) != -1 and t_tmp == 0 else 0
                    if ii.find(cc) == -1:
                        t_tmp += 0.7 if (ii[:5].find(cc[:5]) != -1 and t_tmp == 0) else 0
                    if ii.find(cc) != -1:
                        print(ii)
                text_tmp += t_tmp
            # print(text_tmp)
            # Подсчет балл-оценки похожести названий
            res_dict.loc[i, 'num_leven'] = text_tmp / len(client_arr)  # ((len(info_arr)+len(client_arr))/2)
            # print('res1 ', res_dict.loc[i,'num_leven'])
            res_dict.loc[i, 'num_leven'] = res_dict.loc[i, 'num_leven'] + res_dict.loc[i, 'num_prc'] + res_dict.loc[
                i, 'num_fv']
        # print('res2 ', res_dict.loc[i,'num_leven'])
        # print('client', client_arr)
        # print('info', info_arr)
        print('Завершен основной алгоритм сопоставления ', round(time.time() - start_time), 'sec')

        print(res_dict.columns)

        # Подсчет кол-ва
        records_calc = pd.pivot_table(res_dict, values='id', index='nnt', aggfunc=np.count_nonzero)
        res_dict = res_dict.assign(qnt=0)

        for i in records_calc.index:
            res_dict.loc[res_dict['nnt'] == i, 'qnt'] = records_calc.loc[i, 'id']

        # Оставить топ записей
        res_dict = res_dict.sort_values(by=['name', 'num_leven'], ascending=False)

        last_name = ''
        target_name = ''
        pointer = 0
        for i in res_dict.index:
            target_name = res_dict.loc[i, 'name']

            if last_name != target_name:
                pointer = 1
            else:
                pointer += 1

            if pointer > 7:
                res_dict.loc[i, 'rank'] = 0

            last_name = target_name

        res_dict = res_dict.loc[res_dict['rank'] == 1]

        # Прибить производителя
        res_dict = res_dict.assign(tn_fv_prod=res_dict.tn_fv + ' ' + res_dict.full_corp + ' ' + res_dict.corp_rus)
        res_dict = res_dict[
            ['id_c', 'number_competitor', 'nnt', 'id', 'name', 'tn_fv_prod', 'brand', 'num_prc', 'num_fv', 'num_leven',
             'qnt']]
        print('RES_DIC', ' IDI ', ' NAH', res_dict)

        # Добавить элементы без зонтичного бренда
        new_ind = max(res_dict.index) + 1
        for i, r in (asna.loc[asna['brand'] == '-']).iterrows():
            # print(r)
            res_dict.loc[new_ind] = {
                'id_c': r['id_c'],
                'number_competitor': r['number_competitor'],
                'nnt': r['nnt'],
                'id': -1,
                'name': r['name'],
                'tn_fv_prod': '-',
                'brand': '-',
                'num_prc': 0,
                'num_leven': 0,
                'num_fv': 0,
                'qnt': 0
            }
            new_ind += 1

        sss = pd.pivot_table(res_dict, index='nnt')
        print(sss)

        print('Подготовка данных для экспорта ', round(time.time() - start_time), 'sec')

        res_dict[['name', 'tn_fv_prod', 'brand', 'num_prc', 'num_fv', 'num_leven', 'qnt']].to_excel(
            '{}/logs/algoritm/out{}.xlsx'.format(settings.BASE_DIR, str(time.time())))
        print('Записан файл ', round(time.time() - start_time), 'sec')
        # Результат. Данные + заголовки отдельно
        result = {'data': res_dict.to_dict('records'), 'heads': res_dict.columns}
        return result