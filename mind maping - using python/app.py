from flask import Flask, render_template, request, jsonify
import networkx as nx
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    topic = request.form['topic']
    mind_map_data = generate_mind_map(topic)
    print(json.dumps(mind_map_data))  # Add this line to see the output in the console
    return jsonify(mind_map_data)

def generate_mind_map(topic):
    # Create a basic graph with NetworkX
    G = nx.Graph()

    # Add a central topic node
    G.add_node(topic, description=f"Main topic: {topic}")

    # Define subtopics and their descriptions
    subtopics = {
        "Definition": "The explanation of the topic.",
        "Applications": "Various ways this topic can be utilized.",
        "Challenges": "Common obstacles encountered.",
        "Tools": "Tools or software related to the topic."
    }

    # Define child nodes for each subtopic and their descriptions
    child_nodes = {
        "Definition": [
            ("Meaning", "The general meaning or interpretation."),
            ("Examples", "Examples of the topic in real-world scenarios.")
        ],
        "Applications": [
            ("In Education", "Usage in educational settings."),
            ("In Industry", "Usage in industrial contexts.")
        ],
        "Challenges": [
            ("Data Privacy", "Concerns regarding data protection."),
            ("Implementation Issues", "Problems faced during execution.")
        ],
        "Tools": [
            ("Software A", "Description of Software A."),
            ("Software B", "Description of Software B.")
        ],
    }

    # Add subtopics and their descriptions to the graph
    for subtopic, description in subtopics.items():
        G.add_node(subtopic, description=description)
        G.add_edge(topic, subtopic)

        # Add child nodes for each subtopic
        for child, child_description in child_nodes[subtopic]:
            G.add_node(child, description=child_description)
            G.add_edge(subtopic, child)

    # Prepare data for Plotly
    pos = nx.spring_layout(G, dim=3, seed=42)  # Fixed seed for consistent layout
    edge_trace = []
    node_trace = []

    # Customizing node appearance and adding descriptions
    for node in G.nodes():
        x, y, z = pos[node]
        size = 50 if node == topic else 20  # Main topic larger
        color = '#1f77b4' if node == topic else '#ff7f0e'  # Main topic color

        # Create node traces with description as part of the text
        description = G.nodes[node]['description']
        node_trace.append({
            'x': [x], 'y': [y], 'z': [z],
            'text': f"{node}: {description}",
            'mode': 'markers+text',
            'marker': {
                'size': size,
                'color': color,
                'line': {'width': 2, 'color': 'black'}
            },
            'textposition': 'top center',
            'customdata': list(child_nodes.get(node, []))  # Store child nodes as custom data
        })

    # Create edge traces
    for edge in G.edges():
        x0, y0, z0 = pos[edge[0]]
        x1, y1, z1 = pos[edge[1]]
        edge_trace.append({
            'x': [x0, x1, None],
            'y': [y0, y1, None],
            'z': [z0, z1, None],
            'mode': 'lines',
            'line': {'width': 2, 'color': '#888'}
        })

    return {'nodes': node_trace, 'edges': edge_trace}

if __name__ == '__main__':
    app.run(debug=True)
