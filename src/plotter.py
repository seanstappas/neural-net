from __future__ import division

import os
import matplotlib.pyplot as plt
import pandas as pd

from matplotlib.ticker import MaxNLocator

from mnist_hello_world import test_mnist_one_hot

plt.rcParams["font.family"] = "Times New Roman"
NUM_DATA_POINTS = 35
LOGS_DIRECTORY = 'csv'


def plot_directory(directory, x_label, y_label):
    f = plt.figure()
    ax = f.gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    for filename in os.listdir(directory):
        x_range = pd.read_csv(os.path.join(directory, filename))[x_label][1:NUM_DATA_POINTS]
        y_range = pd.read_csv(os.path.join(directory, filename))[y_label][1:NUM_DATA_POINTS]
        splt = filename.split('.')[0].split('_')
        plt.plot(x_range, y_range, label='learning_rate={}%, learning_decay={}%'.format(splt[2], splt[4]))
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.grid(True)
    f.savefig('plots/{}_vs_{}.pdf'.format(y_label, x_label), bbox_inches='tight')


def plot_csv_simple(filename):
    f = plt.figure()
    ax = f.gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    csv_file = pd.read_csv('csv/{}.csv'.format(filename))
    x_range = csv_file['epoch']
    y_range = csv_file['test_accuracy']
    plt.plot(x_range, y_range)
    plt.xlabel('Epoch')
    plt.ylabel('Test Accuracy')
    plt.grid(True)
    f.savefig('plots/{}.pdf'.format(filename), bbox_inches='tight')


def plot_test_accuracy_simple(y_range, filename):
    f = plt.figure()
    ax = f.gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    x_range = [i for i in range(100)]
    plt.plot(x_range, y_range)
    plt.xlabel('Epoch')
    plt.ylabel('Test Accuracy')
    plt.grid(True)
    f.savefig('plots/{}.pdf'.format(filename), bbox_inches='tight')


def plot_test_accuracy_multiple(y_ranges, labels, filename):
    f = plt.figure()
    ax = f.gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    x_range = [i for i in range(100)]
    for y_range, label in zip(y_ranges, labels):
        plt.plot(x_range, y_range, label=label)
    plt.xlabel('Epoch')
    plt.ylabel('Test Accuracy')
    plt.legend()
    plt.grid(True)
    f.savefig('plots/{}.pdf'.format(filename), bbox_inches='tight')


def plot_network_size():
    filename = 'network_size'
    test_accuracies = test_mnist_one_hot(csv_filename=filename)
    plot_test_accuracy_simple(test_accuracies, filename)


def plot_logistic_vs_tanh():
    # TODO: Logistic memory error?
    test_accuracies_logistic = test_mnist_one_hot(sigmoid='logistic', csv_filename='logistic')
    test_accuracies_tanh = test_mnist_one_hot(sigmoid='tanh', csv_filename='tanh')
    plot_test_accuracy_multiple((test_accuracies_logistic, test_accuracies_tanh), ('logistic', 'tanh'),
                                'logistic_vs_tanh')


def plot_batch_size():
    batch_sizes = [1, 10, 100]
    accuracy_ranges = []
    labels = []
    for batch_size in batch_sizes:
        test_accuracies = test_mnist_one_hot(batch_size=batch_size, csv_filename='batch_size_{}'.format(batch_size))
        accuracy_ranges.append(test_accuracies)
        labels.append('batch_size = {}'.format(batch_size))
    plot_test_accuracy_multiple(accuracy_ranges, labels, 'batch_size')


def plot_momentum():
    # 0.0 to 1.0 in 0.1
    momenta = [i / 10 for i in range(11)]
    accuracy_ranges = []
    labels = []
    for momentum in momenta:
        test_accuracies = test_mnist_one_hot(momentum=momentum, csv_filename='momentum_{}'.format(momentum * 100))
        accuracy_ranges.append(test_accuracies)
        labels.append('momentum = {}'.format(momentum))
    plot_test_accuracy_multiple(accuracy_ranges, labels, 'momentum')


def plot_learning_rate_decay():
    # 0.7, 0.8, 0.9, 0.99, 1
    learning_rate_decays = [0.7, 0.8, 0.9, 0.99, 1]
    accuracy_ranges = []
    labels = []
    for learning_rate_decay in learning_rate_decays:
        test_accuracies = test_mnist_one_hot(learning_decay=learning_rate_decay,
                                             csv_filename='learning_rate_decay_{}'.format(learning_rate_decay * 100))
        accuracy_ranges.append(test_accuracies)
        labels.append('learning_rate_decay = {}'.format(learning_rate_decay))
    plot_test_accuracy_multiple(accuracy_ranges, labels, 'learning_rate_decay')


if __name__ == '__main__':
    plot_network_size()
    plot_logistic_vs_tanh()
    plot_batch_size()
    plot_momentum()
    plot_learning_rate_decay()
    # TODO: Zoom into plots (starting at epoch 1)

