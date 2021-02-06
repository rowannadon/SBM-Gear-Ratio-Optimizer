#!/usr/bin/python

import sys

class Gearbox:
  
  def __init__(self, min_teeth, max_teeth, stages, target_ratio):
    self.stages = stages
    self.min_teeth = min_teeth
    self.max_teeth = max_teeth+1
    self.target_ratio = target_ratio
    self.ratio = 0
    self.gears = []
    self.current_best_error = 100

  def optimize(self):
    self.loop(self.min_teeth, self.max_teeth, [0 for i in range(self.stages*2)], self.stages*2)
    return


  def loop(self, min, max, current_index, loop_counter):
    if (loop_counter == 0):
      ratio = 1.0
      for i in range(0, len(current_index)//2):
        ratio *= current_index[2*i+1]/current_index[2*i]
      err = abs(ratio-self.target_ratio)
      if (err < self.current_best_error):
        self.current_best_error = err
        self.ratio = ratio
        self.gears[:] = current_index[:]
      return
    else:
      for i in range(min, max):
        current_index[loop_counter-1] = i
        if (self.target_ratio <= 1):
          self.loop(i, max, current_index, loop_counter-1)
        else:
          self.loop(min, i, current_index, loop_counter-1)

def main():
  try:
    stages = int(sys.argv[1])
    ratio = float(sys.argv[2])
    min_teeth = int(sys.argv[3])
    max_teeth = int(sys.argv[4])
  except ValueError:
    print("Invalid input types! Usage: ./optimize_gear_ratio <int> <float> <int> <int>")
    exit()
  except IndexError:
    print("Invalid input number! Usage: ./optimize_gear_ratio <max stages> <output ratio> <min gear teeth> <max gear teeth>")
    exit()


  gb = Gearbox(min_teeth, max_teeth, stages, ratio)
  gb.optimize()

  for i in range(0, len(gb.gears)//2):
    gear = gb.gears[2*i+1]
    pinion = gb.gears[2*i]
    print("Stage:", i)
    print("\tPinion:", pinion)
    print("\tGear:", gear)
  
  print("Target final gear ratio was:", gb.target_ratio)
  print("Final gear ratio after optimization:", gb.ratio)
  print("Error compared to target ratio:", gb.current_best_error)
 

if __name__ == "__main__":
  main()