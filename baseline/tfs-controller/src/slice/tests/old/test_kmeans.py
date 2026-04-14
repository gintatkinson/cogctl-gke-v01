# Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import pandas, random, sys
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from typing import Dict, List, Tuple

def get_random_slices(count : int) -> List[Tuple[str, float, float]]:
    slices = list()
    for i in range(count):
        slice_name          = 'slice-{:03d}'.format(i)
        slice_availability  = random.uniform(00.0, 99.99)
        slice_capacity_gbps = random.uniform(0.1, 100.0)
        slices.append((slice_name, slice_availability, slice_capacity_gbps))
    return slices

def init_kmeans() -> Tuple[KMeans, Dict[str, int]]:
    groups = [
        # Name, avail[0..100], bw_gbps[0..100]
        ('silver',   25.0,  50.0), # ('silver',   25.0,  25.0),
        ('gold',     90.0,  10.0), # ('gold',     90.0,  50.0),
        ('platinum', 99.0, 100.0),
    ]
    df_groups = pandas.DataFrame(groups, columns=['name', 'availability', 'capacity'])

    num_clusters = len(groups)
    k_means = KMeans(n_clusters=num_clusters)
    k_means.fit(df_groups[['availability', 'capacity']])

    df_groups['label'] = k_means.predict(df_groups[['availability', 'capacity']])
    mapping = {group['name']:group['label'] for group in list(df_groups.to_dict('records'))}

    return k_means, mapping

def main():
    k_means, mapping = init_kmeans()
    slices = get_random_slices(500)
    df_slices = pandas.DataFrame(slices, columns=['slice_uuid', 'availability', 'capacity'])

    # predict one
    #sample = df_slices[['availability', 'capacity']].iloc[[0]]
    #y_predicted = k_means.predict(sample)
    #y_predicted

    df_slices['group'] = k_means.predict(df_slices[['availability', 'capacity']])

    df_silver   = df_slices[df_slices['group']==mapping['silver']]
    df_gold     = df_slices[df_slices['group']==mapping['gold']]
    df_platinum = df_slices[df_slices['group']==mapping['platinum']]

    plt.scatter(df_silver.availability,         df_silver.capacity,             s=25,  c='black' )
    plt.scatter(df_gold.availability,           df_gold.capacity,               s=25,  c='gold'  )
    plt.scatter(df_platinum.availability,       df_platinum.capacity,           s=25,  c='silver')
    plt.scatter(k_means.cluster_centers_[:, 0], k_means.cluster_centers_[:, 1], s=100, c='red'   )
    plt.xlabel('service-slo-availability')
    plt.ylabel('service-slo-one-way-bandwidth')
    #ax = plt.subplot(1, 1, 1)
    #ax.set_ylim(bottom=0., top=1.)
    #ax.set_xlim(left=0.)
    plt.savefig('slice_grouping.png')
    return 0

if __name__ == '__main__':
    sys.exit(main())
