import plotly.express as px

def plot_topics(topic_predictions):
    topic_preds_T = topic_predictions.T
    topic_preds_T.reset_index(inplace=True)
    topic_preds_T.columns = ['Topic', 'Affinity']
    
    fig = px.bar(
        topic_preds_T, 
        x='Topic', 
        y='Affinity',
        title="Predicted Topic Affinity Of Paper"
    )

    fig.update_layout(
        title={
            'text' : "<b>Predicted Topic Affinity Of Paper</b>",
            'y' : 0.95,
            'x' : 0.5,
            'xanchor' : 'center',
            'yanchor' : 'top'
        }
    )

    return fig.to_html(full_html=False, include_plotlyjs='cdn')