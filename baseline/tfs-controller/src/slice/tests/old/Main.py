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

import logging, os, pandas, random, sys, time
#from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from typing import Dict, List, Tuple

os.environ['METRICSDB_HOSTNAME' ] = '127.0.0.1' #'questdb-public.qdb.svc.cluster.local'
os.environ['METRICSDB_ILP_PORT' ] = '9009'
os.environ['METRICSDB_REST_PORT'] = '9000'

from .MetricsExporter import MetricsExporter # pylint: disable=wrong-import-position

logging.basicConfig(level=logging.DEBUG)
LOGGER : logging.Logger = logging.getLogger(__name__)

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
        ('bronze',   10.0,  10.0), # ('silver',   25.0,  25.0),
        ('silver',   30.0,  40.0), # ('silver',   25.0,  25.0),
        ('gold',     70.0,  50.0), # ('gold',     90.0,  50.0),
        ('platinum', 99.0, 100.0),
    ]
    df_groups = pandas.DataFrame(groups, columns=['name', 'availability', 'capacity'])

    num_clusters = len(groups)
    k_means = KMeans(n_clusters=num_clusters)
    k_means.fit(df_groups[['availability', 'capacity']])

    df_groups['label'] = k_means.predict(df_groups[['availability', 'capacity']])
    mapping = {
        group['name']:{k:v for k,v in group.items() if k != 'name'}
        for group in list(df_groups.to_dict('records'))
    }

    return k_means, mapping

def main():
    LOGGER.info('Starting...')
    metrics_exporter = MetricsExporter()
    metrics_exporter.create_table()

    k_means, mapping = init_kmeans()
    label_to_group = {}
    for group_name,group_attrs in mapping.items():
        label = group_attrs['label']
        availability = group_attrs['availability']
        capacity = group_attrs['capacity']
        metrics_exporter.export_point(group_name, group_name, availability, capacity, is_center=True)
        label_to_group[label] = group_name

    slices = get_random_slices(10000)
    for slice_ in slices:
        sample = pandas.DataFrame([slice_[1:3]], columns=['availability', 'capacity'])
        sample['label'] = k_means.predict(sample)
        sample = sample.to_dict('records')[0]
        label = sample['label']
        availability = sample['availability']
        capacity = sample['capacity']
        group_name = label_to_group[label]
        metrics_exporter.export_point(slice_[0], group_name, availability, capacity, is_center=False)
        time.sleep(0.01)

    #df_silver   = df_slices[df_slices['group']==mapping['silver']]
    #df_gold     = df_slices[df_slices['group']==mapping['gold']]
    #df_platinum = df_slices[df_slices['group']==mapping['platinum']]
    #plt.scatter(df_silver.availability,         df_silver.capacity,             s=25,  c='black' )
    #plt.scatter(df_gold.availability,           df_gold.capacity,               s=25,  c='gold'  )
    #plt.scatter(df_platinum.availability,       df_platinum.capacity,           s=25,  c='silver')
    #plt.scatter(k_means.cluster_centers_[:, 0], k_means.cluster_centers_[:, 1], s=100, c='red'   )

    LOGGER.info('Bye')
    return 0

if __name__ == '__main__':
    sys.exit(main())
