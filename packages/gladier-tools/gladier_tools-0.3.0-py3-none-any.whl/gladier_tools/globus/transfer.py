from gladier import GladierBaseTool


class Transfer(GladierBaseTool):

    flow_definition = {
        'Comment': 'Transfer a file or directory in Globus',
        'StartAt': 'Transfer',
        'States': {
            'Transfer': {
                'Comment': 'Transfer a file or directory in Globus',
                'Type': 'Action',
                'ActionUrl': 'https://actions.automate.globus.org/transfer/transfer',
                'Parameters': {
                    'source_endpoint_id.$': '$.input.transfer_source_endpoint_id',
                    'destination_endpoint_id.$': '$.input.transfer_destination_endpoint_id',
                    'transfer_items': [
                        {
                            'source_path.$': '$.input.transfer_source_path',
                            'destination_path.$': '$.input.transfer_destination_path',
                            'recursive.$': '$.input.transfer_recursive',
                        }
                    ]
                },
                'ResultPath': '$.Transfer',
                'WaitTime': 600,
                'End': True
            },
        }
    }

    flow_input = {
        'transfer_sync_level': 'checksum'
    }
    required_input = [
        'transfer_source_path',
        'transfer_destination_path',
        'transfer_source_endpoint_id',
        'transfer_destination_endpoint_id',
        'transfer_recursive',
    ]
