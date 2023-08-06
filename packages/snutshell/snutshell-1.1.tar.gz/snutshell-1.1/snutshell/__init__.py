import pickle
import xlsxwriter
import numpy as np

def np_2darray_converter(matrix):

    new_matrix = np.array(matrix, ndmin = 2)
    if (new_matrix.dtype == 'O'):
        return -1, -1, -1
    rows = new_matrix.shape[0]
    cols = new_matrix.shape[1]
    return rows, cols, new_matrix



def create_xlsx(filename, keys, data = None):
    workbook = xlsxwriter.Workbook( filename + '.xlsx')
    worksheet = workbook.add_worksheet()
    title_format = workbook.add_format({ 'font_size':16, 'font_color':'#02172C',
                                            'bold':True, 'bg_color':'#7FF000'})  #A9E063
    separator_format = workbook.add_format({'bg_color':'#434446'})  #A72307

    if(data == None):
        try:
            d_keys = list(keys.keys())
            d_data = list(keys.values())
        except:
            print('A dictionary is expected as 2nd positional argument')
            return
    else:
        d_keys = keys
        d_data = data

    current_column = 3
    current_row = 3
    for i in range(len(d_data)):
        worksheet.write(current_row, current_column, d_keys[i], title_format)

        rows, cols, current_data = np_2darray_converter(d_data[i])
        if(rows == -1):
            continue

        if(rows == 1):
            worksheet.write_column(current_row + 2, current_column, current_data[0])
            current_column += 4
            worksheet.set_column(current_column-2, current_column-2, width = 3, cell_format = separator_format)
        else:
            worksheet.conditional_format(current_row, current_column + 1, current_row, current_column + cols - 1, {'type':'blanks',
                                                                                                'format':title_format})
            for j in range(rows):
                worksheet.write_row(current_row + 2 + j, current_column, current_data[j])
            current_column += cols + 3
            worksheet.set_column(current_column-2, current_column-2,width = 3, cell_format = separator_format)

    workbook.close()

class Simsum:
    '''the summary class summarizes simulation results (input files, parameters, useful results)
    '''

    def __init__(self, s = None):
        if(s == None):
            self.description = "Simulation Description was not provided"
        else:
            self.description = s
        self.data = {}
    def add(self, keys, values = None):
        if (values == None):    # dictionary input
            try:
                for i in keys.keys():
                    if(i[0] == '_' and i[1] == '_'):
                        pass
                    #elif(np.array(keys[i], ndmin = 2).dtype == 'O' and type(keys[i]) != type({})):
                    #    pass
                    else:
                        self.data[i] = keys[i]
            except:
                print('A dictionary with "string" type as keys is expected as 2nd positional argument')

        else:
            try:
                for i, key in enumerate(keys):
                    self.data[key] = values[i]
            except:
                print('A list is expected as 2nd and 3rd positional argument')



    def save(self, filename, xlsx = False):
        final_dict = {'description' : self.description,
                      'data' : self.data }
        pickle.dump(final_dict, open(filename + '.dat', 'wb'))

        if(xlsx == True):
            create_xlsx(filename, self.data)


    @classmethod
    def load(cls, filename, dict = False):
        loaded_dict = pickle.load(open(filename + '.dat', 'rb'))
        if (dict == False):
            new_obj = Simsum(loaded_dict['description'])
            new_obj.add(loaded_dict['data'])
            return new_obj
        else:
            return loaded_dict

    def print_description(self):
        print(self.description)
    def print_keys(self):
        print('Data Keys: ', list(self.data.keys()))

    def get_data(self, key = None):
        if(key == None):
            return self.data
        else:
            return self.data[key]
