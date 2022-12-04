#! /usr/bin/python3
import pickle
import csv

def noramlizeCalData(cal_data, verbose:bool=False):
        # find upper left, (0,0)
        # find lower right (1,1)
        x_min = cal_data[0][1]
        y_min = cal_data[0][2]
        x_max = cal_data[0][1]
        y_max = cal_data[0][2]
        for p in cal_data:
                if verbose:
                        print(p)
                if p[1] < x_min:
                        x_min = p[1]
                if p[2] < y_min:
                        y_min = p[2]
                if p[1] > x_max:
                        x_max = p[1]
                if p[2] > y_max:
                        y_max = p[2]
        if verbose:
                print("x_min: ", x_min)
                print("x_max: ", x_max)
                print("y_min: ", y_min)
                print("y_max: ", y_max)
        normalized = []
        for p in cal_data:
                n = (p[0], (p[1]-x_min)/(x_max-x_min), (p[2]-y_min)/(y_max-y_min))
                normalized.append(n)
                if verbose:
                        print(n)
        return normalized
        
if __name__=="__main__":
        cal_data = None
        with open('cam/cal_data.pickle', 'rb') as pickle_file:
                cal_data = pickle.load(pickle_file)
        
        with open('cam/cal_data.csv', 'w') as csv_file:
                c = noramlizeCalData(cal_data, verbose=True)
                csv_writer = csv.writer(csv_file, delimiter=";")
                for p in c:
                        csv_writer.writerow(p)
        
