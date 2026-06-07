from enum import Enum


class FieldType(str, Enum):
    CLASSIFIER = 'classifier'
    PROPERTY = 'property'


class ClassifierMode(str, Enum):
    SINGLE = 'single'
    MULTI = 'multi'
    ABBREVIATED = 'abbreviated'


class PropertyMode(str, Enum):
    NUMBER = 'number'
    TEXT = 'text'
    DATE = 'date'


REQUIRED_FIELDS = {
    'doc_type': {
        'type': FieldType.PROPERTY,
        'mode': PropertyMode.NUMBER
    },
    'office_class_view_docs': {
        'type': FieldType.CLASSIFIER,
        'mode': ClassifierMode.SINGLE
    }
}

ALL_FIELDS = {
    'doc_type': {
        'type': FieldType.PROPERTY,
        'mode': PropertyMode.NUMBER
    },
    'office_class_view_docs': {
        'type': FieldType.CLASSIFIER,
        'mode': ClassifierMode.SINGLE
    },
    'doc_num': {
        'type': FieldType.PROPERTY,
        'mode': PropertyMode.NUMBER
    },
    'link_to_num': {
        'type': FieldType.PROPERTY,
        'mode': PropertyMode.NUMBER
    },
    'data_experiment': {
        'type': FieldType.PROPERTY,
        'mode': PropertyMode.DATE
    },
    'whom': {
        'type': FieldType.CLASSIFIER,
        'mode': ClassifierMode.SINGLE
    },
    'target_department': {
        'type': FieldType.CLASSIFIER,
        'mode': ClassifierMode.SINGLE
    },
    'responsible_performer': {
        'type': FieldType.CLASSIFIER,
        'mode': ClassifierMode.SINGLE
    },
    'signature': {
        'type': FieldType.CLASSIFIER,
        'mode': ClassifierMode.ABBREVIATED
    },
    'coordinator_name': {
        'type': FieldType.CLASSIFIER,
        'mode': ClassifierMode.ABBREVIATED
    },
    'number_64_test': {
        'type': FieldType.PROPERTY,
        'mode': PropertyMode.NUMBER
    },
    'users_my_org_test': {
        'type': FieldType.CLASSIFIER,
        'mode': ClassifierMode.SINGLE
    },
    'by_attorney': {
        'type': FieldType.PROPERTY,
        'mode': PropertyMode.NUMBER
    },
    'office_class_topics': {
        'type': FieldType.CLASSIFIER,
        'mode': ClassifierMode.SINGLE
    },
    'office_class_corrs': {
        'type': FieldType.CLASSIFIER,
        'mode': ClassifierMode.SINGLE
    },
    'document_type_field_meeting_region': {
        'type': FieldType.CLASSIFIER,
        'mode': ClassifierMode.MULTI
    },
    'document_type_field_meeting': {
        'type': FieldType.CLASSIFIER,
        'mode': ClassifierMode.MULTI
    },
    'print_font_size_pt': {
        'type': FieldType.CLASSIFIER,
        'mode': ClassifierMode.SINGLE
    },
    'smrkdocinfo': {
        'type': FieldType.PROPERTY,
        'mode': PropertyMode.TEXT
    }
}
