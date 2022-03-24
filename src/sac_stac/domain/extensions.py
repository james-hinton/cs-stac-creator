from pystac import STAC_EXTENSIONS
from pystac.extensions.base import CollectionExtension
from pystac.extensions.base import ExtendedObject
from pystac.extensions.base import ExtensionDefinition
from pystac.extensions.base import ItemExtension
from pystac.collection import Collection
from pystac.item import Item

class Extensions:
    PRODUCT_DEFINITION = 'product_definition'
    ODC = 'odc'

class ODCExt(ItemExtension):
    def __init__(self, item: Item):
        self.item = item
        
    def apply(self, region_code=None):
        self.region_code=region_code
        
    def return_region_code():
        pass
        
    @property
    def region_code(self):
        return self.item.properties.get('odc:region_code')

    @region_code.setter
    def region_code(self, region_code):
        self.item.properties['odc:region_code'] = region_code
        
    @classmethod
    def from_item(self, item):
        return ODCExt(item)

    @classmethod
    def _object_links(cls):
        return []

class ProdefColExt(CollectionExtension):
    def __init__(self, collection):
        self.collection = collection

    def apply(self, metadata_type=None, metadata=None, measurements=None):
        self.metadata_type = metadata_type
        self.metadata = metadata
        self.measurements = measurements

    @property
    def metadata_type(self):
        """"ADD DOCSTRING!"""
        return self.collection.properties.get('product_definition:metadata_type')

    @metadata_type.setter
    def metadata_type(self, v):
        self.collection.properties['product_definition:metadata_type'] = v

    @property
    def metadata(self):
        """"ADD DOCSTRING!"""
        return self.collection.properties.get('product_definition:metadata')

    @metadata.setter
    def metadata(self, v):
        self.collection.properties['product_definition:metadata'] = v

    @property
    def measurements(self):
        """"ADD DOCSTRING!"""
        return self.collection.properties.get('product_definition:measurements')

    @measurements.setter
    def measurements(self, v):
        self.collection.properties['product_definition:measurements'] = v

    @classmethod
    def from_collection(self, collection):
        return ProdefColExt(collection)

    @classmethod
    def _object_links(cls):
        return []


def register_product_definition_extension():
    extended_object = ExtendedObject(Collection, ProdefColExt)
    extension_definition = ExtensionDefinition(Extensions.PRODUCT_DEFINITION, [extended_object])
    STAC_EXTENSIONS.add_extension(extension_definition)

def register_odc_extension():
    extended_object = ExtendedObject(Item, ODCExt)
    extension_definition = ExtensionDefinition(Extensions.ODC, [extended_object])
    STAC_EXTENSIONS.add_extension(extension_definition)