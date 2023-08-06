
import numpy as np


class Data2D:
    @staticmethod
    def to_np_array(data2d):
        data2d = np.array(data2d)
        dshape = data2d.shape
        if len(dshape) != 2:
            print('[to_np_array] dshape != 2')
            # raise RuntimeError
            return None
        # else:
        #     nvariables = dshape[0]
        #     nsamples = dshape[1]
        return data2d

    @staticmethod
    def search_and_replace_nan(data2d, maxnum_nan):
        dshape = data2d.shape
        if len(dshape) != 2:
            print('[search_and_replace_nan] dshape != 2')
            return None
        else:
            nvariables = dshape[0]
            nsamples = dshape[1]
            _ = nsamples

        # Correct for NaN in data_matrix
        # data2d = [data1_arr, data2_arr, .. , datan_arr]

        for i in range(0, nvariables):
            datai_arr = data2d[i]
            indx_nan = np.argwhere(np.isnan(datai_arr))
            num_nan = len(indx_nan)
            if num_nan <= maxnum_nan:
                # Assign previous value
                datai_arr[indx_nan] = datai_arr[indx_nan - 1]
            else:
                print('[search_and_replace_nan] Too many NaN in data2d[%s]' % i)
                print('[search_and_replace_nan] num_nan %s' % num_nan)
                # raise RuntimeError
                return None

        return data2d
