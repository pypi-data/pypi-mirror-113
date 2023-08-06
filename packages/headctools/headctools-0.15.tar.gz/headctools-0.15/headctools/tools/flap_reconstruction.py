import os
import os.path as osp
import tempfile

import SimpleITK as sitk
from SimpleITK import Show as sh
from ctunet.pytorch.train_test import Model

from .. import utilities as common
from ..Preprocessor import prep_img_cr


class FlapReconstruction:
    def __init__(self, input_ff, out_path=None, model_path=None,
                 ext='.nii.gz', show_intermediate=False, skip_prep=False):
        self.model_path = model_path
        self.input_ff = input_ff
        self.ext = ext
        self.sh_imgs = show_intermediate
        self.skip_prep = skip_prep

        alt_out_f = osp.join(input_ff, 'reconstructed') if osp.isdir(
            input_ff) else osp.join(osp.split(input_ff)[0], 'reconstructed')
        self.out_folder_path = out_path if out_path else alt_out_f

        self.run()

    def run(self):
        if osp.isdir(self.input_ff):
            self.flaprec_folder(self.input_ff)
        if osp.isfile(self.input_ff):
            self.flaprec_file(self.input_ff)

    def flaprec_folder(self, input_folder):
        common.veri_folder(self.out_folder_path)
        for file in os.listdir(input_folder):
            if file.endswith(self.ext):
                self.flaprec_file(osp.join(input_folder, file))

    def flaprec_file(self, input_file):
        common.veri_folder(self.out_folder_path)
        self.check_model_exists(self.model_path)

        fname = os.path.split(input_file)[1]
        out_flap = osp.join(self.out_folder_path,
                            fname.replace(self.ext, '_fl' + self.ext))
        out_inputsk = osp.join(self.out_folder_path,
                               fname.replace(self.ext, '_i' + self.ext))
        out_fullsk = osp.join(self.out_folder_path,
                              fname.replace(self.ext, '_sk' + self.ext))

        sh(sitk.ReadImage(input_file), 'input-image') if self.sh_imgs else 0

        # Preprocess
        if self.skip_prep is False:
            # Temp file
            prep_file = tempfile.NamedTemporaryFile(suffix='.nii.gz',
                                                    delete=False)
            prep_file_path = prep_file.name
            prep_file_folder, prep_file_name = os.path.split(prep_file_path)

            prep_img_cr(input_file, out_ff=prep_file_path,
                        image_identifier=None, mask_identifier=None,
                        generate_csv=False, overwrite=False)
            sh(sitk.ReadImage(prep_file_path),
               'prepr-img') if self.sh_imgs else 0

        else:
            prep_file_path = input_file
            prep_file_folder, prep_file_name = os.path.split(prep_file_path)

        # PyTorch model
        params = {
            "name": ('default' if not self.model_path else ''),
            "train_flag": False,
            "test_flag": True,
            "model_class": 'UNetSP',
            "problem_handler": 'FlapRecWithShapePriorDoubleOut',
            "workspace_path": '~/headctools',  # It will lookup the model here.
            "single_file": prep_file_path,
            "device": 'cuda',
            "resume_model": (self.model_path if self.model_path else ''),
        }
        Model(params=params)

        mod_fn = None  # Model filename (will be used in the out folder name)
        if self.model_path:
            mod_fn = os.path.splitext(os.path.split(self.model_path)[1])[0]
        out_folder = 'pred_' + 'default' if not self.model_path else mod_fn

        pred_flap = os.path.join(prep_file_folder, out_folder,
                                 prep_file_name.replace(self.ext,
                                                        '_fl' + self.ext))
        pred_input = os.path.join(prep_file_folder, out_folder,
                                  prep_file_name.replace(self.ext,
                                                         '_i' + self.ext))
        pred_skull = os.path.join(prep_file_folder, out_folder,
                                  prep_file_name.replace(self.ext,
                                                         '_sk' + self.ext))

        # Sum Skull + Flap
        fl_stk = sitk.ReadImage(pred_flap)
        inp_stk = sitk.ReadImage(pred_input)
        fullsk_stk = sitk.ReadImage(pred_skull)

        sh(fl_stk, 'generated-flap') if self.sh_imgs else 0
        sh(inp_stk, 'input-img') if self.sh_imgs else 0
        sh(fullsk_stk, 'generated-skull') if self.sh_imgs else 0
        sitk.WriteImage(fl_stk, out_flap)
        sitk.WriteImage(inp_stk, out_inputsk)
        sitk.WriteImage(fullsk_stk, out_fullsk)

        prep_file.close() if not self.skip_prep else 0

    def check_model_exists(self, model_path=None):
        """ Check if model exists and throw an error in case it doesn't.

        :param model_path: If a default model isn't loaded, use this model.
        :return:
        """

        model_path = model_path if model_path else os.path.expanduser(
            '~/headctools/UNetSP_FlapRecWithShapePriorDoubleOut/model/default'
            '.pt')

        if not os.path.exists(model_path):
            raise FileNotFoundError("The UNetSP model was not found. "
                                    "Download the default model with: "
                                    "'headctools download UNetSP'.")


if __name__ == "__main__":
    FlapReconstruction('/home/fmatzkin/Code/datasets/test_pypi',
                       show_intermediate=True)
