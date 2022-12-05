#! /usr/bin/python3
import pickle
import csv

if __name__=="__main__":
        cal_data = None
        with open('cam/cal_data.pickle', 'rb') as pickle_file:
                cal_data = pickle.load(pickle_file)
        