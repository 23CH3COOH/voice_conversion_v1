# -*- coding: utf-8 -*-
import os
from extract_mcep import wav_to_mcep, output_mcep_text
from align_mcep import align_mcep, draw_aligned_mceps, DrawingAlignedMcepsItems
from train_gmm import train_gmm
from convert_voice import convert_voice
from common import m


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
        for target in [self.__from, self.__to]:
            if not os.path.exists('mcep/{}/text/'.format(target)):
                os.makedirs('mcep/{}/text/'.format(target))

            for file in self.__train_files:
                wave_path = 'wav/train/{}/{}.wav'.format(target, file)
                mcep_path = 'mcep/{}/{}.mcep'.format(target, file)
                text_path = 'mcep/{}/text/{}.mcep_ascii'.format(target, file)
                wav_to_mcep(wave_path, mcep_path)
                output_mcep_text(mcep_path, text_path)

    def __align_mcep(self):
        outdir = 'mcep_aligned/{}_to_{}/'.format(self.__from, self.__to)
        if not os.path.exists(outdir + '{}/'.format(self.__from)):
            os.makedirs(outdir + '{}/'.format(self.__from))
        if not os.path.exists(outdir + '{}/'.format(self.__to)):
            os.makedirs(outdir + '{}/'.format(self.__to))
        for i in range(m + 1):
            if not os.path.exists(outdir + 'graph/{:02}-th/'.format(i)):
                os.makedirs(outdir + 'graph/{:02}-th/'.format(i))
        text_dir = 'mcep/{}/text/{}.mcep_ascii'

        for file in self.__train_files:
            mcep_from = 'mcep/{}/{}.mcep'.format(self.__from, file)
            mcep_to = 'mcep/{}/{}.mcep'.format(self.__to, file)
            align_mcep_from = outdir + '{}/{}.mcep'.format(self.__from, file)
            align_mcep_to = outdir + '{}/{}.mcep'.format(self.__to, file)
            align_mcep(mcep_from, mcep_to, align_mcep_from, align_mcep_to)
            for i in range(m + 1):
                items_1 = DrawingAlignedMcepsItems()
                items_1.name = self.__from
                items_1.mcep_path_prev = text_dir.format(self.__from, file)
                items_1.mcep_path_result = align_mcep_from
                items_2 = DrawingAlignedMcepsItems()
                items_2.name = self.__to
                items_2.mcep_path_prev = text_dir.format(self.__to, file)
                items_2.mcep_path_result = align_mcep_to
                out_path = outdir + 'graph/{:02}-th/{}.png'.format(i, file)
                draw_aligned_mceps(items_1, items_2, i, out_path)

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
        print('Extracting mel cepstrum...')
        self.__extract_mcep()
        print('Aligning mel cepstrum...')
        self.__align_mcep()
        print('Training...')
        self.__train_gmm()
        print('Converting voice...')
        self.__convert_voice()


if __name__ == '__main__':
    voice_converter = VoiceConverter('clb', 'slt')
    voice_converter.run()
