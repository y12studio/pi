#
# Copyright 2013 Y12Studio
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
import  m_dys388icon as ledicon
import  m_dys388dbp as ledDys388
import numpy as np
import threading,time
import m_led as led
from scipy import stats

xi = np.arange(0,9)
y = [19, 20, 20.5, 21.5, 22, 23, 23, 25.5, 24]

slope, intercept, r_value, p_value, std_err = stats.linregress(xi,y)
print 'slope',slope
print 'intercept', intercept
print 'r value', r_value
print  'p_value', p_value
print 'standard deviation', std_err

