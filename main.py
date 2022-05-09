# -*- coding: utf-8 -*-
import os
from extract_mcep import wav_to_mcep
from align_mcep import align_mcep
from train_gmm import train_gmm
from convert_voice import convert_voice


class VoiceConverter:
    def __init__(self, conv_from, conv_to):
        self.__from = conv_from
        self.__to = conv_to

    def __search_common_wav_files(self):
        wav_files_from = os.listdir('wav/train/{}/'.format(self.__from))
        wav_files_to = os.listdir('wav/train/{}/'.format(self.__to))
        wav_files = list(set(wav_files_from) & set(wav_files_to))
        # 拡張子無しのファイル名リストの状態で保持しておく
        self.__train_files = [file.replace('.wav', '') for file in wav_files]

    def __extract_mcep(self):
        if not os.path.exists('mcep/{}/'.format(self.__from)):
            os.makedirs('mcep/{}/'.format(self.__from))
        if not os.path.exists('mcep/{}/'.format(self.__to)):
            os.makedirs('mcep/{}/'.format(self.__to))

        for file in self.__train_files:
            wave_path = 'wav/train/{}/{}.wav'.format(self.__from, file)
            mcep_path = 'mcep/{}/{}.mcep'.format(self.__from, file)
            wav_to_mcep(wave_path, mcep_path)
            wave_path = 'wav/train/{}/{}.wav'.format(self.__to, file)
            mcep_path = 'mcep/{}/{}.mcep'.format(self.__to, file)
            wav_to_mcep(wave_path, mcep_path)

    def __align_mcep(self):
        outdir = 'mcep_aligned/{}_to_{}/'.format(self.__from, self.__to)
        if not os.path.exists(outdir + '{}/'.format(self.__from)):
            os.makedirs(outdir + '{}/'.format(self.__from))
        if not os.path.exists(outdir + '{}/'.format(self.__to)):
            os.makedirs(outdir + '{}/'.format(self.__to))

        for file in self.__train_files:
            mcep_from = 'mcep/{}/{}.mcep'.format(self.__from, file)
            mcep_to = 'mcep/{}/{}.mcep'.format(self.__to, file)
            align_mcep_from = outdir + '{}/{}.mcep'.format(self.__from, file)
            align_mcep_to = outdir + '{}/{}.mcep'.format(self.__to, file)
            align_mcep(mcep_from, mcep_to, align_mcep_from, align_mcep_to)

    def __train_gmm(self):
        outdir = 'train_result/{}_to_{}/'.format(self.__from, self.__to)
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        
        aligned_mcep = 'mcep_aligned/{}_to_{}/'.format(self.__from, self.__to)
        aligned_mcep_from = aligned_mcep + '{}/'.format(self.__from)
        aligned_mcep_to = aligned_mcep + '{}/'.format(self.__to)
        files = os.listdir(aligned_mcep_from)
        aligned_mcep_paths_from = [aligned_mcep_from + file for file in files]
        aligned_mcep_paths_to = [aligned_mcep_to + file for file in files]        
        train_gmm(aligned_mcep_paths_from, aligned_mcep_paths_to, outdir)

    def __convert_voice(self):
        wav_dir_from = 'wav/production/{}/'.format(self.__from)
        wav_dir_to = 'wav/production/{}/'.format(self.__to)
        if not os.path.exists(wav_dir_from):
            os.makedirs(wav_dir_from)
        if not os.path.exists(wav_dir_to):
            os.makedirs(wav_dir_to)

        gmm = 'train_result/{}_to_{}/GMM.gmm'.format(self.__from, self.__to)
        for file in os.listdir(wav_dir_from):
            wav_path_from = wav_dir_from + file
            wav_path_to = wav_dir_to + file
            convert_voice(wav_path_from, wav_path_to, gmm)        

    def run(self):
        self.__search_common_wav_files()
        self.__extract_mcep()
        self.__align_mcep()
        self.__train_gmm()
        self.__convert_voice()


if __name__ == '__main__':
    voice_converter = VoiceConverter('clb', 'slt')
    voice_converter.run()
