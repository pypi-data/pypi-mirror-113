"""
Plates
"""

import numpy as np
import pandas as pd

from .plate import Plate

class Plates(Plate):
    """Class for handling multiple Plate-like objects"""
    
    def __init__(
        self,
        plate_list,
        plate_name=None,
        name_list=None,
        # Plate args if non-plate obj is passed
        locations=None,
        values=None,
        case=None,
        zero_padding=None,
    ):
        # Assign attributes
        self.plate_list = plate_list
        self.plate_name = plate_name
        self.name_list = name_list
        self._locations = locations
        self._values = values
        self._case = case
        self._zero_padding = zero_padding

        self = self._generate_plates()

    def _generate_plates(self):
        # Get type of plate_list passed
        ziplike = (True if isinstance(self.plate_list[0], (list, tuple))
                        else False)

        # If list of plate-like objs: [obj, obj, ...]
        if not ziplike:
            # Assign column name
            if self.plate_name is None:
                self.plate_name = 'plate'

                # Assign the plate name values for each plate
                if self.name_list is None:
                    self.name_list = range(1, len(self.plate_list)+1)
            # else:
                # for plate in self.plate_name:
                #     try:
                #         plate[plate_name]
                #     except KeyError:
                #         raise ValueError(
                #             f'{plate_name} not found in your columns, options'\
                #             f' are {plate.columns}.'
                #         )
        
        # If list of plate-name pairs: [(obj, 1), (obj, 2), ...]
        elif ziplike:
            # Unzip
            self.plate_list, self.name_list = (
                [plate for (plate, name) in self.plate_list],
                [name for (plate, name) in self.plate_list]
            )

            # Assign column name
            if self.plate_name is None:
                self.plate_name = 'plate'

        # Determine if Plate or DataFrame
        df_bool = [True for plate in self.plate_list
                      if isinstance(plate, pd.DataFrame)]
        if sum(df_bool) == len(self.plate_list):
            df_bool = True
        elif not df_bool:
            df_bool = False
        else:
            raise ValueError(
                'Mixed object types are not allowed in Plates'
            )
        
        # Make plates
        if df_bool:
            plates = []
            for df in self.plate_list:
                plate = Plate(
                    df,
                    value_name=self._value_name,
                    zero_padding=self._zero_padding,
                    case=self._case
                )
                plate.locations = self._locations
                plate.values = self._values
                plates.append(plates)
            
            self.plate_list = plates

        # Check that all objects are the same
        locations = [plate.locations for plate in self.plate_list]
        annotations = [plate.annotations for plate in self.plate_list]
        values = [plate.values for plate in self.plate_list]
        for plate_attr in (locations, annotations, values):
            differences = set(plate_attr[0]).difference(*plate_attr[1:])
            if differences:
                raise ValueError(
                    'Plate objects contain unmatched data columns'
                )

        

        # Add plate name data
        # if self.name_list is None:
        #     for plate in self.plate_list: