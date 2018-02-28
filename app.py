from flask import Flask, request, send_from_directory
import os
from jira_dependency_graph import JiraSearch, build_graph_data, create_graph_image, filter_duplicates
app = Flask(__name__)

@app.route('/')
def index():
    jira_url = os.environ["JIRA_URL"]
    auth = str(request.args.get("cookie"))
    node_shape = "box"
    file_name = "issue_graph.png"
    directions = ["inward"]

    jira = JiraSearch(jira_url, auth)

    graph = []
    for issue in request.args.get("issues").split(","):
        graph = graph + build_graph_data(issue, jira, excludes=[], show_directions=["inward", "outward"], directions=directions, includes="", ignore_closed=False, ignore_epic=False, ignore_subtasks=False, traverse=True)

    image = create_graph_image(filter_duplicates(graph), file_name, node_shape)
    return send_from_directory(".", file_name)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
