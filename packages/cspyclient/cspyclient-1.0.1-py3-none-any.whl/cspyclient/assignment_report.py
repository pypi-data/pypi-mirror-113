from .cohort import Cohort
from .assignment import Assignment
from .submission import Submission
import pandas as pd
import numpy as np

def assignment_report(assignment_name, port=8050):
    '''Generate a real-time Dash app that shows the assignment report

    Parameters:
        - assignment_name: name of the assignment
    '''
    try:
        from jupyter_dash import JupyterDash 
        import dash_core_components as dcc
        import dash_html_components as html
        import dash_bootstrap_components as dbc
        from dash.dependencies import Input, Output
        import dash_table
        import plotly.express as px
        from plotly.subplots import make_subplots
        import plotly.graph_objects as go
    except:
        print('Installation required: jupyter-dash and dash-bootstrap-components (use pip install)')
        return

    app = JupyterDash(__name__, external_stylesheets=[dbc.themes.SUPERHERO],
                    meta_tags=[{'name': 'viewport',
                                'content': 'width=device-width, initial-scale=1.0'}]
                    )

    # Data
    assignment = Assignment.find_one_by_name(assignment_name)
    if not getattr(assignment, '_id', None) or not assignment._id:
        print("ERROR: Assignment not found")
        return

    cohort = Cohort.find_by_id(assignment.cohort_id)
    if not getattr(cohort, '_id', None) or not assignment._id:
        print("ERROR: Cohort not found")
        return

    def get_assignment_report_data(assignment, include_staff=False):
        data = {
            'students': pd.DataFrame(columns=['name', 'email','currentScore', 'entries', 'time']),
            'n_student': 0,
            'submissions': [],
            'n_submission': 0,
            'student_scores': [],
            'n_submitted': 0,
            'avg_score': 0,
            'plot_progress_data': pd.DataFrame(columns=['time', 'currentScore', 'email'])
        }
        students, n_student = cohort.get_student_list()
        if not n_student:
            return data
        
        data['n_student'] = n_student

        # Cleaning submission
        submissions, n_submission = Submission.find_all({'assignmentId': assignment._id})
        if not n_submission:
            students['entries'] = 0
            students['currentScore'] = -1
            students['time'] = 0
            students = students[['name', 'email','currentScore', 'entries', 'time']]
            data['students'] = students
            return data
        
        if not include_staff:
            staffs, num_staff = cohort.get_staff_list()
            staff_emails = staffs['email'].uniques() if staffs else []
            if staff_emails:
                submissions = submissions[~submissions['email'].isin(staff_emails)] 
        submissions = submissions[['_id', 'cohortMember', 'assignment', 'name', 'email', 'currentScore', 'createdAt']]
        submissions['createdAt'] = pd.to_datetime(submissions['createdAt'])
        submissions['assignmentName'] = assignment.name
        n_submission = submissions.shape[0]
        data['submissions'] = submissions
        data['n_submission'] = n_submission

        # Current score table
        student_scores = pd.pivot_table(submissions[['email', 'assignmentName', 'currentScore']], 
                                values='currentScore', index='email', columns=['assignmentName'], 
                                aggfunc=np.max).fillna(0)

        students['entries'] = students.apply(lambda row: len(submissions[submissions['email']==row['email']]), axis=1)
        students['currentScore'] = students.merge(student_scores, on='email', how='left').fillna(-1)[assignment.name]
        data['student_scores'] = student_scores
        data['n_submitted'] = student_scores.shape[0]
        data['avg_score'] = int(student_scores[assignment.name].mean())


        # Compute duration
        first_created = submissions.groupby('email')['createdAt'].min().reset_index().rename(columns={'createdAt': 'firstCreated'})
        plot_progress_data = pd.merge(submissions, first_created, on='email')
        plot_progress_data['time'] = (plot_progress_data['createdAt'] - plot_progress_data['firstCreated']) / pd.to_timedelta(1, 'm')
        plot_progress_data['time'] = plot_progress_data['time'].apply(int)
        data['plot_progress_data'] = plot_progress_data

        students = students.merge(plot_progress_data.groupby('email')[['time']].max(), on='email', how='left').fillna(-1)
        students = students[['name', 'email','currentScore', 'entries', 'time']]
        data['students'] = students

        return data

    # Navbar
    navbar = dbc.Navbar([
        html.A(
            dbc.Row(
                [

                    dbc.Col(html.Img(src="https://i.imgur.com/dpd20EG.png", height="30px")),
                    dbc.Col(dbc.NavbarBrand(f"{cohort.name} - {assignment.name}", className="ml-2")),
                ],
                align='center',
                no_gutters=True
            ),
            href="#"
        )
    ], color="dark", dark=True)

    # Score cards
    score_cards = html.Div(id='score-cards')

    # Student table
    student_table = dbc.Row([
        dbc.Col(id='student-table'),
    ])

    # Histogram
    histogram = html.Div([
        dcc.Graph(id='score_histogram'),
    ])

    # Progress graph
    progress_graph = html.Div([
        dcc.Graph(id='progress-graph'),
    ], className='my-4')

    # App layout
    app.layout = dbc.Container([
        navbar,
        score_cards,
        student_table,
        histogram,
        progress_graph,
        dcc.Interval(
            id='interval-component',
            interval=10*1000, # in milliseconds
            n_intervals=0
        )
    ])

    @app.callback(Output('score-cards', 'children'),
                  Output('student-table', 'children'),
                  Output('score_histogram', 'figure'),
                  Output('progress-graph', 'figure'),
                  Input('interval-component', 'n_intervals'))
    def update_graph_live(n):
        data = get_assignment_report_data(assignment)
        students = data['students']
        n_student = data['n_student']
        n_submission = data['n_submission']
        student_scores = data['student_scores']
        n_submitted = data['n_submitted']
        avg_score = data['avg_score']
        plot_progress_data = data['plot_progress_data']
        
        # Scorecards        
        num_student_card = dbc.Card([
            dbc.CardBody([
                html.H3(f'{n_submitted} / {n_student}', className='card_title'),
                html.P("Students submitted", className='card-text')
            ])
        ], color="primary", inverse=True)

        num_submission_card = dbc.Card([
            dbc.CardBody([
                html.H3(f'{n_submission}', className='card_title'),
                html.P("Submissions", className='card-text')
            ])
        ], color="secondary", inverse=True)

        avg_score_card = dbc.Card([
            dbc.CardBody([
                html.H3(f'{avg_score} / {assignment.total_score}', className='card_title'),
                html.P("Average score / Total score", className='card-text')
            ])
        ], color="info", inverse=True)
        new_score_cards = [
            dbc.Row([
                dbc.Col(num_student_card),
                dbc.Col(num_submission_card),
                dbc.Col(avg_score_card),
            ], className='my-4')
        ]
        
        # Student table
        std_table = dash_table.DataTable(
            id='datatable-interactivity',
            columns=[
                {"name": i, "id": i} for i in students.columns
            ],
            data=students.to_dict('records'),

            page_action='none',
            style_table={'height': '300px', 'overflowY': 'auto'},

            filter_action="native",
            row_selectable="multi",
            sort_action="native",
            sort_mode="multi",
            selected_rows=[],

            style_header={ 
                'border': '1px solid #2c3e50',
                'color': 'white',
                'backgroundColor': '#34495e'
            },
            style_cell={
                # 'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'black',
                'textAlign': 'left',
                'border': '1px solid #2c3e50',
                'font-family': 'Helvetica Neue'
            },
            style_data_conditional=[                
                {
                    "if": {"state": "selected"},
                    "backgroundColor": "inherit !important",
                    "border": "inherit !important",
                }   
            ]

        )
        
        # Histogram
        fig_hist = make_subplots(rows=1, cols=2, subplot_titles=('currentScore', 'Time'))
        fig_hist.add_trace(
            go.Histogram(
                x=students['currentScore'],
                nbinsx=10, 
                marker_color='slateblue', 
                name='Time',
                hovertemplate=
                '<i>Range</i>: %{x}'+
                '<br><i>Count</i>: %{y}'
            ),
            row=1, 
            col=1
        )
        fig_hist.add_trace(
            go.Histogram(
                x=students['time'], 
                nbinsx=10, 
                marker_color='salmon', 
                name='Time',
                hovertemplate=
                '<i>Range</i>: %{x}'+
                '<br><i>Count</i>: %{y}'
            ),
            row=1, 
            col=2
        )
        fig_hist.update_layout(
            title_text='Score and Time Distribution',
            template="plotly_white", 
            showlegend=False)
        
        # Progress graph
        if plot_progress_data.shape[0] > 0:
            fig_progress = px.line(plot_progress_data, 
                                  x="time", 
                                  y="currentScore", 
                                  color="email",
                                  hover_name="email",
                                  template="plotly_white")
            fig_progress.update_traces(mode="markers+lines")
            fig_progress.update_layout(title_text='Student Progresses')
        else:
            fig_progress = {}
        
        return new_score_cards, std_table, fig_hist, fig_progress


    app.run_server(mode='inline', port=port, debug=True)