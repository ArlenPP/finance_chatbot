chatbot_states_config = {
    'states': [
        'init', 'future', 'future_date', 
        'strategy', 'strategy_num', 'strategy_date',
    ],
    'transitions': [
        {
            'trigger': 'advance',
            'source': 'init',
            'dest': 'future',
            'conditions': 'is_go_to_future',
        },
        {
            'trigger': 'advance',
            'source': 'init',
            'dest': 'strategy',
            'conditions': 'is_go_to_strategy',
        },
        {
            'trigger': 'advance',
            'source': 'init',
            'dest': 'init',
            'unless': ['is_go_to_future', 'is_go_to_strategy'],
        },
        {
            'trigger': 'advance',
            'source': 'future',
            'dest': 'future_date',
            'conditions': 'is_go_to_future_date',
        },
        {
            'trigger': 'go_back_future',
            'source': 'future_date',
            'dest': 'future',
        },
        {
            'trigger': 'go_init',
            'source': ['init', 'future_date', 'strategy_date'],
            'dest': 'init',
        },
        {
            'trigger': 'advance',
            'source': 'strategy',
            'dest': 'strategy_num',
            'conditions': 'is_go_to_strategy_num',
        },
        {
            'trigger': 'advance',
            'source': 'strategy_num',
            'dest': 'strategy_date',
            'conditions': 'is_go_to_strategy_date',
        },
        {
            'trigger': 'go_back_strategy_num',
            'source': 'strategy_date',
            'dest': 'strategy_num',
        },

    ],
    'initial': 'init',
    'auto_transitions': False,
    # 'show_conditions': True,
}