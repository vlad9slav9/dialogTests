from enum import Enum


class FieldType(str, Enum):
    CLASSIFIER = 'classifier'
    PROPERTY = 'property'


class ClassifierMode(str, Enum):
    SINGLE = 'single'
    MULTI = 'multi'
    ABBREVIATED = 'abbreviated'


FIELDS = {
    'doc_type': {
        'type': FieldType.PROPERTY
    },
    'by_attorney': {
        'type': FieldType.PROPERTY
    },
    'office_class_view_docs': {
        'type': FieldType.CLASSIFIER,
        'mode': ClassifierMode.SINGLE
    },
    'document_type_field_meeting_region': {
        'type': FieldType.CLASSIFIER,
        'mode': ClassifierMode.MULTI
    },
    'signature': {
        'type': FieldType.CLASSIFIER,
        'mode': ClassifierMode.ABBREVIATED
    }
}
