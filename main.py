# -*- coding: utf-8 -*-
from extract_mcep import extract_mcep
from align_mcep import align_mcep
#from train_gmm import train_gmm
#from convert_voice import convert_voice


if __name__ == '__main__':
    conv_from = ''
    conv_to = ''
    extract_mcep(conv_from, conv_to)
    align_mcep(conv_from, conv_to)
    #train_gmm(conv_from, conv_to)
    #convert_voice(conv_from, conv_to)
