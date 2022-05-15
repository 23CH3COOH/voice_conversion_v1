# -*- coding: utf-8 -*-
import os
from extract_mcep import wav_to_mcep
from align_mcep import align_mcep, draw_aligned_mceps, DrawingAlignedMcepsItems
from train_gmm import train_gmm
from convert_voice import convert_voice
from common import binary_to_text

wav_s = 'wav/train/%s/'
mcep_s = 'mcep/%s/'
mcep_text_s = 'mcep/%s/text/'
aligned_mcep_sss = 'mcep_aligned/%s_to_%s/%s/'
aligned_mcep_text_sss = 'mcep_aligned/%s_to_%s/%s/text/'
aligned_mcep_graph_sss = 'mcep_aligned/%s_to_%s/graph/%s/'
train_ss = 'train_result/%s_to_%s/'
wav_prod = 'wav/production/%s/'

settings_file = 'settings.txt'
gmm_file = 'GMM.gmm'
wavf_s = '%s.wav'
mcepf_s = '%s.mcep'
mcep_textf_s = '%s.mcep_ascii'
pngf_d = '%d-th.png'


class VoiceConverter:
    def __init__(self, conv_from, conv_to, output_visible_form=True):
        self.__from = conv_from
        self.__to = conv_to
        self.__output_visible_form = output_visible_form

    def __load_settings(self):
        f = open(settings_file)
        rows = f.readlines()
        f.close()

        parsed = dict()
        for row in rows:
            if '#' in row or not '=' in row:
                continue
            splited = row.split('=')
            parsed[splited[0]] = splited[1].strip()

        self.__m = int(parsed['m'])
        self.__a = float(parsed['a'])
        self.__e = float(parsed['e'])
        self.__K = int(parsed['K'])
        self.__ch = int(parsed['channel'])
        self.__fr = int(parsed['frame_rate'])
        self.__exc = bool(int(parsed['exclude_both_mcep_ends']))

    def __search_common_wav_files(self):
        wav_files_from = os.listdir(wav_s % self.__from)
        wav_files_to = os.listdir(wav_s % self.__to)
        wav_files = list(set(wav_files_from) & set(wav_files_to))
        # 拡張子無しのファイル名リストの状態で保持しておく
        self.__train_files = [file.replace('.wav', '') for file in wav_files]

    def __output_extracted_mcep_to_text(self):
        if not os.path.exists(mcep_text_s % self.__from):
            os.makedirs(mcep_text_s % self.__from)
        if not os.path.exists(mcep_text_s % self.__to):
            os.makedirs(mcep_text_s % self.__to)

        for file in self.__train_files:
            mcep_path = mcep_s % self.__from + mcepf_s % file
            text_path = mcep_text_s % self.__from + mcep_textf_s % file
            binary_to_text(mcep_path, text_path, self.__m + 1)
            mcep_path = mcep_s % self.__to + mcepf_s % file
            text_path = mcep_text_s % self.__to + mcep_textf_s % file
            binary_to_text(mcep_path, text_path, self.__m + 1)

    def __extract_mcep(self):
        if not os.path.exists(mcep_s % self.__from):
            os.makedirs(mcep_s % self.__from)
        if not os.path.exists(mcep_s % self.__to):
            os.makedirs(mcep_s % self.__to)

        for file in self.__train_files:
            wave_path = wav_s % self.__from + wavf_s % file
            mcep_path = mcep_s % self.__from + mcepf_s % file
            wav_to_mcep(wave_path, mcep_path, self.__m, self.__a, self.__e)
            wave_path = wav_s % self.__to + wavf_s % file
            mcep_path = mcep_s % self.__to + mcepf_s % file
            wav_to_mcep(wave_path, mcep_path, self.__m, self.__a, self.__e)

    def __output_aligned_mcep_to_text(self):
        indir_from = aligned_mcep_sss % (self.__from, self.__to, self.__from)
        indir_to = aligned_mcep_sss % (self.__from, self.__to, self.__to)
        outdir_from = aligned_mcep_text_sss % (self.__from, self.__to, self.__from)
        outdir_to = aligned_mcep_text_sss % (self.__from, self.__to, self.__to)
        if not os.path.exists(outdir_from):
            os.makedirs(outdir_from)
        if not os.path.exists(outdir_to):
            os.makedirs(outdir_to)

        for file in self.__train_files:
            mcep_path = indir_from + mcepf_s % file
            text_path = outdir_from + mcep_textf_s % file
            binary_to_text(mcep_path, text_path, self.__m + 1)
            mcep_path = indir_to + mcepf_s % file
            text_path = outdir_to + mcep_textf_s % file
            binary_to_text(mcep_path, text_path, self.__m + 1)

    def __output_aligned_mcep_to_graph(self):
        prev_from = mcep_text_s % self.__from
        prev_to = mcep_text_s % self.__to
        result_from = aligned_mcep_text_sss % (self.__from, self.__to, self.__from)
        result_to = aligned_mcep_text_sss % (self.__from, self.__to, self.__to)

        for file in self.__train_files:
            outdir = aligned_mcep_graph_sss % (self.__from, self.__to, file)
            if not os.path.exists(outdir):
                os.makedirs(outdir)

            for i in range(self.__m + 1):
                items_1 = DrawingAlignedMcepsItems()
                items_1.name = self.__from
                items_1.mcep_path_prev = prev_from + mcep_textf_s % file
                items_1.mcep_path_result = result_from + mcep_textf_s % file
                items_2 = DrawingAlignedMcepsItems()
                items_2.name = self.__to
                items_2.mcep_path_prev = prev_to + mcep_textf_s % file
                items_2.mcep_path_result = result_to + mcep_textf_s % file
                draw_aligned_mceps(items_1, items_2, i, outdir + pngf_d % i)

    def __align_mcep(self):
        outdir_from = aligned_mcep_sss % (self.__from, self.__to, self.__from)
        outdir_to = aligned_mcep_sss % (self.__from, self.__to, self.__to)
        if not os.path.exists(outdir_from):
            os.makedirs(outdir_from)
        if not os.path.exists(outdir_to):
            os.makedirs(outdir_to)

        for file in self.__train_files:
            mcep_from = mcep_s % self.__from + mcepf_s % file
            mcep_to = mcep_s % self.__to + mcepf_s % file
            align_from = outdir_from + mcepf_s % file
            align_to = outdir_to + mcepf_s % file
            align_mcep(mcep_from, mcep_to, align_from, align_to, self.__m)

    def __train_gmm(self):
        outdir = train_ss % (self.__from, self.__to)
        if not os.path.exists(outdir):
            os.makedirs(outdir)

        mcep_from = aligned_mcep_sss % (self.__from, self.__to, self.__from)
        mcep_to = aligned_mcep_sss % (self.__from, self.__to, self.__to)
        paths_from = [mcep_from + mcepf_s % f for f in self.__train_files]
        paths_to = [mcep_to + mcepf_s % f for f in self.__train_files]
        train_gmm(paths_from, paths_to, outdir, self.__m, self.__K, self.__exc)

    def __convert_voice(self):
        if not os.path.exists(wav_prod % self.__to):
            os.makedirs(wav_prod % self.__to)

        gmm_path = train_ss % (self.__from, self.__to) + gmm_file
        for file in os.listdir(wav_prod % self.__from):
            wav_path_from = wav_prod % self.__from + file
            wav_path_to = wav_prod % self.__to + file
            convert_voice(wav_path_from, wav_path_to, gmm_path,
                self.__ch, self.__fr, self.__m, self.__a, self.__e, self.__K)

    def run(self):
        self.__search_common_wav_files()
        self.__load_settings()
        print('Extracting mel cepstrum...')
        self.__extract_mcep()
        if self.__output_visible_form:
            self.__output_extracted_mcep_to_text()
        print('Aligning mel cepstrum...')
        self.__align_mcep()
        if self.__output_visible_form:
            self.__output_aligned_mcep_to_text()
            self.__output_aligned_mcep_to_graph()
        print('Training...')
        self.__train_gmm()
        print('Converting voice...')
        self.__convert_voice()


if __name__ == '__main__':
    voice_converter = VoiceConverter('clb', 'slt')
    voice_converter.run()
