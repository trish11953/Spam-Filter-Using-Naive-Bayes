import unittest
import homework5_tvm5513


class Test_homework5(unittest.TestCase):

    def test_load_tokens(self):
        self.assertEqual(homework5_tvm5513.load_tokens("homework5_data/train/ham/ham1")[200:204],
                         ['of', 'my', 'outstanding', 'mail'])
        self.assertEqual(homework5_tvm5513.load_tokens("homework5_data/train/spam/spam1")[1:5],
                         ['You', 'are', 'receiving', 'this'])
        self.assertEqual(homework5_tvm5513.load_tokens("homework5_data/train/ham/ham2")[110:114],
                         ['for', 'Preferences', '-', "didn't"])
        self.assertEqual(homework5_tvm5513.load_tokens("homework5_data/train/spam/spam2")[:4],
                         ['<html>', '<body>', '<center>', '<h3>'])

    def test_log_probs(self):
        path = ["homework5_data/train/ham/ham%d" % i for i in range(1, 11)]
        p = homework5_tvm5513.log_probs(path, 1e-5)
        self.assertEqual(p["the"], -3.6080194731874062)
        self.assertEqual(p["line"], -4.272995709320345)
        path_2 = ["homework5_data/train/spam/spam%d" % i for i in range(1, 11)]
        p_2 = homework5_tvm5513.log_probs(path_2, 1e-5)
        self.assertEqual(p_2["Credit"], -5.837004641921745)
        self.assertEqual(p_2["<UNK>"], -20.34566288044584)

    def test_is_spam(self):
        sf = homework5_tvm5513.SpamFilter("homework5_data/train/spam", "homework5_data/train/ham", 1e-5)
        self.assertEqual(sf.is_spam("homework5_data/train/spam/spam1"), True)
        self.assertEqual(sf.is_spam("homework5_data/train/spam/spam2"), True)
        self.assertEqual(sf.is_spam("homework5_data/train/ham/ham1"), False)
        self.assertEqual(sf.is_spam("homework5_data/train/ham/ham2"), False)

    def test_most_indicative_spam(self):
        sf = homework5_tvm5513.SpamFilter("homework5_data/train/spam", "homework5_data/train/ham", 1e-5)
        self.assertEqual(sf.most_indicative_spam(5), ['<a', '<input', '<html>', '<meta', '</head>'])
        self.assertEqual(sf.most_indicative_ham(5), ['Aug', 'ilug@linux.ie', 'install', 'spam.', 'Group:'])


if __name__ == '__main__':
    unittest.main()