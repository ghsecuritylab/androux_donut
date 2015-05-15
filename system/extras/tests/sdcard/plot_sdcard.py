#!/usr/bin/python2.5
#
# Copyright 2009, The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""plot_sdcard: A module to plot the results of an sdcard perf test.

Requires Gnuplot python v 1.8

Typical usage:
 -t x axis is time
 -i x axis is iteration
 -p profile data generated by profile_sdcard.sh

./plot_sdcard.py -t /tmp/data.txt
./plot_sdcard.py -i /tmp/data.txt
./plot_sdcard.py -p

python interpreter
>>> import plot_sdcard as p
>>> (metadata, data) = p.Parse('/tmp/data.txt')
>>> p.PlotIterations(metadata, data)
>>> p.PlotTimes(metadata, data)

"""

import getopt
from itertools import izip
import re
import sys
import Gnuplot
import numpy


class DataSet(object):
  """Dataset holds the summary and data (time,value pairs)."""

  def __init__(self, line):
    res = re.search(('# StopWatch ([\w]+) total/cumulative '
                     'duration ([0-9.]+). Samples: ([0-9]+)'), line)
    self.time = []
    self.data = []
    self.name = res.group(1)
    self.duration = float(res.group(2))
    self.iteration = int(res.group(3))
    self.summary = re.match('([a-z_]+)_total', self.name)

  def __repr__(self):
    return str(zip(self.time, self.data))

  def Add(self, time, value):
    self.time.append(time)
    self.data.append(value)

  def RescaleTo(self, length):
    factor = len(self.data) / length

    if factor > 1:
      new_time = []
      new_data = []
      accum = 0.0
      idx = 1
      for t, d in izip(self.time, self.data):
        accum += d
        if idx % factor == 0:
          new_time.append(t)
          new_data.append(accum / factor)
          accum = 0
        idx += 1
      self.time = new_time
      self.data = new_data


class Metadata(object):
  def __init__(self):
    self.kernel = ''
    self.command_line = ''
    self.sched = ''
    self.name = ''
    self.fadvise = ''
    self.iterations = 0
    self.duration = 0.0
    self.complete = False

  def Parse(self, line):
    if line.startswith('# Kernel:'):
      self.kernel = re.search('Linux version ([0-9.]+-[0-9]+)', line).group(1)
    elif line.startswith('# Command:'):
      self.command_line = re.search('# Command: [/\w_]+ (.*)', line).group(1)
      self.command_line = self.command_line.replace(' --', '-')
      self.command_line = self.command_line.replace(' -d', '')
      self.command_line = self.command_line.replace('--test=', '')
    elif line.startswith('# Iterations'):
      self.iterations = int(re.search('# Iterations: ([0-9]+)', line).group(1))
    elif line.startswith('# Fadvise'):
      self.fadvise = re.search('# Fadvise: ([\w]+)', line).group(1)
    elif line.startswith('# Sched'):
      self.sched = re.search('# Sched features: ([\w]+)', line).group(1)
      self.complete = True

  def AsTitle(self):
    return '%s-duration:%f\\n-%s\\n%s' % (
        self.kernel, self.duration, self.command_line, self.sched)

  def UpdateWith(self, dataset):
    self.duration = max(self.duration, dataset.duration)
    self.name = dataset.name


def Parse(filename):
  """Parse a file with the collected data.

  The data must be in 2 rows (x,y).

  Args:
    filename: Full path to the file.
  """

  f = open(filename, 'r')

  metadata = Metadata()
  data = []  # array of dataset
  dataset = None

  for num, line in enumerate(f):
    try:
      line = line.strip()
      if not line: continue

      if not metadata.complete:
        metadata.Parse(line)
        continue

      if re.match('[a-z_]', line):
        continue

      if line.startswith('# StopWatch'):  # Start of a new dataset
        if dataset:
          if dataset.summary:
            metadata.UpdateWith(dataset)
          else:
            data.append(dataset)

        dataset = DataSet(line)
        continue

      if line.startswith('#'):
        continue

      # must be data at this stage
      try:
        (time, value) = line.split(None, 1)
      except ValueError:
        print 'skipping line %d: %s' % (num, line)
        continue

      if dataset and not dataset.summary:
        dataset.Add(float(time), float(value))

    except Exception:
      print 'Error parsing line %d' % num, sys.exc_info()[0]
      raise
  data.append(dataset)
  if not metadata.complete:
    print """Error missing metadata. Did you mount debugfs?
    [adb shell mount -t debugfs none /sys/kernel/debug]"""
    sys.exit(1)
  return (metadata, data)


def PlotIterations(metadata, data):
  """Plot the duration of the ops against iteration.

  If you are plotting data with widely different runtimes you probably want to
  use PlotTimes instead.

  For instance when readers and writers are in the same mix, the
  readers will go thru 100 iterations much faster than the
  writers. The load test tries to be smart about that but the final
  iterations of the writers will likely be done w/o any influence from
  the readers.

  Args:
    metadata: For the graph's title.
    data: pair of to be plotted.
  """

  gp = Gnuplot.Gnuplot(persist=1)
  gp('set data style lines')
  gp.clear()
  gp.xlabel('iterations')
  gp.ylabel('duration in second')
  gp.title(metadata.AsTitle())
  styles = {}
  line_style = 1

  for dataset in data:
    dataset.RescaleTo(metadata.iterations)
    x = numpy.arange(len(dataset.data), dtype='int_')
    if not dataset.name in styles:
      styles[dataset.name] = line_style
      line_style += 1
      d = Gnuplot.Data(x, dataset.data,
                       title=dataset.name,
                       with_='lines ls %d' % styles[dataset.name])
    else:  # no need to repeat a title that exists already.
      d = Gnuplot.Data(x, dataset.data,
                       with_='lines ls %d' % styles[dataset.name])

    gp.replot(d)
  gp.hardcopy('/tmp/%s-%s-%f.png' %
              (metadata.name, metadata.kernel, metadata.duration),
              terminal='png')


def PlotTimes(metadata, data):
  """Plot the duration of the ops against time elapsed.

  Args:
    metadata: For the graph's title.
    data: pair of to be plotted.
  """

  gp = Gnuplot.Gnuplot(persist=1)
  gp('set data style impulses')
  gp('set xtics 1')
  gp.clear()
  gp.xlabel('seconds')
  gp.ylabel('duration in second')
  gp.title(metadata.AsTitle())
  styles = {}
  line_style = 1

  for dataset in data:
    x = numpy.array(dataset.time, dtype='float_')
    if not dataset.name in styles:
      styles[dataset.name] = line_style
      line_style += 1
      d = Gnuplot.Data(x, dataset.data,
                       title=dataset.name,
                       with_='impulses ls %d' % styles[dataset.name])
    else:  # no need to repeat a title that exists already.
      d = Gnuplot.Data(x, dataset.data,
                       with_='impulses ls %d' % styles[dataset.name])

    gp.replot(d)
  gp.hardcopy('/tmp/%s-%s-%f.png' %
              (metadata.name, metadata.kernel, metadata.duration),
              terminal='png')


def PlotProfile():
  """Plot the time of a run against the number of processes."""
  (metadata, data) = Parse('/tmp/sdcard-scalability.txt')
  gp = Gnuplot.Gnuplot(persist=1)
  gp('set data style impulses')
  gp('set xtics 1')
  gp('set pointsize 2')
  gp.clear()
  gp.xlabel('writer process')
  gp.ylabel('duration in second')
  gp.title(metadata.AsTitle())

  dataset = data[0]
  x = numpy.array(dataset.time, dtype='int_')
  d = Gnuplot.Data(x, dataset.data,
                   title=dataset.name,
                   with_='linespoints')
  gp.replot(d)
  gp.hardcopy('/tmp/%s-%s-%f.png' %
              (metadata.name, metadata.kernel, metadata.duration),
              terminal='png')


def Usage():
  """Print this module's usage."""
  print """
  To plot the result using the iter number of the x axis:

    plot_sdcard.py -i /tmp/data.txt

  To plot the result using time for the x axis:

    plot_sdcard.py -t /tmp/data.txt

  To plot the result from the profiler:

    profile_sdcard.sh
    plot_sdcard.py -p

  """
  sys.exit(2)


def main(argv):
  try:
    (optlist, args) = getopt.getopt(argv[1:],
                                    'itp', ['iteration', 'time', 'profile'])
  except getopt.GetoptError, err:
    print str(err)
    Usage()

  for flag, val in optlist:
    if flag in ('-i', '--iteration'):
      (metadata, data) = Parse(args[0])
      PlotIterations(metadata, data)
      sys.exit(0)
    elif flag in ('-t', '--time'):
      (metadata, data) = Parse(args[0])
      PlotTimes(metadata, data)
      sys.exit(0)
    elif flag in ('-p', '--profile'):
      PlotProfile()
      sys.exit(0)
  Usage()


if __name__ == '__main__':
  main(sys.argv)
