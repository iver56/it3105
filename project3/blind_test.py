from classify import Classify


class ann(object):
    @staticmethod
    def blind_test(feature_sets):
        classifier = Classify(init=False)
        classifier.network_filename = 'hl2__sizes-300-500-__acfn-linear-linear-__dr-0.2-0.5-0.5-__lr0.1__mb100__mom0.9__seed10.hdf5'
        classifier.initialize_network()

        labels = []
        for image in feature_sets:
            image_1d = map(lambda value: value / 255.0, image)
            image_2d = []
            for row_idx in range(28):
                image_2d.append([])
                for col_idx in range(28):
                    image_2d[row_idx].append(image_1d[row_idx * 28 + col_idx])

            label = classifier.classify(image_2d)
            labels.append(label)
        return labels
