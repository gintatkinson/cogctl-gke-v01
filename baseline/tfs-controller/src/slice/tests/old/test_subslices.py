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


import sqlalchemy, sys
from sqlalchemy import Column, ForeignKey, String, event, insert
from sqlalchemy.orm import Session, declarative_base, relationship
from typing import Dict

def _fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute('pragma foreign_keys=ON')

_Base = declarative_base()

class SliceModel(_Base):
    __tablename__ = 'slice'

    slice_uuid = Column(String, primary_key=True)

    slice_subslices = relationship(
        'SliceSubSliceModel', primaryjoin='slice.c.slice_uuid == slice_subslice.c.slice_uuid')

    def dump_id(self) -> Dict:
        return {'uuid': self.slice_uuid}

    def dump(self) -> Dict:
        return {
            'slice_id': self.dump_id(),
            'slice_subslice_ids': [
                slice_subslice.subslice.dump_id()
                for slice_subslice in self.slice_subslices
            ]
        }

class SliceSubSliceModel(_Base):
    __tablename__ = 'slice_subslice'

    slice_uuid    = Column(ForeignKey('slice.slice_uuid', ondelete='CASCADE' ), primary_key=True)
    subslice_uuid = Column(ForeignKey('slice.slice_uuid', ondelete='RESTRICT'), primary_key=True)

    slice    = relationship('SliceModel', foreign_keys='SliceSubSliceModel.slice_uuid', back_populates='slice_subslices', lazy='joined')
    subslice = relationship('SliceModel', foreign_keys='SliceSubSliceModel.subslice_uuid', lazy='joined')

def main():
    engine = sqlalchemy.create_engine('sqlite:///:memory:', echo=False, future=True)
    event.listen(engine, 'connect', _fk_pragma_on_connect)

    _Base.metadata.create_all(engine)

    slice_data = [
        {'slice_uuid': 'slice-01'},
        {'slice_uuid': 'slice-01-01'},
        {'slice_uuid': 'slice-01-02'},
    ]

    slice_subslices_data = [
        {'slice_uuid': 'slice-01', 'subslice_uuid': 'slice-01-01'},
        {'slice_uuid': 'slice-01', 'subslice_uuid': 'slice-01-02'},
    ]

    # insert
    with engine.connect() as conn:
        conn.execute(insert(SliceModel).values(slice_data))
        conn.execute(insert(SliceSubSliceModel).values(slice_subslices_data))
        conn.commit()

    # read
    with Session(engine) as session:
        obj_list = session.query(SliceModel).all()
        print([obj.dump() for obj in obj_list])
        session.commit()

    return 0

if __name__ == '__main__':
    sys.exit(main())

[
    {'slice_id': {'uuid': 'slice-01'}, 'slice_subslice_ids': [
        {'uuid': 'slice-01-01'},
        {'uuid': 'slice-01-02'}
    ]},
    {'slice_id': {'uuid': 'slice-01-01'}, 'slice_subslice_ids': []},
    {'slice_id': {'uuid': 'slice-01-02'}, 'slice_subslice_ids': []}
]
